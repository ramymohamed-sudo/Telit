


# https://www.digitalocean.com/community/tutorials/how-to-install-and-use-docker-on-ubuntu-18-04
#
# sudo apt update
#
# alpine vs Debian broker
#
# Docker in interactive mode
#
# sublime text editor
#
# For simplicity, install the broker on the host device
import paho.mqtt.client as mqtt
# from csv import writer
import csv
from time import sleep
import datetime
import json 

#1-client send CONNECT to the broker -2- ACK. The broker acknowledgement will generate a callback (on_connect). if rc=0, connection success 
def on_connect(pvtClient,userdata,flags,rc):
    print("** Connected to client! Return Code:"+str(rc)) # printing the data on the screen
    client.subscribe("$/SYS#")

def on_message(client, userdata,msg):
    print("** "+msg.topic+" "+str(msg.payload))

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
broker_address = '9.161.154.25' #"mqtt.eclipse.org"
client.connect(broker_address,1883,60)
topic = "MQTTsecondcode" 

with open('UC3.4_synthetic_kpis.csv',newline='') as csvfile:
    kpi_data_reader = csv.reader(csvfile,delimiter=',')
    next(kpi_data_reader)
    for row in kpi_data_reader:
        # current_time = datetime.datetime.strptime(row[1],'%Y-%m-%d %H:%M:%S')
        # delta = current_time - previous_time
        sleep(1)    # delta
        # previous_time = current_time
        client.publish(topic,','.join(row)) 
        # client.publish(topic,json.loads(str(row)))
        print(topic,','.join(row))


