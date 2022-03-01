from pandas import read_pickle
import RPi.GPIO as GPIO
import time

hiC = 0
reset = 0

while True: 
    if(reset == 900):
        print(hiC)
        hiC = 0
        reset = 0
    if(GPIO.input(19)):
        hiC+=1
    reset +=1
    time.sleep(.00001)


