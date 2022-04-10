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
currentRoomTemp, outsideTemp = None, None #initialize temp variables

# set up arduino
board = Arduino('/dev/ttyACM0') 
pin = board.get_pin('a:0:i')
it = util.Iterator(board)
it.start()

#initialize servo motor
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
pwm=GPIO.PWM(17, 50)
pwm.start(0)
#initialize blinder level values
bValPrev = -1
bVal = 0

#######initialize lin actuator
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
#initialize window level values
wValPrev = -1
wVal = 0

def ultrasonicW(): # Window Ultrasonic function
    TRIG, ECHO = 17, 27 
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    #time.sleep(0.2)
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
    #print("distance:", distance, "cm")
    return distance

def ultrasonicB():  # Blind Ultrasonic function
    TRIG, ECHO = 23, 24
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.setup(ECHO, GPIO.IN)
    GPIO.output(TRIG, False)
    #time.sleep(0.2)
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
    #print("distance:", distance, "cm")
    return distance

def lightSensor(): # light sensor measurement function
    # initialize light sensor
    import TSL2591
    lightSensor = TSL2591.TSL2591()
    T = 50 # threshold value
    
    if lightSensor.Lux > T:
        sunlight = True
        print('Lux: %d'%lightSensor.Lux)
        #print("Day time")
        lightSensor.TSL2591_SET_LuxInterrupt(50, 200)
    else:
        sunlight = False
        print('Lux: %d'%lightSensor.Lux)
        #print("Night time")
        lightSensor.TSL2591_SET_LuxInterrupt(50, 200)
    return sunlight


def Rain(): # Rain Sensor function
    analog_value = pin.read()
    while analog_value is None:
        analog_value = pin.read()
    T = 0.75 # Threshold value
    
    if analog_value > T:
        rain = False
    elif analog_value < T:
        rain = True
        
    return rain

def operateBlinders(valPrev, val): # operate Blinders Function
    distInterval = [74, 65.3, 58.6, 51.9, 45.2, 38.5, 31.8, 25.1, 18.4, 11.7, 5]
    dist = ultraSonicB()
    A, B = 6, 7 # Lin Actuator Pins on Arduino
    
    for i in range(11):
        if val == i and dist < (distInterval[i] - 2):
            board.digital[A].write(1)
            board.digital[B].write(0)
        elif val == i and dist > (distInterval[i] + 2):
            board.digital[A].write(0)
            board.digital[B].write(1)
        if val == i and dist > (distInterval[i] - 2) and dist < (distInterval[i] + 2):
            board.digital[A].write(1)
            board.digital[B].write(1)
            valPrev = val
            
    if valPrev == val:
        return val
    else: 
        return -1 # Can't return previous value
        
def operateWindow(valPrev, val): # operate window function
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
        return -1 # Can't return previous value
    
def Geofence():
    geofence = False
    cO = db.child("Settings").child("closeOption").get().val() #check if geofence is enabled
    
    if cO == False:
        geofence = True
    else:
        location = db.child("Geofence").get().val()
        for k, v in location.items(): #iterate through every user
            if v is True:
                geofence = True
    return geofence

def Temp(crt, ot): #retreive temp valies
    dRoomTemp = (db.child("Smart").child("temp").get()).val() # get desired room temp from app
    
    try:
        cRoomTemp = tempSensorIn.temperature # get temp reading from inside temp sensor
        outsideTemp = tempSensorOut.temperature # get temp reading from outside temp sensor
    except RuntimeError as error:
        cRoomTemp = crt
        outsideTemp = ot
    
    return dRoomTemp, cRoomTemp, outsideTemp
         
if __name__ == "__main__":
    while True:
        mode = db.child("SelectedMode").get().val() # get selected mode from app
        
        if mode == 1:
            print("Smart", mode)
            sunlight = lightSensor()
            desiredRoomTemp, currentRoomTemp, outsideTemp = Temp(currentRoomTemp, outsideTemp)
            
            if (currentRoomTemp > (desiredRoomTemp + 2)): #room is hotter than desired
                print("room is hotter")
                if (outsideTemp > (desiredRoomTemp + 2)):
                    print("outside is hotter")
                    print("closing window and blinds")
                    wVal = 10 #close windows
                    bVal = 10 # close blinds
                elif (outsideTemp < (desiredRoomTemp + 2)):
                    print("outside is colder/desired")
                    print("opening window and blinds")
                    
                    wVal = db.child("Settings").child("autoWindowsLevel").get().val()
                    bVal = db.child("Settings").child("autoBlindsLevel").get().val()
            elif (currentRoomTemp < (desiredRoomTemp + 2)): #room is colder or at desired
                wVal = 10 # close window to prevent heat from escaping home
                print("room is colder")
                if sunlight == True:
                    print("opening blinds bc sun")
                    bVal = db.child("Settings").child("autoBlindsLevel").get().val() # allow sunlight to heat home
                else:
                    print("closing blinds bc no sun")
                    bVal = 10 # close blinds
            
            #Rain Overide
            rain = Rain()
            print("rain: ", rain)
            if rain == True:
                print("closing window bc of rain")
                wVal = 10 # close windows
                    
        if mode == 2:
            print("Auto", mode)
            
            # Window Open Time
            wOpenHour = db.child("Automatic").child("Windows").child("wOpenHour").get().val()
            wOpenMinute = db.child("Automatic").child("Windows").child("wOpenMinute").get().val()
            print("Window Open Time: ", wOpenHour,":", wOpenMinute)
            wOpenTime = wOpenHour * 60 + wOpenMinute
            # Blinds Open Time
            bOpenHour = db.child("Automatic").child("Blinds").child("bOpenHour").get().val()
            bOpenMinute = db.child("Automatic").child("Blinds").child("bOpenMinute").get().val()
            print("Blinds Open Time: ", bOpenHour,":", bOpenMinute)
            bOpenTime = bOpenHour * 60 + bOpenMinute
            
            # Window Close Time
            wCloseHour = db.child("Automatic").child("Windows").child("wCloseHour").get().val()
            wCloseMinute = db.child("Automatic").child("Windows").child("wCloseMinute").get().val()
            print("Window Close Time: ", wCloseHour,":", wCloseMinute)
            wCloseTime = wCloseHour * 60 + wCloseMinute
            # Blinds Close Time
            bCloseHour = db.child("Automatic").child("Blinds").child("bCloseHour").get().val()
            bCloseMinute = db.child("Automatic").child("Blinds").child("bCloseMinute").get().val()
            print("Window Open Time: ", bCloseHour,":", bCloseMinute)
            bCloseTime = bCloseHour * 60 + bCloseMinute
            
            #current
            cH = datetime.now().hour  # Current Hour as an int
            cM = datetime.now().minute
            print("Current Time: ", cH,":", cM)
            currentTime = cH * 60 + cM
            
            #Auto window Val
            if wOpenTime < wCloseTime:
                if wOpenTime <= currentTime < wCloseTime:
                    print("Open Window")
                    wVal = db.child("Settings").child("autoWindowsLevel").get().val()
                else:
                    print("Close Window")
                    wVal = 10
            else:
                if currentTime >= wOpenTime or currentTime <= wCloseTime:
                    print("Open Window")
                    wVal = db.child("Settings").child("autoWindowsLevel").get().val()
                else:
                    print("Close Window")
                    wVal = 10
            #Auto Blind Val
            if bOpenTime < bCloseTime:
                if bOpenTime <= currentTime < bCloseTime:
                    print("Open Blinds")
                    bVal = db.child("Settings").child("autoBlindsLevel").get().val()
                else:
                    print("Close Blinds")
                    bVal = 10
            else:
                if currentTime >= bOpenTime or currentTime <= bCloseTime:
                    print("Open Blinds")
                    bVal = db.child("Settings").child("autoBlindsLevel").get().val()
                else:
                    print("Close Blinds")
                    bVal = 10

        if mode == 3:
            print("Manual", mode)
            wVal = db.child("Manual").child("windowsVal").get().val()
            bVal = db.child("Manual").child("blindsVal").get().val()
            
        #Geofence overide
        geofence = Geofence()
        if geofence == False:
            #print("closing window and blinds bc no one is home")
            wVal = 10
            bVal = 10
        
        if wVal != wValPrev: #adjust window if needed
            wValPrev = operateWindow(wValPrev, wVal)
            print("Previous Window Value: ", wValPrev)
            print("Current Window Value: ", wVal)
        if bVal != bValPrev: #adjust blinds if needed
            bValPrev = operateBlinders(bValPrev, bVal)
            print("Previous Blinders Value: ", bValPrev)
            print("Current Blinders Value: ", bVal)
