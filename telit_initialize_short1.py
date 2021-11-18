

""" Telit ME910C1-WW 
https://y1cj3stn5fbwhv73k0ipk1eg-wpengine.netdna-ssl.com/wp-content/uploads/2019/06/Telit_ME910C1_NE910C1_ML865C1_AT_Commands_Reference_Guide_r11.pdf

https://www.telit.com/wp-content/uploads/2018/10/Telit_ME910C1_NE910C1_ML865C1_AT_Commands_Reference_Guide_r4.pdf

"""

import IoTSixfabTelit
from time import sleep
import json
import socket
node = IoTSixfabTelit.IoT()
node.setupGPIO()  

# returns current service (Amarisoft Base Station if connected)
node.sendATComm("AT#RFSTS","OK")


""" ___________________ PDP Context Activation ____________________________ """
# Read command returns the current socket configuration parameters values for all the six sockets
node.sendATComm("AT#SCFG?","OK")

# Read command returns the current value of <mode>, the registration status <stat>  - # AT+CEREG=[<mode>]
node.sendATComm("AT+CREG?","OK")    # returns 0,1 if registered
node.sendATComm("AT+CREG=1","OK")  # enable the network registration unsolicited result code
node.sendATComm("AT+CREG?","OK")    # now returns 1,1 if registered

# AT+CEREG=[<mode>] ; mode=1 enable the network registration unsolicited result code
node.sendATComm("AT+CEREG?","OK")       # returns <mode>, <EPS registration status stat>
node.sendATComm("AT+CEREG=1","OK")
node.sendATComm("AT+CEREG?","OK") 


node.sendATComm("AT+CGREG?","OK")      # AT+CGREG - GPRS Network Registration Status
node.sendATComm("AT+CGREG=1","OK")
node.sendATComm("AT+CGREG?","OK")       # returns <mode>, the registration status <stat>


# AT+CGDCONT - Define PDP Context       - # check REG commands, 1,5 => 5 for HSUPA not LTE
node.sendATComm("AT+CGDCONT?","OK")     # returns 6 rows for context 1 to context 6
node.sendATComm("AT+CGPADDR=1","OK")    # # get CID address    +CGPADDR: 1, "192.168.2.6"
# AT+CGDCONT=[<cid>[,<PDP_type>[,<APN>[,<PDP_addr>
# AT+CGDCONT=1,\"IP\",\"default\",\"192.168.2.6\",0,0
node.sendATComm("AT+CGDCONT=1,\"IP\",\"default\",\"192.168.2.22\",0,0","OK")
node.sendATComm("AT+CGDCONT?","OK")     # the first row is:1, "IP", "default", "192.168.2.6", 0,0,0,0
node.sendATComm("AT+CGACT?","OK")   # # Read command returns the current activation state    CGACT:1,1     rest are 0s

# VIP page 338 - recall this is multiple time for context activation
node.sendATComm("AT#SGACT?","OK")   # IPEasy Context Activation
node.sendATComm("AT#SGACT=1,1","OK")    # only IF not 1,1
node.sendATComm("AT#SGACT?","OK")


""" ----------------------$$$$$$$$$$$$$$$$$$$$----------------------"""
# #MQEN: <instanceNumber>,<enabled>
node.sendATComm("AT#MQEN?","OK")        # enable it IF not 1,1 or 2,1
# - Enable MQTT Feature - instanceNumber=1 then 2
node.sendATComm("AT#MQEN=1,1","OK")    # if not 1,1

# Configure timeouts
#  AT#MQCFG2=<instanceNumber>,<keepAlive>,<cleanSession>
node.sendATComm("AT#MQCFG2=1,60,1","OK")
node.sendATComm("AT#MQCFG2?","OK")


# - Configure MQTT   AT#MQCFG=<instanceNumber>,<hostname>,<port>,<cid>
node.sendATComm("AT#MQCFG=1,\"9.162.161.90\",1883,1","OK")  # cid 1-6
# check the current configuration, e.g., hostname, port number, etc
node.sendATComm("AT#MQCFG?","OK") 
 
# reports the configuration of active MQTT connections
node.sendATComm("AT#MQCONN?","OK")      #  what I do if it is 1,2 - disable MQTT??


# Connect and Log in the MQTT Broker AT#MQCONN=<instanceNumber>,<clientID>,<userName>,<passWord>
name = socket.gethostname()
node.sendATComm("AT#MQCONN=1,\"05\",\"userName\",\"passWord\"","OK")
node.sendATComm(f"AT#MQCONN=1,\"{name}\",\"userName\",\"passWord\"","OK")

node.sendATComm("AT#MQCONN?","OK")    # should return 1, 1


node.sendATComm("AT#MQPUBS=1,\"5G-Solutions\",0,0,\"Hello 05\""+node.CTRL_Z,"OK")      # this works well 
sensor_data = {"ID": 12, "Battery": 90}
node.sendATComm(f"AT#MQPUBS=1,\"5G-Solutions\",0,0,\"{sensor_data}\""+node.CTRL_Z,"OK") # this also works well 

""" Subscribe to 5G-Solutions if needed """
# AT#MQSUB=<instanceNumber>,<topic>
node.sendATComm("AT#MQSUB=1,\"5G-Solutions\"","OK")
node.sendATComm("AT#MQSUB=2,\"5G-Solutions\"","OK")

# - Log Out and Disconnect from the MQTT Broker
# AT#MQDISC=<instanceNumber>
node.sendATComm("AT#MQDISC=1","OK")


# reboot 
node.sendATComm("AT#REBOOT","OK")


""" ___________________ PDP Context Activation ____________________________ """


# DNS resolve example
# AT#QDNS[=<host name>]
node.sendATComm("AT#QDNS=\"www.google.com\"","OK")
# 142.250.102.99

# Open socket 1 in online mode
# AT#SD=1,0,80,"www.google.com",0,0,0
node.sendATComm("AT#SD=1,0,80,\"142.250.102.99\",0,0,1,","OK")
# node.sendATComm("","OK")





node.sendATComm("AT#RFSTS=?","OK")












# Read command returns the current socket configuration parameters values for all the six sockets,
node.sendATComm("AT#SCFG?","OK")


node.sendATComm("AT#SD=?","OK")

node.sendATComm("AT#SD=1,0,80,\"142.250.102.99\",0,0,1,","OK")
node.sendATComm("AT#SD=1,0,80,\"www.google.com\",0,0,1,","OK")

# node.sendATComm("","OK")