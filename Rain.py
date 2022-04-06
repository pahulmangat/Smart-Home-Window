# Rain
import RPi.GPIO as GPIO
import time
from pyrebase import pyrebase
from pyfirmata import Arduino, util

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

Rain = 4

board = Arduino('/dev/ttyACM0')

while True:
    isRain = board.digital[Rain].read
    print("Rain:",isRain)
    time.sleep(1)