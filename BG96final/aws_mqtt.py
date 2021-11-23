



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



class WifiMqtt(mqtt.Client):
    def __init__(self,
                 broker_address='9.162.161.90',
                 # broker_address='9.161.154.25',
                 # broker_address='34.241.236.160',
                 # broker_address='ec2-34-241-236-160.eu-west-1.compute.amazonaws.com',
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


def initialize_sensor_data():
    global sensor_data
    sensor_data = dict()
    millis = int(round(time.time() * 1000))
    sensor_data['timestamp'] = millis
    sensor_data['name'] = socket.gethostname()




def main():
    # data = ','.join(row)
    initialize_sensor_data()


iot_is_used = True
sensor_data = dict()
no_of_iter = 5
i = 1

if __name__ == "__main__":

    client = WifiMqtt(client_type='publisher')
    client.connect(client.broker_address, client.port, client.keepAlive)
    client.subscribe(client.topic)
    print(f"The subscriber just subscribed to topic {client.topic}")

    while i <= no_of_iter:
        print(f"iteration number {i}")
        main()
        data_frame_json = json.dumps(sensor_data, indent=4)
        client.publish(client.topic, data_frame_json)
        # client.publish(topic,json.loads(str(row)))
        client.on_publish_message(data_frame_json)
        time.sleep(5)
        i += 1
