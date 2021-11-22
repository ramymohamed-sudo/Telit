

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


class WifiMqtt(mqtt.Client):
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


def initialize_sensor_data():
    global sensor_data
    sensor_data = dict()
    millis = int(round(time.time() * 1000))
    sensor_data['timestamp'] = millis
    sensor_data['name'] = socket.gethostname()

""" features such as no of running processes/ # Telit or BG96 """
def cpu_temp_process_ram_utilization():
    # CPU_temp = float(getCPUtemperature())
    # CPU_use = float(getCPUuse())
    # RAM_stats = getRAMinfo()
    # DISK_stats = getDiskSpace()
    # RAM_use = round(int(RAM_stats[1]) / 1000,1)
    # DISK_perc = DISK_stats[3]
    sensor_data['CPU_temp'] = float(getCPUtemperature())
    sensor_data['CPU_use'] = float(getCPUuse())
    sensor_data['RAM_use'] = round(int(getRAMinfo()[1]) / 1000,1)
    sensor_data['DISK_perc'] = getDiskSpace()[3]
    WiFi_ssd = str(subprocess.check_output('iwgetid', shell=True))
    if search('HUAWEI', WiFi_ssd):
        sensor_data['WiFi'] = True
    else:
        sensor_data['WiFi'] = False


""" Raspberry PI parameters reading"""
def raspb_pi_update_values():
    cpu_temp = subprocess.check_output('vcgencmd measure_temp', shell=True)
    sensor_data['cpu_temperature'] = float(str(cpu_temp)[7:11])
    # memory usage/ CPU usage of the R-PI as well
    # RX/TX and processing on BG96
    # looking for intergrated sensors as one part on chip



""" BG96 parameters reading"""
def update_BG_values():
    sensor_data['tx_pwr'] = 1.0
    sensor_data['nb_iot_mode'] = 'mode'
    # sensor_data['humidity'] = str(round(node.readHum(), 2))
    # sensor_data['temperature'] = str(round(node.readTemp(), 2))
    # sensor_data['light'] = light
    # sensor_data['acceleration_x'] = 0.0  # str(node.readAccel())[0]
    # sensor_data['acceleration_y'] = 1.1  # str(node.readAccel())[1]
    # sensor_data['acceleration_z'] = 2.2  # str(node.readAccel())[2]
    # sensor_data['adc0'] = str(node.readAdc(0))
    # sensor_data['adc1'] = str(node.readAdc(1))
    # sensor_data['adc2'] = str(node.readAdc(2))
    # sensor_data['adc3'] = str(node.readAdc(3))

""" Battery parameters reading"""
def battery_update_values():
    # use try/except here please
    status = pijuice.status.GetStatus()
    key, value = next(iter(status.items()))
    if key != 'error':
        sensor_data['battery_level'] = pijuice.status.GetChargeLevel()['data']
        sensor_data['battery_milli_voltage'] = pijuice.status.GetBatteryVoltage()['data']
        sensor_data['battery_temperature'] = pijuice.status.GetBatteryTemperature()['data']
        sensor_data['hours_since_fully_charged'] = 2    # env.variables from IFTT script
        sensor_data['charge_cycle'] = '1'
        """ Battery methods to enable/disable charging """
        # pijuice.status.GetStatus()
        # pijuice.status.GetChargeLevel()
        # pijuice.status.GetFaultStatus()
        # pijuice.status.GetBatteryTemperature()
        # pijuice.status.GetChargeLevel()
    else: 
        sensor_data['battery_level'] = 90.0
        sensor_data['battery_milli_voltage'] = 30.0
        sensor_data['battery_temperature'] = 18.0
        sensor_data['hours_since_fully_charged'] = 2
        sensor_data['charge_cycle'] = '1'

def main():
    # data = ','.join(row)
    initialize_sensor_data()
    update_BG_values()
    cpu_temp_process_ram_utilization()
    battery_update_values()

iot_is_used = False     # True
sensor_data = dict()
node = IoTMqtt()
node.setupGPIO()
no_of_iter = 3
i = 1


""" The lines below should be uncommented for real scenarios """
node.disable()
sleep(5)
node.enable()
sleep(5)
node.powerUp()     # we might need a condition to check it is powered up
sleep(10)

if __name__ == "__main__":

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
                data_frame_json = json.dumps(sensor_data, indent=4)
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
                data_frame_json = json.dumps(sensor_data, indent=4)
                client.publish(client.topic, data_frame_json)
                # client.publish(topic,json.loads(str(row)))
                client.on_publish_message(data_frame_json)
                sleep(5)
                i += 1

