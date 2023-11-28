''' 
Program: gdxst_raw_to_console.py
Author: Vincent Lacasse
Date: 2023-010-19

This program extract temperature in Celsius
from a Vernier GDX-ST sensor and prints it to the console

Installation
  Prior to running this program, some python module must be installed.
  On macOS, open a terminal and execute the following commands
  
  $ pip3 install godirect
  
  Also, the running directory must contain the gdx/ directory 
  provided by Vernier.

To run the program
  
  $ python3 gdxst_raw_to_console.py
  
'''
import signal
import math
import time
from gdx import gdx

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
    print(value) 