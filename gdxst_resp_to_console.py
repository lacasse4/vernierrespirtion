''' 
Program: gdxst_resp_to_console.py
Author: Vincent Lacasse
Date: 2023-11-14

This program extract respiration frequency in breath per minute (bpm)
from a Vernier GDX-ST sensor and prints it to the console.

Installation
  Prior to running this program, some python module must be installed.
  On macOS, open a terminal and execute the following commands
  
  $ pip3 install godirect
  $ pip3 install numpy
  
  Also, the running directory must contain the gdx/ directory 
  provided by Vernier.

To run the program
  
  $ python3 gdxst_resp_to_console.py
  
'''
import signal
import time
import numpy as np
import peak as p
from gdx import gdx

# define constants

SAMPLING_PERIOD = 50        # sensor sampling period in milliseconds
SIGNAL_LENGTH = 256         # buffer size for Fast Fourrier Transfom
SAMPLES_PER_UNIT =  SIGNAL_LENGTH / (1000/SAMPLING_PERIOD)
LOWEST_BREATH_FREQ  = 4.0  / 60.0  
HIGHEST_BREATH_FREQ = 50.0 / 60.0 

# The gdx object from Vernier allow communication with the GDX-ST sensor
# connection = 'ble' for bluetooth (wireless)
# connection = 'usb' for usb (connection with a cable)
# Experience has shown that the USB connection is more reliable than Bluetooth.

gdx = gdx.gdx()     
gdx.open(connection='usb', device_to_open="GDX-ST 0P2016K2")
gdx.select_sensors([1])       # measurement #1 is temperature on GDX-ST.  This is the only measurement.
gdx.start(SAMPLING_PERIOD)    # start sensor with specified samplig period (in ms)


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

# Main loop

temperature_data = np.empty([SIGNAL_LENGTH])
counter = 0
index = 0

while True:
    # get next data point
    temperature_data[index] = gdx.read()[0]
        
    index += 1
    if index >= SIGNAL_LENGTH:
        index = 0
        
    if counter >= SIGNAL_LENGTH:
        fft = np.fft.rfft(temperature_data)
        spectrum = abs(fft)
        spectrum[0] = 0.0  # Remove DC bias
            
        peak = p.find_peak_with_unit(spectrum, LOWEST_BREATH_FREQ, HIGHEST_BREATH_FREQ, SAMPLES_PER_UNIT)
        if peak.position != -1:
            print("%5.2f" % (peak.scaled_position * 60), end = '')
            print("                      ", end='\r')
        else:
            print("no breath detected", end = '\r')
    else:
        counter += 1
        print("%4d building buffer..." % counter, end = '\r')
    
cleanup(0, 0)
    