import pyrebase

config = {
  "apiKey": "AIzaSyDIx4wG2woFuKsk64nPpu7BnKE9CawnMDo",
  "authDomain": "smart-windows-app-edc8a.firebaseapp.com",
  "databaseURL": "https://smart-windows-app-edc8a-default-rtdb.firebaseio.com",
  "projectId": "smart-windows-app-edc8a",
  "storageBucket": "smart-windows-app-edc8a.appspot.com",
  "messagingSenderId": "1035393408535",
  "appId": "1:1035393408535:web:3a24ebae2282d1d7f40652",
  "measurementId": "G-CXZQXB2ZGV"
};

firebase = pyrebase.initialize_app(config)
# Get a reference to the auth service
db = firebase.database()

# Fetch temp and unit
temp = db.child("temp").get()
print(temp.key(),": ", temp.val()) # temp

unit = db.child("unit").get()
print(unit.key(),": ", unit.val()) # users
