''' 
Program: gdxst_raw_to_max.py
Author: Vincent Lacasse
Date: 2023-11-28

This program extract temperature in Celsius
from a Vernier GDX-ST sensor and sends it to MaxMSP via OSC

Installation
  Prior to running this program, some python module must be installed.
  On macOS, open a terminal and execute the following commands
  
  $ pip3 install godirect
  $ pip3 install python-osc
  
  Also, the running directory must contain the gdx/ directory 
  provided by Vernier.

To run the program
  
  $ python3 gdxst_raw_to_max.py
  
To receive data in MaxMSP

    - create a "udpreceive 7400" object
    - link its output to a message's input 

'''
import signal
import math
import time
from gdx import gdx
from pythonosc import udp_client


# The gdx object from Vernier allow communication with the GDX-ST sensor

gdx = gdx.gdx()     

# Open a connection with the sensor.
# connection = 'ble' for bluetooth (wireless)
# connection = 'usb' for usb (connection with a cable)
# Experience has shown that the USB connection is more reliable than Bluetooth.

gdx.open(connection='usb', device_to_open="GDX-ST 0P2016K2")  # 'usb' for usb, 'ble' for bluetooth
# gdx.select_sensors([2])     # measurement #1 is force in N, measurment #2 is respiration in bpm
gdx.select_sensors([1])     # measurement #1 is temperature on GDX-ST.  This is the only measurement.
gdx.start(100)              # measurement frequency 0.1 Hz (100 ms)

# Get sensor info and display it

column_headers= gdx.enabled_sensor_info()   # returns a string with sensor description and units
print('\n')
print(column_headers)

# The udp_client object allow communication with Max (using OSC)

ip = "127.0.0.1"    # loop back.  This script must be run on the same machine as MasMSP
port = 7400         # port to be used in the "updreceive" object in MaxMSP
client = udp_client.SimpleUDPClient(ip, port)

# Setup a clean-up function that will be called when CTRL_C is pressed. 

def cleanup(signum, frame):
    gdx.stop()
    gdx.close()
    quit()

# Pressing CTRL_C will execute cleanup() and exit the program

signal.signal(signal.SIGINT, cleanup)
print('Press CTRL-C to terminate loop')
time.sleep(1)

# Main loop

while True:
    value = gdx.read()[0]
    client.send_message("/temperature", value) 