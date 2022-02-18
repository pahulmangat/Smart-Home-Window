from pyrebase import pyrebase

config = {"apiKey": "AIzaSyDIx4wG2woFuKsk64nPpu7BnKE9CawnMDo",
  "authDomain": "smart-windows-app-edc8a.firebaseapp.com",
  "databaseURL": "https://smart-windows-app-edc8a-default-rtdb.firebaseio.com",
  "projectId": "smart-windows-app-edc8a",
  "storageBucket": "smart-windows-app-edc8a.appspot.com",
  "messagingSenderId": "1035393408535",
  "appId": "1:1035393408535:web:3a24ebae2282d1d7f40652",
  "measurementId": "G-CXZQXB2ZGV"}

firebase = pyrebase.initialize_app(config)
# Get a reference to the auth service
db = firebase.database()

# Fetch
# Mode
mode = db.child("SelectedMode").get()
print(mode.key(),": ", mode.val()) 

#Smart
temp = db.child("Smart").child("temp").get()
print(temp.key(),": ", temp.val()) 

unit = db.child("Smart").child("unit").get()
print(unit.key(),": ", unit.val()) 

#Manual
blindsVal = db.child("Manual").child("blindsVal").get()
print(blindsVal.key(),": ", blindsVal.val()) 

windowsVal = db.child("Manual").child("windowsVal").get()
print(windowsVal.key(),": ", windowsVal.val()) 

#Automatic

#Blinds
#Open
bOpenHour = db.child("Automatic").child("Blinds").child("bOpenHour").get()
bOpenMinute = db.child("Automatic").child("Blinds").child("bOpenMinute").get()
print("Blinds Open Time: ",bOpenHour.val(),":", bOpenMinute.val())

#Close
bCloseHour = db.child("Automatic").child("Blinds").child("bCloseHour").get()
bCloseMinute = db.child("Automatic").child("Blinds").child("bCloseMinute").get()
print("Blinds Close Time: ",bCloseHour.val(),":", bCloseMinute.val())

#Windows
#Open
wOpenHour = db.child("Automatic").child("Windows").child("wOpenHour").get()
wOpenMinute = db.child("Automatic").child("Windows").child("wOpenMinute").get()
print("Windows Open Time: ",wOpenHour.val(),":", wOpenMinute.val())

#Close
wCloseHour = db.child("Automatic").child("Windows").child("wCloseHour").get()
wCloseMinute = db.child("Automatic").child("Windows").child("wCloseMinute").get()
print("Windows Close Time: ",wCloseHour.val(),":", wCloseMinute.val())

