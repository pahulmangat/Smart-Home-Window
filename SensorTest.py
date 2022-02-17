#import libraries
import time
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
# sensor.SET_InterruptThreshold(0xff00, 0x0010)

# Initial the dht device, with data pin connected to:
dhtDevice = adafruit_dht.DHT22(board.D5,use_pulseio=False)

while True:
    try:
        #print light sensor readings
        lux = sensor.Lux
        print('Lux: %d'%lux)
        lightSensor.TSL2591_SET_LuxInterrupt(50, 200)
        infrared = lightSensor.Read_Infrared
        print('Infrared light: %d'%infrared)
        visible = lightSensor.Read_Visible
        print('Visible light: %d'%visible)
        full_spectrum = lightSensor.Read_FullSpectrum
        print('Full spectrum (IR + visible) light: %d\r\n'%full_spectrum)
        
        #print temp sensor readings
        temperature_c = dhtDevice.temperature
        temperature_f = temperature_c * (9 / 5) + 32
        humidity = dhtDevice.humidity
        print(
            "Temp: {:.1f} F / {:.1f} C    Humidity: {}% ".format(
                temperature_f, temperature_c, humidity
            )
        ) 
    except KeyboardInterrupt:    
        logging.info("ctrl + c:")
        sensor.Disable()
        exit()
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print(error.args[0])
        time.sleep(2.0)
        continue
    except Exception as error:
        dhtDevice.exit()
        raise error

    time.sleep(2.0)
