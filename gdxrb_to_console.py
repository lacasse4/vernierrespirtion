''' 
gdxrb_to_console.py
author: Vincent Lacasse
date: 2023-04-28

This program extract respiration frequency in breath per minute from
a Vernier GDX-RB sensor, and shows data ton the console

Installation
  Prior to running this program, some python module must be installed.
  On macOS, open a terminal and execute the following commands
  
  $ pip3 install godirect
  
  Also, the running directory must contain the gdx/ directory 
  provided by Vernier.

To run the program
  
  $ python3 gdxrb_to_console.py

'''
import signal
import math
from gdx import gdx
gdx = gdx.gdx()

def cleanup(signum, frame):
    quit()
    
signal.signal(signal.SIGINT, cleanup)

gdx.open(connection='ble', device_to_open="GDX-RB 0K4000J6")  # 'usb' for usb, 'ble' for bluetooth
gdx.select_sensors([2])     # measurement #1 is force in N, measurment #2 is respiration in bpm
gdx.start(1000)             # measurement frequency 1 Hz (1000 ms)

#column_headers= gdx.enabled_sensor_info()   # returns a string with sensor description and units
#print('\n')
#print(column_headers)

gdx.read()[0]               # skip first measure which seems to be wrong sometimes

while True:
    value = gdx.read()[0]
    if math.isnan(value):   # value is return as NAN when invalid. This line remove NAN data points
        continue
    print(value)

gdx.stop()
gdx.close()
