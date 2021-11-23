


import sys
import IoTSixfab
from time import sleep
import socket
from re import search
import json


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

    def mqtt_publish(self):
        # AT+QMTPUB=<tcpconnectID>,<msgID>,<qos>,<retain>,"<topic>"
        # self.sendATComm("AT+QMTPUB=0,0,0,0,"+self.topic,">")
        self.sendATComm("AT+QMTPUB=0,0,0,0,\"5G-Solutions\"",">")
        print("Waiting 5 seconds before sending a message....")
        sleep(5)

        self.sensor_data = {"battery": 90.0}
        self.data_frame_json = json.dumps(self.sensor_data, indent=4)
        self.sendATComm(self.data_frame_json+self.CTRL_Z,"+QMTPUB: 0,0,0")

    def mqtt_close(self):
        # # AT+QMTCLOSE=<tcpconnectID>
        self.sendATComm("AT+QMTCLOSE=0","+QMTCLOSE: 0")


node = IoTMqtt()
""" The lines below should be uncommented for real scenarios"""
# node.setupGPIO()
# node.disable()
# sleep(5)
# node.enable()
# node.powerUp()
# sleep(5)


node_getOperator = node.sendATComm("AT+COPS?","OK\r\n")
if search('Amarisoft', node_getOperator):
    print("The sensor is registered with Amarisoft")
    
    # MQTT Connection
    # check the MQTT status
    node_mqtt_status = node.sendATComm("AT+QMTOPEN?","OK")
    while not (search(node.host_name, node_mqtt_status)):
        print("trying to open MQTT connection via mqtt_open() and mqtt_connect()")
        node.mqtt_open()
        sleep(10)
        print("mqtt_open() is passed")
        node.mqtt_connect()
        sleep(10)
        print("mqtt_connect() is passed")

        node_mqtt_status = node.sendATComm("AT+QMTOPEN?","OK")
        # break this loop after a few times and call node.sendATComm("AT+COPS?","OK\r\n")
        # and come to these steps again
    print("The MQTT connection is open")
    # node.mqtt_connect()
    node.mqtt_publish()
    # node.mqtt_close()
