

""" This code is based on Sixfab basic HAT and Telit module and Pijuice HAT 
No built-in sensors witht the Sixfab HAT - 
Remember for Pijuice HAT, there was a function to stop the battery from being charged (if needed)
"""

# import BG96final.processor as processor
import autoswitches.processor as processor
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
import requests
from re import search
import itertools
import string
from collections import defaultdict


connected = False
MessageReceived = False


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
            print("WifiMqtt is attached to the broker .....")
            print("\n")
            global connected
            connected = True
            # client.subscribe(topic)
        else:
            print("WifiMqtt is not attached")

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
            print("The MQTT connection is now open and attached")

        elif search('#MQCONN: 1,2', mqtt_connect_status):
            print("Please restart the module and exit code as connection status is 2")
            self.sendATComm("AT#REBOOT","OK")
            sys.exit()
        else:
            print("The MQTT connection is not open - please DEBUG this manually")
            self.sendATComm("AT#MQCONN?","OK") 
            sys.exit()


    def mqtt_publish(self, data=None):
        print(f"Waiting {self.secs_befr_send} seconds before sending sensor data....")
        sleep(self.secs_befr_send)

        all_keys_sent = {}
        message = True
        while message:
            sensor_data_truncated = {key: val for (key, val) in data.items()
                                    if key not in all_keys_sent.keys()}
            if len(sensor_data_truncated) == 0:
                message = False
                print(f"message is {message}")
            else:
                for k in range(len(sensor_data_truncated) + 1):
                    new_sensor_data = dict(itertools.islice(sensor_data_truncated.items(), k))  # noqa
                    data_frame_json = json.dumps(new_sensor_data, indent=4)
                    if len(data_frame_json) > 120:
                        break
                print(f"Message is being sent; length of the truncated message is {len(data_frame_json)}")     # noqa
                self.sendATComm(f"AT#MQPUBS=1,\"5G-Solutions\",0,0,\"{new_sensor_data}\""+self.CTRL_Z,"OK") # this also works well 
                # self.sendATComm(self.data_frame_json+self.CTRL_Z,"+QMTPUB: 0,0,0")
                sleep(0.5)
            all_keys_sent.update(new_sensor_data)
        print("The while loop is just exited!!!!!!")

    def mqtt_close(self):
        self.sendATComm("AT#MQDISC=1","OK")
    
    def subs_topic(self):
        self.sendATComm("AT#MQSUB=1,\"5G-Solutions\"","OK")

def main():
    sensor_data.reset_sensor_data()
    sensor_data.timestamp()
    sensor_data.update_Telit_values()
    sensor_data.cpu_temp_process_ram_utilization()
    sensor_data.battery_update_values()


iot_is_used = False
node = IoTMqtt()
node.setupGPIO()
no_of_iter = 3
i = 1
name = socket.gethostname()
""" Telit is enabled by default (double check "ls /dev")- maybe assert """
if iot_is_used:
    # node.disable()
    sleep(1)
    # node.enable()
    sleep(1)

if __name__ == "__main__":
    sensor_data = processor.SensorData(name)

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
                data_frame = sensor_data.sensor_data
                data_frame_json = data_frame   # json.dumps(sensor_data.sensor_data, indent=4) 
                print(f"sensor_data is:\n {data_frame_json}")
                node.mqtt_publish(data=data_frame_json)
                print("after node.mqtt_publish()")
                # node.mqtt_close()
                sleep(1)
                i += 1

    else:
        client = WifiMqtt(client_type='publisher')
        client.connect(client.broker_address, client.port, client.keepAlive)
        client.subscribe(client.topic)
        print(f"The subscriber just subscribed to topic {client.topic}")

        for chrg_cycls in range(4):
            print(f"chrg_cycls: {chrg_cycls+1}")
            print("sensor_data.SENSOR_READY before", sensor_data.SENSOR_READY)

            while sensor_data.SENSOR_READY == False:
                sensor_data.prepare_for_data_collect()
                sleep(10)
            sensor_data.battery_update_values()

            if (sensor_data.sensor_data['batt_lvl'] >= sensor_data.upper_threshold) and (sensor_data.charge_status == 'PRESENT'):
                sensor_data.turn_switch_off()
                while sensor_data.charge_status == 'PRESENT':
                    sleep(5)
                    sensor_data.battery_update_values()
                    
                    print("waiting for the charger to be disconnected")

                print(f"A new charging cycle is just started: {chrg_cycls+1}")
                sensor_data.start_cycle_timestamp()

                while (sensor_data.sensor_data['batt_lvl'] >= sensor_data.lower_threshold) and (sensor_data.charge_status != 'PRESENT'):     # i <= no_of_iter
                    print(f"cycle number {chrg_cycls+1} and iteration number {i}")
                    main()
                    data_frame = sensor_data.sensor_data
                    data_frame['chrg_cycls'] = chrg_cycls+1
                    data_frame_json = json.dumps(data_frame, indent=4)
                    client.publish(client.topic, data_frame_json)
                    client.on_publish_message(data_frame_json)
                    sleep(10)
                    i += 1
                
                if (sensor_data.sensor_data['batt_lvl'] <= sensor_data.lower_threshold) and (sensor_data.charge_status != 'PRESENT'):
                    print(f"The charging cycle number {chrg_cycls+1} is just ended")
                    sensor_data.SENSOR_READY == False
                    print("sensor_data.SENSOR_READY after", sensor_data.SENSOR_READY)
                    sleep(10)
                else:
                    print("The loop cycle no. {chrg_cycls+1} did not complete!!!")
                    sys.exit()

                    

                



