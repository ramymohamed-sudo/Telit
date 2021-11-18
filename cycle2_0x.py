

""" This code is based on Sixfab basic HAT and Telit module and Pijuice HAT 
No built-in sensors witht the Sixfab HAT - 
Remember for Pijuice HAT, there was a function to stop the battery from being charged (if needed)
"""

from pijuice import PiJuice
import IoTSixfabTelit
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
import itertools


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
            print("WifiMqtt is connected to the broker .....")
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


class IoTMqtt(IoTSixfabTelit.IoT):
    def __init__(self,
                broker_address= '9.162.161.90',
                port=1883,
                topic="5G-Solutions",
                clientID="sixfab",
                tcpconnectID=0,
                msgID=1,
                qos=0,
                retain=0,
                msg = "Hello world 22",
                name='IoTMqtt'):
        super(IoTMqtt, self).__init__()         # name=name

        self.broker_address = broker_address
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
        self.secs_befr_send = 5
    
    def mqtt_check_and_enable(self):
        self.node_mqtt_check_enable = self.sendATComm("AT#MQEN?","OK")
        if not search('1,1', self.node_mqtt_check_enable):      # 1,1 and 2,1??
            print("Enable MQTT feature as it not enabled")
            self.sendATComm("AT#MQEN=1,1","OK")
        
    
    def pdp_context_check_and_enable(self):
        self.sendATComm("AT+CREG=1","OK")
        sleep(5)
        self.sendATComm("AT+CEREG=1","OK")
        sleep(5)
        self.sendATComm("AT+CGREG=1","OK")
        sleep(5)
        # get CID/IP address
        self.cid_addr = self.sendATComm("AT+CGPADDR=1","OK")    # +CGPADDR: 1, "192.168.2.6"
        self.cid_addr = search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', self.cid_addr).group()
        print("self.cid_addr", self.cid_addr)
        sleep(5)

        self.cgdcont = self.sendATComm("AT+CGDCONT?","OK")
        if not search(self.cid_addr, self.cgdcont):      # 1,1 and 2,1??
            print("Set the IP address of the PDP context")
            self.sendATComm("AT+CGDCONT=1,\"IP\",\"default\","+str(self.cid_addr)+",0,0","OK")
            self.sendATComm("AT+CGDCONT?","OK")
            sleep(5)
        
        self.sgact = self.sendATComm("AT#SGACT?","OK")   # IPEasy Context Activation
        if not search('1,1', self.sgact):
            self.sendATComm("AT#SGACT=1,1","OK")
            sleep(5)
        print("pdp_context_check_and_enable is finished")


    def mqtt_status(self):      
        # check the current configuration, e.g., hostname, port number, etc
        self.sendATComm("AT#MQCFG?","OK")

    def mqtt_open(self):    
        self.sendATComm("AT#MQCFG=1,\"9.162.161.90\",1883,1","OK") 
        
    def mqtt_connect(self): 
        # self.sendATComm("AT#MQCONN=1,\"1\",\"userName\",\"passWord\"","OK")
        name = socket.gethostname()    
        self.sendATComm(f"AT#MQCONN=1,\"{name}\",\"userName\",\"passWord\"","OK")

    def check_config_open_connect(self):
        mqtt_config_status = self.sendATComm("AT#MQCFG?","OK")
        if not (search(self.broker_address, mqtt_config_status)):
            print("open the MQTT connection via mqtt_open()")
            self.mqtt_open()
            sleep(5)
            print("Connect MQTT via mqtt_connect()")
            self.mqtt_connect()
            sleep(5)
        
        mqtt_connect_status = self.sendATComm("AT#MQCONN?","OK")    # should return 1,1
        if search('#MQCONN: 1,0', mqtt_connect_status):
            print("The MQTT connection is not open now")
            print("Connect MQTT via mqtt_connect()")
            self.mqtt_connect()

        if search('#MQCONN: 1,1', mqtt_connect_status):
            print("The MQTT connection is now open and connected")

        elif search('#MQCONN: 1,2', mqtt_connect_status):
            print("Please restart the module and exit code as connection status is 2")
            self.sendATComm("AT#REBOOT","OK")
            sys.exit()
        else:
            print("The MQTT connection is not open - please DEBUG this manually")
            self.sendATComm("AT#MQCONN?","OK") 
            sys.exit()


    def mqtt_publish(self, message=None):
        print(f"Waiting {self.secs_befr_send} seconds before sending sensor data....")
        sleep(self.secs_befr_send)
        # self.myMessage = "Hello 2025"
        # self.sendATComm("AT#MQPUBS=1,\"5G-Solutions\",0,0,"+self.myMessage+self.CTRL_Z,"OK")
        self.new_sensor_data = dict(itertools.islice(sensor_data.items(), 9))
        print("len(json.dumps(self.new_sensor_data))", len(json.dumps(self.new_sensor_data)))

        # sensor_data = dict()
        # sensor_data['ID'] = 12
        # sensor_data['Battery'] = 90.0
        # self.new_sensor_data = json.dumps(sensor_data) + self.CTRL_Z
        
        # sensor_data = {"ID": 12, "Battery": 90}
        # sensor_data = {'tim': 1637243564699,
        #                'nm': 'cycle2-07',
        #                'tx_pwr': 1.0,
        #                'mode': 'mode',
        #                'cpu_tmp': 65.7,
        #                'btr_lvl': 97,
        #                'btr_vol': 4148,
        #                'btr_tmp': 40,
        #                'hrs_sinc_chrg': 2,
        #                'chrg_cycl': '1'}

        self.sendATComm(f"AT#MQPUBS=1,\"5G-Solutions\",0,0,\"{self.new_sensor_data}\""+self.CTRL_Z,"OK") # this also works well 
        # self.sendATComm("AT#MQPUBS=1,\"5G-Solutions\",0,0,"+self.new_sensor_data,"OK")
        
    def mqtt_close(self):
        self.sendATComm("AT#MQDISC=1","OK")
    
    def subs_topic(self):
        self.sendATComm("AT#MQSUB=1,\"5G-Solutions\"","OK")

def initialize_sensor_data():
    global sensor_data
    sensor_data = dict()
    millis = int(round(time.time() * 1000))
    sensor_data['tim'] = millis
    sensor_data['nm'] = socket.gethostname()


""" add features such as CPU Temperature/no of running processes/CPU 
and RAM utilization """
def cpu_temp_no_of_process_ram_utilization():
    pass

""" Telit parameters reading"""
def update_Telit_values():
    sensor_data['tx_pwr'] = 1.0
    sensor_data['mode'] = 'mode'
    # sensor_data['humidity'] = str(round(node.readHum(), 2))
    # sensor_data['temperature'] = str(round(node.readTemp(), 2))
    # sensor_data['light'] = light
    # sensor_data['acceleration_x'] = 0.0  
    # sensor_data['acceleration_y'] = 1.1  
    # sensor_data['acceleration_z'] = 2.2

""" Raspberry PI parameters reading"""
def raspb_pi_update_values():
    cpu_temp = subprocess.check_output('vcgencmd measure_temp', shell=True)
    sensor_data['cpu_tmp'] = float(str(cpu_temp)[7:11])
    # memory usage/ CPU usage of the R-PI as well
    # RX/TX and processing on BG96
    # looking for intergrated sensors as one part on chip
    # 2021-  features such as CPU Temperature/no of 
    # running processes/CPU and RAM utilization

""" Battery parameters reading - Try try: or asset or eval """
def battery_update_values():
    status = pijuice.status.GetStatus()
    key, value = next(iter(status.items()))
    if key != 'error':
        sensor_data['btr_lvl'] = pijuice.status.GetChargeLevel()['data']
        sensor_data['btr_vol'] = pijuice.status.GetBatteryVoltage()['data']
        sensor_data['btr_tmp'] = pijuice.status.GetBatteryTemperature()['data']
        sensor_data['hrs_sinc_chrg'] = 2    # env.variables from IFTT script
        sensor_data['chrg_cycl'] = '1'
        """ Battery methods to enable/disable charging """
        # pijuice.status.GetStatus()
        # pijuice.status.GetChargeLevel()
        # pijuice.status.GetFaultStatus()
        # pijuice.status.GetBatteryTemperature()
        # pijuice.status.GetChargeLevel()
    else: 
        sensor_data['btr_lvl'] = 90.0    # try None and check if postgres accepts it
        sensor_data['btr_vol'] = 30.0   # try None
        sensor_data['btr_tmp'] = 18.0    # try None
        sensor_data['hrs_sinc_chrg'] = 2     # try None
        sensor_data['chrg_cycl'] = '1'    # try None

def main():
    # data = ','.join(row)
    initialize_sensor_data()
    update_Telit_values()
    raspb_pi_update_values()
    battery_update_values()

iot_is_used = True
sensor_data = dict()
node = IoTMqtt()
node.setupGPIO()
no_of_iter = 3
i = 1

""" Telit is enabled by default (double check "ls /dev")- maybe assert """
# node.disable()
time.sleep(1)
# node.enable()
time.sleep(1)

if __name__ == "__main__":
    if iot_is_used:
        registered = False
        no_of_reg_loops = 50    # 50
        node_getOperator = node.sendATComm("AT#RFSTS","OK")     # the module should be up
        # if the sensor not registered, wait a few loops until register
        while (no_of_reg_loops > 1):
            if search('Amarisoft', node_getOperator):
                print("The sensor is registered with Amarisoft")
                registered = True
                break
            no_of_reg_loops -= 1
            print(f"waiting {50 - no_of_reg_loops} secs for registeration")
            sleep(10)
            node_getOperator = node.sendATComm("AT#RFSTS","OK")

        if registered:
            print("Check the PDP context")
            node.pdp_context_check_and_enable()
            print("Check MQTT is enabled")
            node.mqtt_check_and_enable()
            print("Check MQTT is open/connect")
            node.check_config_open_connect()

            while i <= no_of_iter:
                print(f"iteration number {i}")
                main()
                print(f"sensor_data is:\n {sensor_data}")
                # data_frame_json = json.dumps(sensor_data, indent=4)
                # node.mqtt_publish(data_frame_json)
                print("before node.mqtt_publish()")
                node.mqtt_publish()
                print("after node.mqtt_publish()")
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
                time.sleep(0.2)
            while not MessageReceived:
                time.sleep(0.2)
            client.loop_stop()
        else:
            while i <= no_of_iter:
                print(f"iteration number {i}")
                main()
                data_frame_json = json.dumps(sensor_data, indent=4)
                client.publish(client.topic, data_frame_json)
                # client.publish(topic,json.loads(str(row)))
                client.on_publish_message(data_frame_json)
                time.sleep(5)
                i += 1