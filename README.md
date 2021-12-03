

Step(01 - VNC):
After connecting the Raspberry-pi to the Internet and doing initial configuration:
>> Go to https://www.realvnc.com/en/connect/download/vnc/raspberrypi/ and download then install VNC
>> sudo nano /boot/config.txt # modify the lines as below
# uncomment to force a specific HDMI mode (this will force VGA)
#hdmi_group=1
#hdmi_mode=1
hdmi_ignore_edid=0xa5000080
hdmi_group=2
hdmi_mode=85
>> sudo reboot
>> sudo raspi-config # Interface options and enable VNC if it is not shown on top right 
# Install vim and ssh
>> sudo apt install openssh-server -y
>> sudo apt install vim -y
<br />
<br />
<br />


Step(02 - Setup and Read Battery):
>> sudo apt-get install pijuice-gui -y
>> sudo visudo
>> Add the following line: osmc ALL=(pijuice) ALL
>> sudo hostname cycle2-0X      # did not work >> sudo raspi-config >> System options >> hostname
>> sudo reboot
<br />
<br />
<br />


Step(03 - Install docker on sensor):
>> sudo apt-get update && sudo apt-get upgrade
>> sudo reboot  # this step is VIP
>> curl -sSL https://get.docker.com | sh
>> sudo usermod -aG docker ${USER}
>> echo ${USER}
>> groups ${USER}

# 4. Install Docker-Compose
>> vim install.sh
#!/bin/bash
sudo apt-get install libffi-dev libssl-dev
sudo apt install python3-dev
sudo apt-get install -y python3 python3-pip
sudo pip3 install docker-compose
sudo systemctl enable docker
pip3 install paho-mqtt python-etcd
>> chmod 755 install.sh
>> ./install.sh

5. Run Hello World Container
>> docker run hello-world
<br />
<br />
<br />


Step(1 - Telit):
# git clone --branch development https://github.com/ramymohamed-sudo/5G-Solutions.git Telit 
git clone https://github.com/ramymohamed-sudo/Telit-and-BG96.git 
<br />
Step(2):
cd Telit/
<br />
Step(3):
sudo python3 setup.py install
<br />
Step(4):
Either run the telit_initialize.py file to start the module
<br />
python3 telit_initialize_ready.py
<br />
<br />
or run the following commands in python
<br />
python3
<br />
import IoTSixfabTelit
<br />
from time import sleep
<br />
node = IoTSixfabTelit.IoT()
<br />
node.setupGPIO()   
<br /> 
node.enable()
<br />
print("Check the configured bandwidth")
<br />
node.sendATComm("AT#BND=?","OK")
<br />
node.disable()
<br />
<br />
<br />

VIP: for the mqtt codes and databases
In the python script for each sensor:
0- Install/configure the batteries (linux commands)
1- run the python code/method for the battery level, etc
2- change the sensors hostnames to pi01 to pi08
3- make use of these names (envirnoment variables when send data via the publisher code)
4- Once this is completed for one sensor - put everything on github and just use git clone


<br />
sudo update-alternatives --install /usr/bin/python python /usr/bin/python3 1
<br />
nohup python web_flask.py > switch.log &




https://sixfab.com/updated-tutorial-2-make-a-ppp-internet-connection-with-sixfab-gprs-shield-on-raspberry-pi/

sudo systemd-escape stop serial­-getty@ttyS0.service
sudo systemd-escape start serial­-getty@ttyS0.service

sudo systemd-escape stop serial­-getty@ttyUSB0.service
sudo systemd-escape stop serial­-getty@ttyUSB1.service
sudo systemd-escape stop serial­-getty@ttyUSB2.service