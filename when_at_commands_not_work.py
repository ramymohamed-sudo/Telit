

import time
import serial
import RPi.GPIO as GPIO

TIMEOUT = 3
ser = serial.Serial()

BG96_ENABLE = 26
RELAY = 17
USER_BUTTON = 22
USER_LED = 27


GPIO.setmode(GPIO.BCM)

GPIO.setup(BG96_ENABLE, GPIO.OUT)
GPIO.setup(RELAY, GPIO.OUT)
GPIO.setup(USER_BUTTON, GPIO.IN)
GPIO.setup(USER_LED, GPIO.OUT)

# for enable
GPIO.output(BG96_ENABLE, 1)

# for disable
GPIO.output(BG96_ENABLE, 0)
