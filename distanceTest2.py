import RPi.GPIO as GPIO          
import time
GPIO.setmode(GPIO.BCM)

GPIO.setup(19, GPIO.IN)
GPIO.setup(14, GPIO.OUT)
GPIO.output(14, 0)

hiC = 0
reset = 0
turnCount = 0
turnWindow = 0
turning = 0
turnStop = 0

while True:
    if(reset == 900):
        if(turnStop > 5):
            turning = 0
            turnStop = 0
            GPIO.output(14, 0)
        if(turning == 1 and hiC < 95):
            turnStop += 1
        if(hiC>100):
            turnCount += 1
        if(turnCount > 4):
            GPIO.output(14, 1)
            turning = 1
        if(turnWindow == 10):
            turnStop = 0
            turnCount = 0
            turnWindow = 0
        print(hiC)
        hiC = 0
        reset = 0
        turnWindow += 1
    if(GPIO.input(19)):
        hiC+=1
    reset +=1
    time.sleep(.00001)
