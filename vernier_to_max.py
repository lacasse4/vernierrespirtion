''' 
Program: breath_to_max.py
Author: Vincent Lacasse
Date: 2023-04-28

This program extract respiration frequency in breath per minute (bpm)
from a Vernier GDX-RB sensor and sends it to MaxMSP via OSC

Installation
  Prior to running this program, some python module must be installed.
  On OSX, open a terminal and execute the following commands
  
  $ pip3 install godirect
  $ pip3 install python-osc
  
  Also, the running directory must contain the gdx/ directory 
  provided by Vernier.

To run the program
  
  $ python3 breath_to_max.py

To receive data in MaxMSP

    - create a "udpreceive 7400" object
    - link its output to a message's input 
  
'''
import signal
import math
from gdx import gdx
from pythonosc import udp_client

gdx = gdx.gdx()     # the gdx class from Vernier allow communication with the GDX-RB sensor

ip = "127.0.0.1"    # loop back.  This script must be run on the same machine as MasMSP
port = 7400         # port to be used in the "updreceive" object in MaxMSP
client = udp_client.SimpleUDPClient(ip, port)

def cleanup(signum, frame):
    gdx.stop()
    gdx.close()
    quit()
    
signal.signal(signal.SIGINT, cleanup)  # pressing CTRL_C will execute cleanup() 

# open a connection with the sensor.
# connection = 'ble' for bluetooth (wireless)
# connection = 'usb' for usb (connection with a cable)
# experience has shown that the USB connection is more reliable than Bluetooth.
gdx.open(connection='ble', device_to_open="GDX-RB 0K4000J6")  # 'usb' for usb, 'ble' for bluetooth
gdx.select_sensors([2])     # measurement #1 is force in N, measurment #2 is respiration in bpm
gdx.start(1000)             # measurement frequency 1 Hz (1000 ms)

#column_headers= gdx.enabled_sensor_info()   # returns a string with sensor description and units
#print('\n')
#print(column_headers)

gdx.read()[0]               # skip first measure which seems to be wrong sometimes

while True:
    value = gdx.read()[0]
    if math.isnan(value):   # ignore nan
        continue
    client.send_message("/freq", value)