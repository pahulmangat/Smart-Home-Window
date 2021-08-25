#import RPi.GPIO as GPIO #GPIO library
from datetime import datetime #Date and time library
import time #time-related function library

current_time = (datetime.now()).strftime("%H:%M:%S") #get current time

Blinds = "Closed" #Blinds status flag

#time variables
Waketime = "08:00:00" 
Bedtime = "20:00:00"
Sunrise = "08:00:00"
Sunset = "20:00:00"

def Open_Blinds(): #open blinds function
    global Blinds
    Blinds = "Open"
    print("Blinds are now", Blinds)
    
        
def Close_Blinds(): #close blinds function
    global Blinds
    Blinds = "Closed"
    print("Blinds are now", Blinds)
    
    
def loop(): #main loop
    while True:
        print("CURRENT TIME:", current_time)
        print("Blinds are currently", Blinds)
        if (Waketime < current_time < Bedtime) and (Blinds == "Closed"):
            Open_Blinds()
        if (current_time > Bedtime or current_time < Waketime) and (Blinds == "Open"):
            Close_Blinds()
        time.sleep(5)
            
loop()
    
