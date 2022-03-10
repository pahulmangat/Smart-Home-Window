#import libraries
from datetime import datetime #Date and time library
import time #time-related function library
import sys
import os
import board
import RPi.GPIO as GPIO
import adafruit_dht
from pyrebase import pyrebase

#initiaize firebse
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

# initialize light sensor
import TSL2591
lightSensor = TSL2591.TSL2591()

# Initial both temp sesnors
tempSensorIn = adafruit_dht.DHT22(board.D4,use_pulseio=False) #inside temp sensor
tempSensorOut = adafruit_dht.DHT22(board.D5,use_pulseio=False) #outside temp sensor

#initialize servo motor
GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
pwm=GPIO.PWM(17, 50)
pwm.start(0)

blinderStatus = "Closed" #Blinders status flag
windowStatus = "Closed" #Blinds status flag

def Open_Blinders(): #open blinds function
    global blinderStatus
    if blinderStatus == "Closed":
        pwm.ChangeDutyCycle(5) # servo motor
        time.sleep(10)
        blinderStatus = "Open"
        print("Blinds are now", blinderStatus)
    elif blinderStatus == "Open":
        print("Blinds are already", blinderStatus)
        
def Close_Blinders(): #close blinds function
    global blinderStatus
    if blinderStatus == "Open":
        print("Closing Blinds...")
        pwm.ChangeDutyCycle(5) # servo motor
        time.sleep(10)
        blinderStatus = "Closed"
        print("Blinds are now", blinderStatus)
    elif blinderStatus == "Closed":
        print("Blinds are already", blinderStatus)
        
def Open_Window(): #open windows function
    global windowStatus
    if windowStatus == "Closed":
        print("Opening Blinds...")
        #motor code
        time.sleep(10)
        windowStatus = "Open"
        print("Windows are now", windowStatus)
    elif windowStatus == "Open":
        print("Windows are already", windowStatus)
    
        
def Close_Window(): #close windows function
    global windowStatus
    if windowStatus == "Open":
        #motor code
        time.sleep(10)
        windowStatus = "Closed"
        print("Windows are now", windowStatus)
    elif windowStatus == "Closed":
        print("Windows are already", windowStatus)

def main(mode): #main loop

    while mode == 3: #Manual Mode
        print("Manual")
        userInput = input("Enter your input: ")
        if userInput == "Open Window":
            Open_Window()
        if userInput == "Close Window":
            Close_Window()
        if userInput == "Open Blinds":
            Open_Blinders()
        if userInput == "Close Blinders":
            Close_Blinders()
        
        time.sleep(10)
        
    while mode == 2: #Auto Mode
        print("Auto")
        current_time = (datetime.now()).strftime("%H:%M") #get current time
        print("CURRENT TIME:", current_time)
        print("Blinds are currently", blinderStatus)
        print("Windows are currently", windowStatus)
        
        #openWindowTime = input("Enter Open Window Time: ")
        #closeWindowTime = input("Enter Close Window Time: ")
        #openBlindsTime = input("Enter Open Blinds Time: ")
        #closeBlindsTime = input("Enter Close Blinds Time: ")
        openWindowTime = "08:00"
        closeWindowTime = "20:00"
        openBlindsTime = "08:00"
        closeBlindsTime = "20:00"
        
        if (openWindowTime < current_time < closeWindowTime):
            Open_Window()
        if (current_time > closeWindowTime or current_time < openWindowTime):
            Close_Window()
        
        if (openBlindsTime < current_time < closeBlindsTime):
            Open_Blinders()
        if (current_time > closeBlindsTime or current_time < openBlindsTime):
            Close_Blinders()
            
        time.sleep(10)
        
    while mode == 1:
        print("Smart")
        badWeather = True
        noOneHome = False
        #get light sensor readings
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
        
        desiredRoomTemp = 23
        currentRoomTemp = tempSensorIn.temperature # get temp reading from inside temp sensor
        #outsideTemp = tempSensorOut.temperature # get temp reading from outside temp sensor
        outsideTemp = 23
        print("desired room temp is: ", desiredRoomTemp)
        print("current room temp is: ", currentRoomTemp)
        
        if currentRoomTemp > desiredRoomTemp:
            print("room is hotter")
            if outsideTemp > desiredRoomTemp:
                Close_Window()
                Close_Blinders()
                time.sleep(10)
            else:
                if badWeather == True or noOneHome == True:
                    Close_Window()
                    Close_Blinders()
                    time.sleep(10)
                else:
                    Open_Blinders()
                    Open_Window()
                    time.sleep(10)
        else:
            print("room is colder or at desired temperature")
            Close_Window()
            if sunlight == True:
                Open_Blinders()
                time.sleep(10)
            else:
                Close_Blinders()
                time.sleep(10)
    
if __name__ == "__main__":
    mode = (db.child("SelectedMode").get()).val() # get selected mode from app
    print("Mode: ", mode) 
    while True:
        main(mode)
