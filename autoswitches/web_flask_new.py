



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

print("The code is just started .......")
sys.stdout.flush()


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
# name = sensor_data.sensor_data['name'] = socket.gethostname()   # name
name = socket.gethostname()
# sensor_id = re.findall(r'[\-]\d{2}',name)
sensor_id = [int(s) for s in name.split('-') if s.isdigit()][0]
print("sensor_id is: ", sensor_id)
sys.stdout.flush()

sensor_data = processor.SensorData()
url_turn_on, url_turn_off =  sensor_data.get_on_off_urls(sensor_id)

iter = 0

while (True):
    sensor_data.battery_update_values()

    if sensor_data.sensor_data['batt_lvl'] <= sensor_data.lower_threshold:

        if sensor_data.charge_status != 'PRESENT':
            print(f"the current LOW LOW battery level is {sensor_data.sensor_data['batt_lvl']}")
            sys.stdout.flush()
            r = requests.post(url_turn_on, data=pload)
            print(r.text)
            sys.stdout.flush()
            sleep(10)
            

    elif sensor_data.sensor_data['batt_lvl'] > sensor_data.upper_threshold:

        if sensor_data.charge_status == 'PRESENT':
            print(f"the current HIGH HIGH battery level is {sensor_data.sensor_data['batt_lvl']}")
            sys.stdout.flush()
            r = requests.post(url_turn_off, data=pload)
            print(r.text)
            sys.stdout.flush()
            sleep(10)
            

    print(f"Battery level now is {sensor_data.sensor_data['batt_lvl']} and charging status is {sensor_data.charge_status}")
    #sys.stdout.flush()
    
    sleep(10)

    # add if condition to check if the switch is open/close or the battery is charging or not
