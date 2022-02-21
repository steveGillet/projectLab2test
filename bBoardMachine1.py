import RPi.GPIO as GPIO          
import time

front = 2
left = 3
right = 4
frontLED = 21
leftLED = 16
rightLED = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(front, GPIO.IN)
GPIO.setup(left, GPIO.IN)
GPIO.setup(right, GPIO.IN)
GPIO.setup(frontLED, GPIO.OUT)
GPIO.setup(leftLED, GPIO.OUT)
GPIO.setup(rightLED, GPIO.OUT)
GPIO.output(frontLED, 1)
GPIO.output(leftLED, 0)
GPIO.output(rightLED, 0)

wallFront = 0
wallLeft = 0
wallRight = 0
reset = 0
turnLeft = 0
turnWindow = 0
turning = 0
turnStop = 0
turnLock = 1
turnLockOff = 0

while True:
    if(reset == 900):
        if(wallLeft < 100 and wallLeft > 90 and turnLock == 0):
            turnLeft += 1
        if(wallLeft < 86 and wallFront < 100 and wallFront > 90):
            turnLockOff += 1
            if(turnLockOff == 2):
                turnLock = 0
        if(turnStop > 2):
            turning = 0
            turnStop = 0
            turnLock = 1
            GPIO.output(leftLED, 0)
            GPIO.output(frontLED, 1)
        if(turning == 1 and wallFront < 100 and wallFront > 90):
            turnStop += 1
        #if(wallFront > 100):
        #   turnLeft += 1
        if(turnLeft > 4):
            GPIO.output(leftLED, 1)
            GPIO.output(frontLED, 0)
            turning = 1
        if(turnWindow == 10):
            turnStop = 0
            turnLeft = 0
            turnWindow = 0
            turnLockOff = 0
        print(wallLeft)
        wallFront = 0
        wallLeft = 0
        wallRight = 0
        reset = 0
        turnWindow += 1
    if(GPIO.input(front)):
        wallFront+=1
    if(GPIO.input(left)):
        wallLeft+=1    
    if(GPIO.input(right)):
        wallRight+=1    
    reset +=1
    time.sleep(.00001)
