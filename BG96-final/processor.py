

# https://forums.raspberrypi.com/viewtopic.php?t=22180

import os
from pijuice import PiJuice
from time import sleep
import subprocess
import time
import os
import socket
from re import search
from processor import getCPUtemperature, getRAMinfo, getCPUuse, getDiskSpace


class SensorData():
    def __init__(self) -> None:
        self.sensor_data = dict()
        self.sensor_data['na'] = socket.gethostname()
    
    def timestamp(self):
        millis = int(round(time.time() * 1000))
        self.sensor_data['ts'] = millis

    # """ features such as no of running processes/ # Telit or BG96 """
    def cpu_temp_process_ram_utilization(self):
        self.sensor_data['cpt'] = float(self.getCPUtemperature())
        self.sensor_data['cpu'] = float(self.getCPUuse())
        self.sensor_data['ru'] = round(int(self.getRAMinfo()[1]) / 1000,1)
        self.sensor_data['dp'] = float(self.getDiskSpace()[3].replace("%", ""))    # getDiskSpace()[3]
        WiFi_ssd = str(subprocess.check_output('iwgetid', shell=True))
        if search(r'(HUAWEI|IBM)', WiFi_ssd):
            self.sensor_data['wf'] = True
        else:
            self.sensor_data['wf'] = False

    # """ BG96 parameters reading"""
    def update_BG_values(self):
        self.sensor_data['txp'] = 1.0       # ??
        self.sensor_data['iot'] = 'mode'    # ??

    # """ Battery parameters reading"""
    def battery_update_values(self):
        # use try/except here please
        status = pijuice.status.GetStatus()
        key, value = next(iter(status.items()))
        if key != 'error':
            self.sensor_data['bl'] = pijuice.status.GetChargeLevel()['data']
            self.sensor_data['bmv'] = pijuice.status.GetBatteryVoltage()['data']
            self.sensor_data['bt'] = pijuice.status.GetBatteryTemperature()['data']
            self.sensor_data['hsc'] = 2    # env.variables from IFTT script
            self.sensor_data['cc'] = '1'
            """ Battery methods to enable/disable charging """
            # pijuice.status.GetStatus()
            # pijuice.status.GetChargeLevel()
            # pijuice.status.GetFaultStatus()
            # pijuice.status.GetBatteryTemperature()
            # pijuice.status.GetChargeLevel()
        else: 
            self.sensor_data['bl'] = None
            self.sensor_data['bmv'] = None
            self.sensor_data['bt'] = None
            self.sensor_data['hsc'] = None
            self.sensor_data['cc'] = None

    # Return CPU temperature as a character string                                      
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

    # Return % of CPU used by user as a character string                                
    def getCPUuse(self):
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


    def sensor_data_for_AD(self):
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