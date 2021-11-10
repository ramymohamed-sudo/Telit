

""" Please check band, mode (NB1/2/CAT0/auto) before any tshoot"""


import IoTSixfabTelit
from time import sleep
node = IoTSixfabTelit.IoT()

node.setupGPIO()    # channel is already in use
# node.enable()
# node.disable()
# node.getBandConfiguration()
print("Check the configured bandwidth")
node.sendATComm("AT#BND=?","OK")

# set LTE band to B3
node.sendATComm("AT#BND=0,0,4","OK")

# set NB-IoT mode page 161 
node.sendATComm("AT#WS46?","OK")
node.sendATComm("AT#WS46=1","OK")

# +CEREG: <mode>,<stat>[,[<tac>],[<ci>],[<AcT>]]
# mode to set to 1: enable the network registration unsolicited result code, and select the short format
node.sendATComm("AT+CEREG=2","OK")
node.sendATComm("AT+CEREG=2,2,\"0001\",\"01\",9","OK")      # gives error 

# Read command returns the current value of <mode>
node.sendATComm("AT+CEREG?","OK")   # 2, 2


# returns current service (Amarisoft Base Station if connected)
node.sendATComm("AT#RFSTS","OK")

SIM Field SPN
# node.sendATComm("AT#SPN","OK")    # did not work

# IMSI number 
node.sendATComm("AT#CIMI","OK")
node.sendATComm("AT+CIMI=?","OK") 
node.sendATComm("AT+CIMI","OK")




# SIM Status (page 90)
node.sendATComm("AT#QSS?","OK")
node.sendATComm("AT#QSS=2","OK")


# - Automatic Carrier Switch by SIM
node.sendATComm("AT#FWAUTOSIM?","OK")
node.sendATComm("AT#FWAUTOSIM=1","OK")


# PLMA and TAC - supported PLMNs - not needed 
# node.sendATComm("AT#PLMNUPDATE?","OK")      # the output is very lengthy


# Read command reports whether the currently used list of PLMN names is fixed or not, in the format:
node.sendATComm("AT#PLMNMODE?","OK")
# returns the supported range of values for parameter <mode>.
node.sendATComm("AT#PLMNMODE=?","OK")


# allows to update the PLMN from the following list
node.sendATComm("AT#PLMNMODE=2","OK")


# add Amarisoft to the list
node.sendATComm("AT#PLMNUPDATE=1,001,01,\"Amarisoft\"","OK")


# reboot 
node.sendATComm("AT#REBOOT","OK")


# mcc: 901 or 001
# mnc: 70  or 01 



AT#PLMNUPDATE[<action>,<MCC>,<MNC>[,<PLMNname>]]
# node.sendATComm("","OK")





""" ___________________ MQTT Configuration ___________________ """
# #MQEN: <instanceNumber>,<enabled>
node.sendATComm("AT#MQEN?","OK")
node.sendATComm("AT#MQEN=?","OK")
# - Enable MQTT Feature - instanceNumber=1
node.sendATComm("AT#MQEN=1,1","OK")


# - Configure MQTT   AT#MQCFG=<instanceNumber>,<hostname>,<port>,<cid>
node.sendATComm("AT#MQCFG=1,\"9.162.161.90\",1883,6","OK")  # the cid was 1 then made 6 
# gives range of values for port, cid, etc.
node.sendATComm("AT#MQCFG=?","OK")

# check the current configuration, e.g., hostname, port number, etc
node.sendATComm("AT#MQCFG?","OK") 


# reports the configuration of active MQTT connections
node.sendATComm("AT#MQCONN?","OK")
# Connect and Log in the MQTT Broker AT#MQCONN=<instanceNumber>,<clientID>,<userName>,<passWord>
node.sendATComm("AT#MQCONN=1,\"1\",\"userName\",\"passWord\"","OK")     # takes long time
# check again if it is connected
node.sendATComm("AT#MQCONN=?","OK")    # should return 1, 1


# AT#MQPUBS - Publish ASCII String
# Test command reports the available range of values for parameters
node.sendATComm("AT#MQPUBS=?","OK")
myMessage = 'hello'
# AT#MQPUBS=<instanceNumber>,<topic>,<retain>,<qos>,<message>
node.sendATComm("AT#MQPUBS=1,\"5G-Solutions\",0,0,\"hello\"","OK")

# node.sendATComm("","OK")


# Test command reports the available range of values for parameters.
node.sendATComm("AT#MQSUB=?","OK")
# Subscribe to a Topic AT#MQSUB=<instanceNumber>,<topic>
node.sendATComm("AT#MQSUB=1,\"5G-Solutions\"","OK")




AT+REBOOT

node.sendATComm("AT+CGATT?","OK")
node.sendATComm("AT+CGATT","OK")


# page 342 - network survey 
node.sendATComm("AT#CSURV","OK")


# page 379/382 AT+CGREG - GPRS Network Registration Status


# pages 155 - 157 - 163 (VIP)
 

# node.sendATComm("","OK")


# node.getBandConfiguration()

# node.setMode(node.CATNB1_MODE)
# sleep(1)
# node.setNBIoTBand(node.LTE_B3) - it seems that the band is set to auto
# sleep(1)
# node.getBandConfiguration()

# node.getQueryNetworkInfo()
# node.getNetworkRegStatus()
# node.connectToOperator()





# node.sendATComm("","OK")

#  returns the MSISDN (SIM Presence)
node.sendATComm("AT+CNUM=?","OK") 
