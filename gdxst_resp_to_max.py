''' 
Program: gdxst_resp_to_max.py
Author: Vincent Lacasse
Date: 2023-11-14

This program extract respiration frequency in breath per minute (bpm)
from a Vernier GDX-ST sensor and sends it to MaxMSP via OSC.

Installation
  Prior to running this program, some python module must be installed.
  On macOS, open a terminal and execute the following commands
  
  $ pip3 install godirect
  $ pip3 install numpy
  $ pip3 install python-osc
  
  Also, the running directory must contain the gdx/ directory 
  provided by Vernier.

To run the program
  
  $ python3 gdxst_resp_to_max.py

To receive data in MaxMSP

    - create a "udpreceive 7400" object
    - link its output to a message's input 

'''
import signal
import time
import numpy as np
import peak as p
from gdx import gdx
from pythonosc import udp_client

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

# Main loop

temperature_data = np.empty([SIGNAL_LENGTH])
counter = 0
index = 0

while True:
    value = -1.0
    
    # get next data point
    temperature_data[index] = gdx.read()[0]
    
    # temperature data points are put in the buffer in a wrap around fashion
    index += 1
    if index >= SIGNAL_LENGTH:
        index = 0
    
    # compute fft only if there are enough points in buffer
    if counter >= SIGNAL_LENGTH:
        fft = np.fft.rfft(temperature_data)
        spectrum = abs(fft)
        spectrum[0] = 0.0  # Remove DC bias
            
        peak = p.find_peak_with_unit(spectrum, LOWEST_BREATH_FREQ, HIGHEST_BREATH_FREQ, SAMPLES_PER_UNIT)
        if peak.position != -1:
            value = peak.scaled_position * 60;

    else:
        counter += 1

    # value is  either
    #   1) a valid positive value if a frequency between LOWEST_BREATH_FREQ and HIGHEST_BREATH_FREQ was found
    #   2) -1.0 if no valid frequency was found
    #   3) -1.0 if not enough data was gathered to compute a fft
    client.send_message("/frequency", value) 

    
cleanup(0, 0)
    