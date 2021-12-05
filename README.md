

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
https://docs.sixfab.com/page/setting-up-the-ppp-connection-for-sixfab-shield-hat

sudo systemd-escape stop serial­-getty@ttyS0.service
sudo systemd-escape start serial­-getty@ttyS0.service

sudo systemd-escape stop serial­-getty@ttyUSB0.service
sudo systemd-escape stop serial­-getty@ttyUSB1.service
sudo systemd-escape stop serial­-getty@ttyUSB2.service



 1224  cd 
 1225  ls
 1226  clear
 1227  ls
 1228  vim ppp_install_standalone.sh 
 1229  sudo pon
 1230  clear
 1231  cd Telit-and-BG96/
 1232  python
 1233  clear
 1234  sudo reboot
 1235  cd Telit-and-BG96/
 1236  clear
 1237  python
 1238  cd
 1239  ifconfig
 1240  ifconfig ppp0
 1241  clear
 1242  ifconfig ppp0
 1243  ifconfig
 1244  ping -I ppp0 -c 5 sixfab.com
 1245  ping
 1246  sudo systemctl status ppp_connection_manager.service 
 1247  ifconfig
 1248  clear
 1249  cd 
 1250  cd /etc/chatscripts
 1251  cd /etc
 1252  ls
 1253  sudo vim chatscripts/
 1254  clear
 1255  cd
 1256  git clone https://github.com/sixfab/Sixfab_PPP_Installer.git 
 1257  cd Sixfab_PPP_Installer 
 1258  chmod +x ppp_install.sh
 1259  sudo ./ppp_install.sh
 1260  ls
 1261  sudo ./ppp_install.sh
 1262  sudo pon
 1263  clear
 1264  cd Telit-and-BG96/
 1265  python cycle2_0x.py 
 1266  sudo reboot
 1267  clear
 1268  ls
 1269  cd Telit-and-BG96/
 1270  ifconfig
 1271  ifconfig ppp0
 1272  ping -I ppp0 -c 5 sixfab.com
 1273  ping -I ppp0 -c 5 192.168.2.1
 1274  clear
 1275  history



<br />
git clone https://github.com/sixfab/Sixfab_PPP_Installer.git 
 <br />
cd Sixfab_PPP_Installer 
  <br />
chmod +x ppp_install.sh
  <br />
sudo ./ppp_install.sh
  <br />
ps ax | grep ttyUSB
  <br />
sudo raspi-config 
  <br />
clear
  <br />
ls
  <br />
ifconfig
  <br />
ifconfig ppp0
  <br />
ping -I ppp0 -c 5 sixfab.com
  <br />
history

<br />
sudo ifconfig wlan0 up
sudo ifconfig wlan0 down
<br />
ip a show wlan0 up
<br />