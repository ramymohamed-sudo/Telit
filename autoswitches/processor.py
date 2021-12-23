

# https://forums.raspberrypi.com/viewtopic.php?t=22180

import os
from pijuice import PiJuice
from time import sleep
import subprocess
import time
import os
import socket
from re import search
import requests


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
pload = {"value1": "", "value2": "", "value3": ""}

class SensorData():
    def __init__(self, name, model='Telit') -> None:
        self.sensor_data = dict()
        self.sensor_data['name'] = name
        self.pijuice = PiJuice(1, 0x14)
        self.model= model
        self.lower_threshold = 74.0
        self.upper_threshold = 77.0

        self.sensor_id = [int(s) for s in name.split('-') if s.isdigit()][0]
        self.SENSOR_READY = False
        self.urls_turn_on = [eval(f"url{i}_turn_on") for i in range(3, 11)]
        self.urls_turn_off = [eval(f"url{i}_turn_off") for i in range(3, 11)]
        self.url_turn_on = [eval(f"url{i}_turn_on") for i in range(3, 11)][self.sensor_id-3]
        self.url_turn_off = [eval(f"url{i}_turn_off") for i in range(3, 11)][self.sensor_id-3]
    
    def turn_switch_on(self):
        r = requests.post(self.url_turn_on, data=pload)

    def turn_switch_off(self):
        r = requests.post(self.url_turn_off, data=pload)
    
    def timestamp(self):
        millis = int(round(time.time() * 1000))
        if self.model == 'Telit':
            self.sensor_data['timestamp'] = millis  # timestamp
        else:
            self.sensor_data['timestamp'] = millis     # timestamp
    
    def start_cycle_timestamp(self):
        self.start_millis = int(round(time.time() * 1000))
    
    def ms_to_minutes_Hrs(self, crt_millis):
        ms = crt_millis - self.start_millis
        life_minut = ms/(1000*60)
        self.life_hrs = life_minut/60
        return life_minut/60

    # """ features such as no of running processes/ # Telit or BG96 """
    def cpu_temp_process_ram_utilization(self):
        self.sensor_data['cpu_temp'] = float(self.getCPUtemperature())   # cpu_temp
        self.sensor_data['cpu_util'] = float(self.getCPUuse())   # cpu_utliz
        self.sensor_data['ram_util'] = round(int(self.getRAMinfo()[1]) / 1000,1)  # ram_utliz
        self.sensor_data['disk_perc'] = float(self.getDiskSpace()[3].replace("%", ""))     # disk_percnt    # getDiskSpace()[3]
        # WiFi_ssd = str(subprocess.check_output('iwgetid', shell=True))
        WiFi_ssd = str(subprocess.check_output('ip a show wlan0 up', shell=True))
        if search(r'(HUAWEI|IBM)', WiFi_ssd):
            self.sensor_data['wifi'] = True
        else:
            self.sensor_data['wifi'] = False

    # """ BG96 parameters reading"""
    def update_BG_values(self):
        self.sensor_data['tx_pwr'] = 1.0       # tx_pwr
        self.sensor_data['iot_mode'] = 'm'    # iot_mode
    
    # """ BG96 parameters reading"""
    def update_Telit_values(self):
        self.sensor_data['tx_pwr'] = 1.0       # ??
        self.sensor_data['iot_mode'] = 'm'    # ??

    # """ Battery parameters reading"""
    def battery_update_values(self):
        status = self.pijuice.status.GetStatus()
        key, value = next(iter(status.items()))
        # try:
        self.sensor_data['batt_lvl'] = self.pijuice.status.GetChargeLevel()['data']
        self.sensor_data['batt_mv'] = self.pijuice.status.GetBatteryVoltage()['data']
        self.sensor_data['batt_tmp'] = self.pijuice.status.GetBatteryTemperature()['data']
        crt_millis = int(round(time.time() * 1000))
        self.sensor_data['hrs_since_ful_chrg'] = self.ms_to_minutes_Hrs(crt_millis)
        self.sensor_data['chrg_cycls'] = '1'

        """ Battery methods to enable/disable charging """
        # self.pijuice.status.GetStatus()
        self.charge_status_ = self.pijuice.status.GetStatus()['data']['powerInput']
        self.charge_status_5VIO = self.pijuice.status.GetStatus()['data']['powerInput5vIo']
        
        if (self.charge_status_ != 'PRESENT') and (self.charge_status_5VIO != 'PRESENT'):
            self.charge_status = 'NOT_PRESENT'
        
        elif (self.charge_status_ == 'PRESENT') or (self.charge_status_5VIO == 'PRESENT'):
            self.charge_status = 'PRESENT'
        
        self.sensor_data['chrg_status'] = self.charge_status
            
            # {'data': {'isFault': True, 'isButton': False, 'battery': 'NORMAL', 
            # 'powerInput': 'NOT_PRESENT', 'powerInput5vIo': 'NOT_PRESENT'}, 'error': 'NO_ERROR'}

            # self.pijuice.status.GetChargeLevel()
            # self.pijuice.status.GetFaultStatus()
            # self.pijuice.status.GetBatteryTemperature()
            # self.pijuice.status.GetChargeLevel()
        # except:
        #     print(f"There is error related to battery:\n {key}")
    
    def prepare_for_data_collect(self):
        self.battery_update_values()
        if self.charge_status == 'PRESENT':
            if self.sensor_data['batt_lvl'] > self.upper_threshold:
                self.SENSOR_READY = True
            else:
                pass
                # leave the sensor charges till exceeds upper_threshold
        elif self.charge_status == 'NOT_PRESENT':
            self.turn_switch_on()
        else:
            print("Wiating for the sensor to be ready ......")
        print(f"Battery level now is {self.sensor_data['batt_lvl']} and charging status is {self.charge_status}")
        # if self.sensor_data['batt_lvl'] > self.lower_threshold:
        # return self.SENSOR_READY
        # cases
        # 
        # return True when ready

    def getCPUtemperature(self):
        res = os.popen('vcgencmd measure_temp').readline()
        return(res.replace("temp=","").replace("'C\n",""))

    # Return RAM information (unit=kb) in a list                                        
    # Index 0: total RAM                                                                
    # Index 1: used RAM                                                                 
    # Index 2: free RAM                                                                 
    def getRAMinfo(self):
        p = os.popen('free')
        i = 0
        while 1:
            i = i + 1
            line = p.readline()
            if i==2:
                return(line.split()[1:4])
                            
    def getCPUuse(self):    # Return % of CPU used by user as a character string    
        return(str(os.popen("top -n1 | awk '/Cpu\(s\):/ {print $2}'").readline().strip(\
    )))

    # Return information about disk space as a list (unit included)                     
    # Index 0: total disk space                                                         
    # Index 1: used disk space                                                          
    # Index 2: remaining disk space                                                     
    # Index 3: percentage of disk used                                                  
    def getDiskSpace(self):
        p = os.popen("df -h /")
        i = 0
        while 1:
            i = i +1
            line = p.readline()
            if i==2:
                return(line.split()[1:5])


    def sensor_data_for_anom_detect(self):
        pass
        # self.sensor_data['humidity'] = str(round(node.readHum(), 2))
        # self.sensor_data['temperature'] = str(round(node.readTemp(), 2))
        # self.sensor_data['light'] = light
        # self.sensor_data['acceleration_x'] = 0.0  # str(node.readAccel())[0]
        # self.sensor_data['acceleration_y'] = 1.1  # str(node.readAccel())[1]
        # self.sensor_data['acceleration_z'] = 2.2  # str(node.readAccel())[2]
        # self.sensor_data['adc0'] = str(node.readAdc(0))
        # self.sensor_data['adc1'] = str(node.readAdc(1))
        # self.sensor_data['adc2'] = str(node.readAdc(2))
        # self.sensor_data['adc3'] = str(node.readAdc(3))

    def to_json(self):
        pass


"""json.dumps(sensor_data, indent=4) """ 
""" some static/class methods please """ 