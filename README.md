# vernierrespiration

This repo holds few Python3 programs that interacts with Vernier sensors (https://www.vernier.com/).
Two sensors were used:
  - the Vernier Respiration Belt sensor (GDX-RB)
  - the Vernier Surface Temperature sensor (GDX-ST)
The main objective was to create simple programs that extract respiration frequency in breath per minute (bpm) from Vernier sensors and transmit this information to MaxMSP. Program were written in Python3. 

The following program can be found in this repo.
  - gdxrb_to_console: reads the Respiration Belt sensor and print respiration frequency in bpm to console
  - gdxrb_to_max: reads the Respiration Belt sensor and sends respiration frequency in bpm to MaxMSP
  - gdxst_raw_to_console: reads the Surface Temperature sensor and print temperature in C to console
  - gdxst_raw_to_max: reads the Surface Temperature sensor and sends tempreature in C to MaxMSP
  - gdxst_resp_to_console: reads the Surface Temperature sensor and print respiration frequency in bpm to console
  - gdxst_resp_to_max: reads the Surface Temperature sensor and sends respiration frequency in bpm to MaxMSP

Other programs contained in this repo were used as tests.

These programs use 2 external modules:
  Prior to running these program, some python module must be installed.
  On macOS, open a terminal and execute the following commands
  
  $ pip3 install godirect
  $ pip3 install python-osc
  
  Also, the running directory must contain the gdx/ directory 
  provided by Vernier.

To run the program
  
  Instructions on how to run each program have been placed as comments in the program code. 
  i.e. list the code of 'gdxrb_to_console.py' to see the instruction on how to run 'gdxrb_to_console.py'

  Typically, it is done with a command line as:
    $ python3 <program_name>.py

  The Vernier sensor must be connected via USB on the computer running the program.
  MaxMSP must be running on the machine were the Vernier sensor are conneted.

Setup in MaxMSPO receive data from these programs.

    - create a "udpreceive 7400" object
    - link its output to a message's input 
