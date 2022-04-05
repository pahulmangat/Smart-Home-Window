#import libraries
from datetime import datetime #Date and time library
import time #time-related function library
import sys
import os
import board
import RPi.GPIO as GPIO
import adafruit_dht
from pyrebase import pyrebase
from pyfirmata import Arduino, util

#initiaize firebase
config = {"apiKey": "AIzaSyDIx4wG2woFuKsk64nPpu7BnKE9CawnMDo",
  "authDomain": "smart-windows-app-edc8a.firebaseapp.com",
  "databaseURL": "https://smart-windows-app-edc8a-default-rtdb.firebaseio.com",
  "projectId": "smart-windows-app-edc8a",
  "storageBucket": "smart-windows-app-edc8a.appspot.com",
  "messagingSenderId": "1035393408535",
  "appId": "1:1035393408535:web:3a24ebae2282d1d7f40652",
  "measurementId": "G-CXZQXB2ZGV"}
firebase = pyrebase.initialize_app(config)
db = firebase.database() # Get a reference to the auth service

# Initial both temp sesnors
tempSensorIn = adafruit_dht.DHT22(board.D21,use_pulseio=False) #inside temp sensor
tempSensorOut = adafruit_dht.DHT22(board.D12,use_pulseio=False) #outside temp sensor

#initialize servo motor
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
pwm=GPIO.PWM(17, 50)
pwm.start(0)
bValPrev = -1
bVal = 0

#######initialize lin actuator
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
board = Arduino('/dev/ttyACM0')
wValPrev = -1
wVal = 0

def ultraSonicW():
    TRIG, ECHO = 17, 27 # Window Ultrasonic Pins on Raspi
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    time.sleep(0.2)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    pulse_start = 0
    pulse_end = 0
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    print("distance:", distance, "cm")
    return distance

def ultraSonicB():
    TRIG, ECHO = 23, 24 # Window Ultrasonic Pins on Raspi
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    time.sleep(0.2)
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)
    pulse_start = 0
    pulse_end = 0
    while GPIO.input(ECHO) == 0:
        pulse_start = time.time()
    while GPIO.input(ECHO) == 1:
        pulse_end = time.time()
    pulse_duration = pulse_end - pulse_start
    distance = pulse_duration * 17150
    distance = round(distance, 2)
    print("distance:", distance, "cm")
    return distance

def lightSensor():
    # initialize light sensor
    import TSL2591
    lightSensor = TSL2591.TSL2591()
    if lightSensor.Lux > 100:
        sunlight = True
        print('Lux: %d'%lightSensor.Lux)
        print("day")
        lightSensor.TSL2591_SET_LuxInterrupt(50, 200)
    else:
        sunlight = False
        print('Lux: %d'%lightSensor.Lux)
        print("night")
        lightSensor.TSL2591_SET_LuxInterrupt(50, 200)
    return sunlight

def operateBlinders(valPrev, val):
    distInterval = [72.5, 65, 57.5, 50, 42.5, 35, 27.5, 20, 12.5, 9, 7]
    dist = ultraSonicB()
    A, B = 6, 7 # Lin Actuator Pins on Arduino
    
    for i in range(11):
        if val == i and dist < (distInterval[i] - 5):
            board.digital[A].write(1)
            board.digital[B].write(0)
        elif val == i and dist > (distInterval[i] + 5):
            board.digital[A].write(0)
            board.digital[B].write(1)
        if val == i and dist > (distInterval[i] - 5) and dist < (distInterval[i] + 5):
            board.digital[A].write(1)
            board.digital[B].write(1)
            valPrev = val
            
    if valPrev == val:
        return val
    else: 
        return -1 # Can't return previous value because if user changes mind and sets to same value actuator nevers stops so return -1
        
def operateWindow(valPrev, val):
    distInterval = [9.0, 13.28, 17.56, 21.84, 26.12, 30.4, 34.68, 38.96, 43.24, 47.52, 51.5]
    dist = ultraSonicW()
    A, B = 8, 9 # Lin Actuator Pins on Arduino
    
    for i in range(11):
        if val == i and dist < (distInterval[i] - 0.25):
            board.digital[A].write(0)
            board.digital[B].write(1)
        elif val == i and dist > (distInterval[i] + 0.25):
            board.digital[A].write(1)
            board.digital[B].write(0)
        if val == i and dist > (distInterval[i] - 0.25) and dist < (distInterval[i] + 0.25):
            board.digital[A].write(1)
            board.digital[B].write(1)
            valPrev = val
            
    if valPrev == val:
        return val
    else: 
        return -1 # Can't return previous value because if user changes mind and sets to same value actuator nevers stops so return -1
         
if __name__ == "__main__":
    while True:
        mode = db.child("SelectedMode").get().val() # get selected mode from app
        
        if mode == 1:
            print("Smart", mode)
            sunlight = lightSensor()
            print ("sunlight: ", sunlight)
            sunlight = True
            desiredRoomTemp = (db.child("Smart").child("temp").get()).val() # get desired room temp from app
            #currentRoomTemp = tempSensorIn.temperature # get temp reading from inside temp sensor
            currentRoomTemp = 23
            #outsideTemp = tempSensorOut.temperature # get temp reading from outside temp sensor
            outsideTemp = 24
            print("desired room temp is: ", desiredRoomTemp)
            print("current room temp is: ", currentRoomTemp)
            print("outside room temp is: ", outsideTemp)
            
            if (currentRoomTemp > (desiredRoomTemp + 1)): #room is hotter than desired
                if (outsideTemp > (desiredRoomTemp - 1)):
                    print("yurrrr")
                    wVal = 0 #close windows
                    bVal = 10 # close blinds
                elif (outsideTemp < (desiredRoomTemp - 1)): 
                    wVal = db.child("Settings").child("autoWindowsLevel").get().val()
                    bVal = db.child("Settings").child("autoBlindsLevel").get().val()
            elif (currentRoomTemp < (desiredRoomTemp - 1)): #room is colder than desired
                wVal = 10 # close window to prevent heat from escaping home
                if sunlight == True:
                    bVal = db.child("Settings").child("autoBlindsLevel").get().val() # allow sunlight to heat home
                else:
                    bVal = 10 # close blinds
                    
        if mode == 2:
            print("Auto", mode)
            # Open Times
            wOpenHour = db.child("Automatic").child("Windows").child("wOpenHour").get().val()
            wOpenMinute = db.child("Automatic").child("Windows").child("wOpenMinute").get().val()
            print("wOpenTime: ", wOpenHour,":", wOpenMinute)
            wOpenTime = wOpenHour * 60 + wOpenMinute
            # Close Times
            wCloseHour = db.child("Automatic").child("Windows").child("wCloseHour").get().val()
            wCloseMinute = db.child("Automatic").child("Windows").child("wCloseMinute").get().val()
            print("wOpenTime: ", wCloseHour,":", wCloseMinute)
            wCloseTime = wCloseHour * 60 + wCloseMinute
            #current
            cH = datetime.now().hour  # Current Hour as an int
            cM = datetime.now().minute
            print("wOpenTime: ", cH,":", cM)
            currentTime = cH * 60 + cM
            
            if wOpenTime < wCloseTime:
                if wOpenTime <= currentTime < wCloseTime:
                    print("Open")
                    wVal = db.child("Settings").child("autoWindowsLevel").get().val()
                else:
                    print("Close")
                    wVal = 10
            else:
                if currentTime >= wOpenTime or currentTime <= wCloseTime:
                    print("Open")
                    wVal = db.child("Settings").child("autoWindowsLevel").get().val()
                else:
                    print("Close")
                    wVal = 10

        if mode == 3:
            print("Manual", mode)
            wVal = db.child("Manual").child("windowsVal").get().val()
            bVal = db.child("Manual").child("blindsVal").get().val()
                  
        if mode == 4:
            print("Test", mode)
            
        badWeather = False
        noOneHome = False 
        if (badWeather == True or noOneHome == True):
            print("closing window and blinds for safety")
            wVal = 10
            bVal = 10
        
        if wVal != wValPrev:
            wValPrev = operateWindow(wValPrev, wVal)
            print("Previous Window Value: ", wValPrev)
            print("Current Window Value: ", wVal)
        if bVal != bValPrev:
            bValPrev = operateBlinders(bValPrev, bVal)
            print("Previous Blinders Value: ", bValPrev)
            print("Current Blinders Value: ", bVal)
