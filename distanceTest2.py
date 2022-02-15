import RPi.GPIO as GPIO          
import time
GPIO.setmode(GPIO.BCM)

GPIO.setup(19, GPIO.IN)

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
