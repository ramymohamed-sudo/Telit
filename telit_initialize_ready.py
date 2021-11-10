


import IoTSixfabTelit
from time import sleep
node = IoTSixfabTelit.IoT()

node.setupGPIO()

# set LTE band to B3
node.sendATComm("AT#BND=0,0,4","OK")
sleep(5)

# set NB-IoT mode page 161 
node.sendATComm("AT#WS46?","OK")
sleep(5)
node.sendATComm("AT#WS46=1","OK")
sleep(5)

# mode to set to 1: enable the network registration unsolicited result code, and select the short format
node.sendATComm("AT+CEREG=2","OK")
sleep(5)

# Read command returns the current value of <mode>
node.sendATComm("AT+CEREG?","OK")   # 2, 0 not 2, 2 ???????
sleep(5)

# returns current service (Amarisoft Base Station if connected - now Vodafone)
node.sendATComm("AT#RFSTS","OK")
sleep(5)
 
# check IMSI number 
node.sendATComm("AT#CIMI","OK")
sleep(5)

# - Automatic Carrier Switch by SIM
node.sendATComm("AT#FWAUTOSIM?","OK")
sleep(5)
node.sendATComm("AT#FWAUTOSIM=1","OK")
sleep(5)

# allows to update the PLMN from the following list
node.sendATComm("AT#PLMNMODE=2","OK")
sleep(10)

# add Amarisoft to the list
node.sendATComm("AT#PLMNUPDATE=1,001,01,\"Amarisoft\"","OK")
sleep(10)

# reboot 
node.sendATComm("AT#REBOOT","OK")