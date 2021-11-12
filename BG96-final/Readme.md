

<h1> Repoistory </h1>
>> git clone --filter=blob:none --sparse  https://github.com/ramymohamed-sudo/Telit-and-BG96.>> git sparse-checkout add resources/images/file.png
>> git sparse-checkout add resources/images/
# partial clone and sparse-checkout
>> git sparse-checkout set BG96-final/
>> git sparse-checkout init --cone

# sparse check-out
>> cd Telit-and-BG96
>> sudo python3 setup.py install

<h1> Install with pip3 <h1>
Use pip3 to install from PyPI.
>> sudo pip3 install sixfab-cellulariot


<h1> Test <h1>

<h2> Enable serial_hw and I2C interfaces by following instructions below: <h2>

Run sudo raspi-config
Select 5 Interfacing Options
Enable P5 I2C
For P6 Serial
Disable Login shell to be accessible over serial
Enable Serial port hardware
Finish
Reboot
It's done.

<h2> testing sensor_test example <h2>
cd sample
python3 sensor_test.py
