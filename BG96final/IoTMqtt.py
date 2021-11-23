


import IoTSixfab
from time import sleep
import socket
from re import search


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
        # <tcpconnectID> QMTT socket identifier. The range is 0-5.
        # <clientID> The client identifier string.
        # <username> User name of the client. It can be used for authentication.
        # <password> Password corresponding to the user name of the client.

    def qmtt_open(self):
        # AT+QMTOPEN=<tcpconnectID>,"<host_name>"",<port>
        self.sendATComm(f"AT+QMTOPEN=0, {self.host_name}, {self.port}","+QMTOPEN: 0")         # OK
        # self.sendATComm("AT+QMTOPEN?","OK")    # +QMTOPEN: 0,"9.162.161.90",1883
        # self.sendATComm("AT+QMTCLOSE=0","\r\n")     # ?

    def qmtt_status(self):
        self.sendATComm("AT+QMTOPEN?","OK")

    def qmtt_connect(self):
        # AT+QMTCONN=<tcpconnectID>,"<clientID>"[,"<username>"[,"<password>"]]
        # self.sendATComm("AT+QMTCONN=0,\"sixfab\"","+QMTCONN: 0,0")      # this worked once
        self.sendATComm("AT+QMTCONN=0,\"sixfab\"","+QMTCONN: 0")    # this worked today 04/02

    def qmtt_publish(self):
        # AT+QMTPUB=<tcpconnectID>,<msgID>,<qos>,<retain>,"<topic>"
        # self.sendATComm("AT+QMTPUB=0,1,0,0,\"QMTTsecondcode\"","+QMTPUB: 0,1,0")
        self.sendATComm(f"AT+QMTPUB=0,0,0,0,{self.topic}",">")
        print("Waiting 5 seconds before sending a message....")
        sleep(5)
        self.sendATComm("Hello 2022"+self.CTRL_Z,"+QMTPUB: 0,0,0")

    def qmtt_close(self):
        # # AT+QMTCLOSE=<tcpconnectID>
        self.sendATComm("AT+QMTCLOSE=0","+QMTCLOSE: 0")






""" I need to study timeout wrtitten with self and then self.timeout
    I need also to check the return of each method and cmpare then do something like delay/try&except ...
    try and except and assert """

import IoTMqtt
from time import sleep
node = IoTMqtt.IoTMqtt()
node.qmtt_open()
node.qmtt_connect()
node.qmtt_publish()
node.qmtt_close()

import IoTSixfab
from time import sleep
node = IoTSixfab.IoT()
node.setupGPIO()
node.disable()
node.enable()
node.powerUp()




import IoTMqtt
from time import sleep
node = IoTMqtt.IoTMqtt()
node_getOperator = node.sendATComm("AT+COPS?","OK\r\n")
if not search('Amarisoft', node_getOperator):
    enable_disable_powerup()
    

# node.getIMEI()
# node.getSignalQuality()
# node.getQueryNetworkInfo()
# node.getNetworkRegStatus()
# # get operator node.getOperator()

node_getOperator = node.sendATComm("AT+COPS?","OK\r\n")
if search('Amarisoft', node_getOperator):
    print("Registered to Amarisoft Base Station!")
    # check the MQTT status
    node_qmtt_status = node.sendATComm("AT+QMTOPEN?","OK")
    if not search(node.host_name, node_qmtt_status):
        node.qmtt_open()
        node.qmtt_connect()

else:
    print("Not registered to a Base Station!")



node.qmtt_open()

node.qmtt_status()
while rsponse does not contain self.hostname or port:
    node.qmtt_open()
    print("still not connected")
    if after a few loops:
        disable the node
        sleep(1)
        enable the node
        sleep(1)
        setupGPIO
        powerUp
        sleep(5)

 print("!!! connected")


node.qmtt_connect()
node.qmtt_publish()
node.qmtt_close()


# Turn on cellular functionality
# AT+CFUN=1
#   Check the received signal strength
# AT+QCSQ
#   Query network registration status (0,1=Registered, on home network, 0,5=Registered, roaming) other - not connected
# AT+CEREG?
#   Query network technology and carrier:
# AT+COPS?

#################################################################################
#   Activate PDP context
# AT+QIACT=1

#   Confirm PDP context was activated
# AT+QIACT?

#   Configure QMTT session          # Configure Optional Parameters of QMTT
# AT+QMTCFG="aliauth",0
#################################################################################




#
