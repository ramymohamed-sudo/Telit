

from pijuice import PiJuice
import IoTSixfab
from time import sleep
import subprocess
import time
import json
import paho.mqtt.client as mqtt
import datetime
import numpy as np
import csv
import os
import sys
import flask
import socket
from re import search
from processor import getCPUtemperature, getRAMinfo, getCPUuse, getDiskSpace


connected = False
MessageReceived = False
pijuice = PiJuice(1, 0x14)


# name = name, inherit from two classes :) 
class WifiMqtt(mqtt.Client, subprocess.SensorData):
    def __init__(self,
                 broker_address='9.162.161.90',
                 keepAlive=60,
                 port=1883,
                 topic="5G-Solutions",
                 client_type='subscriber'):
        super(WifiMqtt, self).__init__()
        self.broker_address = broker_address
        self.keepAlive = keepAlive
        self.port = port
        self.topic = topic
        self.client_type = client_type
        # self.on_message = self.onmessage
        # self.on_connect = self.onconnect

    @staticmethod   # or self.on_connect = self.onconnect
    def on_connect(xxx, userdata, flags, rc):  # onconnect()
        if rc == 0:
            print("WifiMqtt is connected to the broker .......")
            print("\n")
            global connected
            connected = True
            # client.subscribe(topic)
        else:
            print("WifiMqtt is not connected")

    @staticmethod
    def on_message(xxx, xxr, message):  # onmessage()
        rx_msg = message.payload.decode("utf-8")
        print("Message is received " + str(rx_msg))
        rx_msg_dict = json.loads(rx_msg)
        global MessageReceived

    def on_publish_message(self, data_row):
        # print(self.topic, ','.join(data_row))
        json_data = data_row
        print("json_data", json_data)


class IoTMqtt(IoTSixfab.IoT):
    def __init__(self,
                host_name= '9.162.161.90',
                port="1883",
                topic="5G-Solutions",
                clientID=socket.gethostname(),      # "sixfab"
                tcpconnectID=0,
                msgID=1,
                qos=0,
                retain=0,
                msg = "Hello world 22",
                name='IoTMqtt'):
        super(IoTMqtt, self).__init__()         # name=name

        self.host_name = host_name
        self.port = port
        self.topic = topic
        self.clientID = clientID
        self.tcpconnectID = tcpconnectID
        self.msgID = msgID
        self.qos = qos
        self.retain = retain
        self.msg = msg
        # <tcpconnectID> MQTT socket identifier. The range is 0-5.
        # <clientID> The client identifier string.
        # <username> User name of the client. It can be used for authentication.
        # <password> Password corresponding to the user name of the client.
        self.no_of_secs_before_send_msg = 5
    
    def enable_disable_powerup(self):
        self.setupGPIO()
        sleep(2)
        self.disable()
        sleep(2)
        self.enable()
        sleep(2)
        self.powerUp()
        sleep(10)

    def mqtt_open(self):
        # AT+QMTOPEN=<tcpconnectID>,"<host_name>"",<port>
        # self.sendATComm("AT+QMTOPEN=0, "+self.host_name+", "+self.port,"+QMTOPEN: 0")
        self.sendATComm("AT+QMTOPEN=0, \"9.162.161.90\", 1883","+QMTOPEN: 0")

    def mqtt_status(self):
        self.sendATComm("AT+QMTOPEN?","OK")

    def mqtt_connect(self):
        # AT+QMTCONN=<tcpconnectID>,"<clientID>"[,"<username>"[,"<password>"]]
        self.sendATComm("AT+QMTCONN=0,\"sixfab\"","+QMTCONN: 0")

    def mqtt_publish(self, message):
        # AT+QMTPUB=<tcpconnectID>,<msgID>,<qos>,<retain>,"<topic>"
        # self.sendATComm("AT+QMTPUB=0,0,0,0,"+self.topic,">")
        self.sendATComm("AT+QMTPUB=0,0,0,0,\"5G-Solutions\"",">")
        print(f"Waiting {self.no_of_secs_before_send_msg} seconds before sending a message....")
        sleep(self.no_of_secs_before_send_msg)
        self.data_frame_json = message
        self.sendATComm(self.data_frame_json+self.CTRL_Z,"+QMTPUB: 0,0,0")

    def mqtt_close(self):
        # # AT+QMTCLOSE=<tcpconnectID>
        self.sendATComm("AT+QMTCLOSE=0","+QMTCLOSE: 0")


def main():
    # initialize_sensor_data()
    sensor_data.timestamp()
    sensor_data.update_BG_values()
    sensor_data.cpu_temp_process_ram_utilization()
    sensor_data.battery_update_values()

    

iot_is_used = False     # True
node = IoTMqtt()
node.setupGPIO()
no_of_iter = 3
i = 1

""" The lines below should be uncommented for real scenarios """
if iot_is_used:
    node.disable()
    sleep(5)
    node.enable()
    sleep(5)
    node.powerUp()     # a condition to check it is powered up!
    sleep(10)

if __name__ == "__main__":
    sensor_data = subprocess.SensorData()

    if iot_is_used:
        registered = False
        no_of_reg_loops = 50
        init_ctr = 0
        node_getOperator = node.sendATComm("AT+COPS?","OK\r\n")     # the module should be up/powered
        # if the sensor not registered, wait a few loops until register 
        while (no_of_reg_loops > 1):
            if search('Amarisoft', node_getOperator):
                print("The sensor is registered with Amarisoft")
                registered = True
                break
            no_of_reg_loops -= 1
            init_ctr += 1
            print(f"waiting {init_ctr*10} secs for registeration")
            sleep(10)
            node_getOperator = node.sendATComm("AT+COPS?","OK\r\n")

        if registered:        
            # MQTT Connection - check the MQTT status
            node_mqtt_status = node.sendATComm("AT+QMTOPEN?","OK")  # the node should be registered
            while not (search(node.host_name, node_mqtt_status)):
                print("trying to open MQTT connection via mqtt_open() and mqtt_connect()")
                node.mqtt_open()
                sleep(10)
                print("mqtt_open() is passed")
                node.mqtt_connect()
                sleep(10)
                print("mqtt_connect() is passed")
                node_mqtt_status = node.sendATComm("AT+QMTOPEN?","OK")
                # pass
                # break this loop after a few times and call node.sendATComm("AT+COPS?","OK\r\n")
                # and come to these steps again
            print("The MQTT connection is now open and connected?")

            while i <= no_of_iter:
                print(f"iteration number {i}")
                main()
                data_frame_json = json.dumps(sensor_data.sensor_data, indent=4)
                node.mqtt_publish(data_frame_json)
                # node.mqtt_close()
                sleep(1)
                i += 1

    else:
        client = WifiMqtt(client_type='publisher')
        client.connect(client.broker_address, client.port, client.keepAlive)
        client.subscribe(client.topic)
        print(f"The subscriber just subscribed to topic {client.topic}")
        if client.client_type == 'subscriber':
            client.loop_start()
            # print("The loop is just started >>>>>")
            while not connected:
                sleep(0.2)
            while not MessageReceived:
                sleep(0.2)
            client.loop_stop()
        
        else:
            while i <= no_of_iter:
                print(f"iteration number {i}")
                main()
                data_frame_json = json.dumps(sensor_data.sensor_data, indent=4)
                client.publish(client.topic, data_frame_json)
                # client.publish(topic,json.loads(str(row)))
                client.on_publish_message(data_frame_json)
                sleep(5)
                i += 1

