

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
                host_name= '9.162.161.90',
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
    
    def mqtt_check_and_enable(self):
        self.node_mqtt_check_enable = self.sendATComm("AT#MQEN?","OK")
        if not search('1,1', self.node_mqtt_check_enable):      # 1,1 and 2,1??
            print("Enable MQTT feature as it not enabled")
            self.sendATComm("AT#MQEN=1,1","OK")
        
    
    def pdp_context_check_and_enable(self):
        # Read command returns the current socket configuration parameters values for all the six sockets
        print("get the current socket configuration parameters values for all the six sockets")
        node.sendATComm("AT#SCFG?","OK")
        sleep(5)

        # Read command returns the current value of <mode>, the registration status <stat>
        self.reg_mode_stat = node.sendATComm("AT+CREG?","OK")    # returns 0,1 if mode-disable, registered
        if not (search('1,1', self.reg_mode_stat) or search('1,5', self.reg_mode_stat)):
            # AT+CEREG=[<mode>]
            node.sendATComm("AT+CREG=1","OK")  # enable the network registration unsolicited result code
            sleep(5)
            self.reg_mode_stat = node.sendATComm("AT+CREG?","OK") 
        
        if (search('1,1', self.reg_mode_stat) or search('1,5', self.reg_mode_stat)):
            # AT+CEREG=[<mode>] ; mode=1 enable the network registration unsolicited result code
            self.eps_reg_mode = node.sendATComm("AT+CEREG?","OK")     # returns <mode>, <EPS registration status stat>
            if not (search('1,1', self.eps_reg_mode) or search('1,5', self.eps_reg_mode)):
                node.sendATComm("AT+CEREG=1","OK")
                sleep(5)
                self.eps_reg_mode = node.sendATComm("AT+CEREG?","OK")
        
        if (search('1,1', self.eps_reg_mode) or search('1,5', self.eps_reg_mode)):
            self.gprs_reg_mode = node.sendATComm("AT+CGREG?","OK")      # AT+CGREG - GPRS Network Registration Status
            if not (search('1,1', self.gprs_reg_mode) or search('1,5', self.gprs_reg_mode)):
                sleep(5)
                node.sendATComm("AT+CGREG=1","OK")
                self.gprs_reg_mode = node.sendATComm("AT+CGREG?","OK") 

        if (search('1,1', self.gprs_reg_mode) or search('1,5', self.gprs_reg_mode)):
            # AT+CGDCONT - Define PDP Context
            node.sendATComm("AT+CGDCONT?","OK")     # returns 6 rows for context 1 to context 6
            sleep(5)
            """ check REG commands, 1,5 => 5 for HSUPA not LTE  """
            # get CID address
            self.cid_addr = node.sendATComm("AT+CGPADDR=1","OK")    # +CGPADDR: 1, "192.168.2.6"
            self.cid_addr = search(r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}', self.cid_addr).group()
            print("self.cid_addr", self.cid_addr)
            print("length of self.cid_addr", len(self.cid_addr))
            print("type of self.cid_addr", type(self.cid_addr))
            sleep(5)
            # AT+CGDCONT=[<cid>[,<PDP_type>[,<APN>[,<PDP_addr>
            # AT+CGDCONT=1,\"IP\",\"default\",\"192.168.2.6\",0,0
            node.sendATComm("AT+CGDCONT=1,\"IP\",\"default\","+str(self.cid_addr)+",0,0","OK")
            # node.sendATComm("AT+CGDCONT=1,\"IP\",\"default\",\"192.168.2.6\",0,0","OK")
            sleep(5)
            node.sendATComm("AT+CGDCONT?","OK")     # the first row is:1, "IP", "default", "192.168.2.6", 0,0,0,0
            # Read command returns the current activation state for all the defined PDP contexts in the format:
            node.sendATComm("AT+CGACT?","OK")   # CGACT:1,1     rest are 0s
            
            
        #     # page 338 - recall this is multiple time for context activation
        #     node.sendATComm("AT#SGACT?","OK")   # IPEasy Context Activation
        #     sleep(5)
        #     node.sendATComm("AT#SGACT=1,1","OK")
        #     sleep(5)
        # print("pdp_context_check_and_enable is finished")


    def mqtt_status(self):      # Telit Now
        # check the current configuration, e.g., hostname, port number, etc
        self.sendATComm("AT#MQCFG?","OK")

    def mqtt_open(self):    # Telit Now
        # - Configure MQTT   AT#MQCFG=<instanceNumber>,<hostname>,<port>,<cid>
        self.sendATComm("AT#MQCFG=1,\"9.162.161.90\",1883,1","OK") 
        
    def mqtt_connect(self):     # Telit Now
        # Connect and Log in the MQTT Broker AT#MQCONN=<instanceNumber>,<clientID>,<userName>,<passWord>
        self.sendATComm("AT#MQCONN=1,\"1\",\"userName\",\"passWord\"","OK")     # takes long time

    def check_config_open_connect(self):
        # Check the current configuration, e.g., hostname, port number, etc
        print("Check the current configuration, e.g., hostname, port number")
        mqtt_config_status = node.sendATComm("AT#MQCFG?","OK")
        while not (search(node.host_name, mqtt_config_status)):
            print("open the MQTT connection via mqtt_open()")
            node.mqtt_open()
            sleep(5)
            print("Connect MQTT via mqtt_connect()")
            node.mqtt_connect()
            sleep(10)
            mqtt_config_status = node.sendATComm("AT#MQCFG?","OK")
        sleep(5)
        
        mqtt_connect_status = node.sendATComm("AT#MQCONN?","OK")    # should return 1,1
        if search('1,1', mqtt_connect_status):
            print("The MQTT connection is now open and connected?")
        
    def mqtt_publish(self, message=None):
        print(f"Waiting {self.no_of_secs_before_send_msg} seconds before sending a message....")
        sleep(self.no_of_secs_before_send_msg)
        self.myMessage = "Hello 2025"
        # AT#MQPUBS=<instanceNumber>,<topic>,<retain>,<qos>,<message>
        node.sendATComm("AT#MQPUBS=1,\"5G-Solutions\",0,0,"+self.myMessage+self.CTRL_Z,"OK")
        # node.sendATComm("AT#MQPUBS=1,\"5G-Solutions\",0,0,\"Hello\""+node.CTRL_Z,"OK")

        # self.data_frame_json = message
        # self.sendATComm(self.data_frame_json+self.CTRL_Z,"+QMTPUB: 0,0,0")

    def mqtt_close(self):
        self.sendATComm("AT+QMTCLOSE=0","+QMTCLOSE: 0")

def initialize_sensor_data():
    global sensor_data
    sensor_data = dict()
    millis = int(round(time.time() * 1000))
    sensor_data['timestamp'] = millis
    sensor_data['name'] = socket.gethostname()


""" add features such as CPU Temperature/no of running processes/CPU 
and RAM utilization """
def cpu_temp_no_of_process_ram_utilization():
    pass

""" Telit parameters reading"""
def update_Telit_values():
    sensor_data['tx_pwr'] = 1.0
    sensor_data['nb_iot_mode'] = 'mode'
    # sensor_data['humidity'] = str(round(node.readHum(), 2))
    # sensor_data['temperature'] = str(round(node.readTemp(), 2))
    # sensor_data['light'] = light
    # sensor_data['acceleration_x'] = 0.0  
    # sensor_data['acceleration_y'] = 1.1  
    # sensor_data['acceleration_z'] = 2.2

""" Raspberry PI parameters reading"""
def raspb_pi_update_values():
    cpu_temp = subprocess.check_output('vcgencmd measure_temp', shell=True)
    sensor_data['cpu_temperature'] = float(str(cpu_temp)[7:11])
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
        sensor_data['battery_level'] = 90.0    # try None and check if postgres accepts it
        sensor_data['battery_milli_voltage'] = 30.0   # try None
        sensor_data['battery_temperature'] = 18.0    # try None
        sensor_data['hours_since_fully_charged'] = 2     # try None
        sensor_data['charge_cycle'] = '1'    # try None

def main():
    # data = ','.join(row)
    initialize_sensor_data()
    update_Telit_values()
    raspb_pi_update_values()
    battery_update_values()

iot_is_used = False
sensor_data = dict()
node = IoTMqtt()
node.setupGPIO()
no_of_iter = 5
i = 1

""" Telit is enabled by default (double check "ls /dev")- maybe assert """
# node.disable()
time.sleep(1)
# node.enable()
time.sleep(1)

if __name__ == "__main__":
    if iot_is_used:
        registered = False
        no_of_reg_loops = 50
        init_ctr = 0
        node_getOperator = node.sendATComm("AT#RFSTS","OK")     # the module should be up
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
            node_getOperator = node.sendATComm("AT#RFSTS","OK")

        if registered:
            print("Check the . PDP context")
            node.pdp_context_check_and_enable()
            print("Check MQTT Feature is enabled")
            node.mqtt_check_and_enable()
            node.check_config_open_connect()
            # reports the configuration of active MQTT connections
            check_connection = node.sendATComm("AT#MQCONN?","OK")
            if not (search('#MQCONN: 1,1', check_connection)):      # instance number is 1
                # Connect and Log in the MQTT Broker AT#MQCONN=<instanceNumber>,<clientID>,<userName>,<passWord>
                node.sendATComm("AT#MQCONN=1,\"1\",\"userName\",\"passWord\"","OK")     # takes long time
                print("I found the MQTT not connected at this stage")
            print("node.mqtt_connect() is checked connected")

            while i <= no_of_iter:
                print(f"iteration number {i}")
                # main()
                data_frame_json = json.dumps(sensor_data, indent=4)
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