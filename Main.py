#import libraries
from datetime import datetime #Date and time library
import time #time-related function library
import sys
import os
import board
import adafruit_dht

# initialize light sensor
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'Capstone')
if os.path.exists(libdir):
    sys.path.append(libdir)
import logging
import TSL2591
logging.basicConfig(level=logging.INFO)
lightSensor = TSL2591.TSL2591()
# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D4,use_pulseio=False)

blinderStatus = "Closed" #Blinders status flag
windowStatus = "Closed" #Blinds status flag

def Open_Blinders(): #open blinds function
    global blinderStatus
    if blinderStatus == "Closed":
        #motor code
        time.sleep(10)
        blinderStatus = "Open"
        print("Blinds are now", blinderStatus)
    elif blinderStatus == "Open":
        print("Blinds are already", blinderStatus)
        
def Close_Blinders(): #close blinds function
    global blinderStatus
    if blinderStatus == "Open":
        #motor code
        time.sleep(10)
        blinderStatus = "Closed"
        print("Blinds are now", blinderStatus)
    elif blinderStatus == "Closed":
        print("Blinds are already", blinderStatus)
        
def Open_Window(): #open windows function
    global windowStatus
    if windowStatus == "Closed":
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

    while mode == "Manual": #Manual Mode
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
        
    while mode == "Auto": #Auto Mode
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
        
    while mode == "Smart":
        print("Smart")
        badWeather = True
        noOneHome = False
        sunlight = False
        desiredRoomTemp = 23
        currentRoomTemp = dhtDevice.temperature
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
    #Mode = input("Mode: ")
    Mode = "Smart" #device mode flag
    while True:
        main(Mode)
