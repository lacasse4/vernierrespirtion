''' 
Program: gdxst_respiration.py
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
  
  $ python3 gdxst_respiration.py
  
'''
import time
import numpy as np
import peak as p

# define constants

SAMPLING_PERIOD = 100       # sensor sampling period in milliseconds
SIGNAL_LENGTH = 1024       # buffer size for Fast Fourrier Transfom
SAMPLES_PER_UNIT = (1000/SAMPLING_PERIOD ) / (SIGNAL_LENGTH)
LOWEST_BREATH_FREQ  = 12.0 / 60.0  # 12 BPM
HIGHEST_BREATH_FREQ = 20.0 / 60.0  # 20 BPM


# Main loop

temperature_data = np.empty([SIGNAL_LENGTH])
counter = 0
index = 0

start = time.time()

fft = np.fft.rfft(temperature_data)
spectrum = abs(fft)
spectrum[0] = 0.0  # Remove DC bias
peak = p.find_peak_with_unit(spectrum, LOWEST_BREATH_FREQ, HIGHEST_BREATH_FREQ, SAMPLES_PER_UNIT)

end = time.time()
print(end - start)

