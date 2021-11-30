


# https://help.ifttt.com/hc/en-us/articles/115010230347-Webhooks-service-FAQ
# for the key https://maker.ifttt.com/use/7exmlYuXrRDcUqCFU5eap
# https://maker.ifttt.com/trigger/{event}/with/key/{webhooks_key}
# ./web_flask.py > auto-switch.log &


from flask import Flask
from flask import request
import requests
from time import sleep
import socket
import re

import sys
# sys.path.append('../')
import processor


""" Use Flask/Web to see the logs - current battery level and button stautus - while is working """ 
# app = Flask(__name__)

# @app.route('/')
# def hello_world():
#     return 'Hello from flask'

# @app.route('/ifttt', methods=['POST'])
# def handler():
#     username = request.get_data()
#     print(f"Got tweeted by {username}")
#     return "username: "


pload = {"value1": "", "value2": "", "value3": ""}
lower_threshold = 50.0
upper_threshold = 70.0
# name = sensor_data.sensor_data['na'] = socket.gethostname()   # name

url3_turn_on = 'https://maker.ifttt.com/trigger/cycle2-03-battery-low/with/key/7exmlYuXrRDcUqCFU5eap'
url4_turn_on = 'https://maker.ifttt.com/trigger/cycle2-04-battery-low/with/key/7exmlYuXrRDcUqCFU5eap'
url5_turn_on = 'https://maker.ifttt.com/trigger/cycle2-05-battery-low/with/key/7exmlYuXrRDcUqCFU5eap'
url6_turn_on = 'https://maker.ifttt.com/trigger/cycle2-06-battery-low/with/key/7exmlYuXrRDcUqCFU5eap'
url7_turn_on = 'https://maker.ifttt.com/trigger/cycle2-07-battery-low/with/key/7exmlYuXrRDcUqCFU5eap'
url8_turn_on = 'https://maker.ifttt.com/trigger/cycle2-08-battery-low/with/key/7exmlYuXrRDcUqCFU5eap'
url9_turn_on = 'https://maker.ifttt.com/trigger/cycle2-09-battery-low/with/key/7exmlYuXrRDcUqCFU5eap'
url10_turn_on = 'https://maker.ifttt.com/trigger/cycle2-10-battery-low/with/key/7exmlYuXrRDcUqCFU5eap'

url3_turn_off = 'https://maker.ifttt.com/trigger/cycle2-03-battery-high/with/key/7exmlYuXrRDcUqCFU5eap'
url4_turn_off = 'https://maker.ifttt.com/trigger/cycle2-04-battery-high/with/key/7exmlYuXrRDcUqCFU5eap'
url5_turn_off = 'https://maker.ifttt.com/trigger/cycle2-05-battery-high/with/key/7exmlYuXrRDcUqCFU5eap'
url6_turn_off = 'https://maker.ifttt.com/trigger/cycle2-06-battery-high/with/key/7exmlYuXrRDcUqCFU5eap'
url7_turn_off = 'https://maker.ifttt.com/trigger/cycle2-07-battery-high/with/key/7exmlYuXrRDcUqCFU5eap'
url8_turn_off = 'https://maker.ifttt.com/trigger/cycle2-08-battery-high/with/key/7exmlYuXrRDcUqCFU5eap'
url9_turn_off = 'https://maker.ifttt.com/trigger/cycle2-09-battery-high/with/key/7exmlYuXrRDcUqCFU5eap'
url10_turn_off = 'https://maker.ifttt.com/trigger/cycle2-10-battery-high/with/key/7exmlYuXrRDcUqCFU5eap'

urls_turn_on = [eval(f"url{i}_turn_on") for i in range(3, 11)]
urls_turn_off = [eval(f"url{i}_turn_off") for i in range(3, 11)]


name = socket.gethostname()
# sensor_id = re.findall(r'[\-]\d{2}',name)
sensor_id = [int(s) for s in name.split('-') if s.isdigit()][0]
print("sensor_id is: ", sensor_id)
# #sys.stdout.flush()()

url_turn_on = urls_turn_on[sensor_id-3]     # -3 as senors start cycle2-03
url_turn_off = urls_turn_off[sensor_id-3] 

print("url_turn_on", url_turn_on)
print("url_turn_off", url_turn_off)


sensor_data = processor.SensorData()
iter = 0

while (True):
    sensor_data.battery_update_values()
    sensor_data.charge_status

    if sensor_data.sensor_data['bl'] <= lower_threshold:

        if sensor_data.charge_status != 'PRESENT':
            print(f"the current LOW LOW battery level is {sensor_data.sensor_data['bl']}")
            #sys.stdout.flush()()
            r = requests.post(url_turn_on, data=pload)
            print(r.text)
            #sys.stdout.flush()()
        
    elif sensor_data.sensor_data['bl'] > upper_threshold:

        if sensor_data.charge_status == 'PRESENT':
            print(f"the current HIGH HIGH battery level is {sensor_data.sensor_data['bl']}")
            #sys.stdout.flush()()
            r = requests.post(url_turn_off, data=pload)
            print(r.text)
            #sys.stdout.flush()()

    print(f"Battery level now is {sensor_data.sensor_data['bl']} and charging status is {sensor_data.charge_status}")
    #sys.stdout.flush()()
    
    sleep(10)

    # add if condition to check if the switch is open/close or the battery is charging or not
