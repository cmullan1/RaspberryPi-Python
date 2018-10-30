# CPRG 220 Python Raspberry Pi Assignment
# Author:  Corinne Mullan
# Date:    October 7, 2018
#
# This program reads the data from the digital temperature sensor that
# is located in /sys/bus/w1/devices/28-02089245c022/w1_slave.  If the
# temperature is less than 15 degrees C, the RGB LED is set to blue.
# If the temperature is between 15 and 30 degrees C, the LED is set to
# green.  If the temperature is greater than 30 degrees C, the LED is set
# to red.  The temperature is also output to the screen.

#!/usr/bin/python3

import os
import glob
import re
import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BOARD)
RED_LED = 16
GREEN_LED = 18
BLUE_LED = 22

GPIO.setup(RED_LED, GPIO.OUT)
GPIO.setup(GREEN_LED, GPIO.OUT)
GPIO.setup(BLUE_LED, GPIO.OUT)

os.system("modprobe w1-gpio")
os.system("modprobe w1-therm")
base_dir = ("/sys/bus/w1/devices/")

# Get the first element in the array returned by the glob method.
# This will be the first (here, only) directory name starting with "28-".
# The w1_slave file with the temperature readings is located in this directory.
folder = glob.glob(base_dir + "28-*")[0]
file = folder + "/w1_slave"

def loop():
    # Open the file containing the temperature sensor data
    f = open(file, "r")
    lines = f.readlines()
    f.close()

    # Search for the temperature reading (at the end of the second line in the
    # format t=nnnnn) in the w1_slave file.
    # Divide by 1000 to get the temperature in degrees C
    match = re.search("t=(\d+)", lines[1])
    return float(match.group(1)) / 1000

if __name__ == "__main__":
    try:
        print("Ctrl-C to exit")
        while True:
            temp_reading = loop()
            print("Temperature = " + str(temp_reading) + "deg C")

            #Check the value of the temperature and set the LED accordingly
            if (temp_reading < 15.0):
                GPIO.output(RED_LED, False)
                GPIO.output(GREEN_LED, False)
                GPIO.output(BLUE_LED, True)
            elif (temp_reading > 30.0):
                GPIO.output(RED_LED, True)
                GPIO.output(GREEN_LED, False)
                GPIO.output(BLUE_LED, False)
            else:
                GPIO.output(RED_LED, False)
                GPIO.output(GREEN_LED, True)
                GPIO.output(BLUE_LED, False)
                      
            time.sleep(0.5)
            
    except KeyboardInterrupt:
        print("Shutting down")

    finally:
        GPIO.cleanup()
        







