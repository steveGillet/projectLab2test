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
turnRight = 0
turnWindow = 0
turning = 0
turnStop = 0
turnLock = 1
turnLockOff = 0
state = "forward"
forwardClear = 0

while True:

    noWallFront = wallFront > 86 and wallFront <= 102
    isWallFront = not noWallFront
    noWallLeft = wallLeft > 86 and wallLeft <= 102
    isWallLeft = not noWallLeft
    noWallRight = wallRight > 86 and wallRight <= 102
    isWallRight = not noWallRight


    if(state == "left"):
        GPIO.output(frontLED, 0)
        GPIO.output(leftLED, 1)
        GPIO.output(rightLED, 0)
        if(forwardClear > 2):
            forwardClear = 0
            state = "forward"
            turnLock = 1
    elif(state == "forward"):
        GPIO.output(frontLED, 1)
        GPIO.output(leftLED, 0)
        GPIO.output(rightLED, 0)
        if(turnLeft > 4):
            state = "left"
        elif(turnRight > 4):
            state = "right"
    elif(state == "right"):
        GPIO.output(frontLED, 0)
        GPIO.output(leftLED, 0)
        GPIO.output(rightLED, 1)
        if(forwardClear > 2):
            forwardClear = 0
            state = "forward"

    if(reset == 900):
        if(noWallLeft and not turnLock):
            turnLeft += 1
        elif(isWallLeft and noWallFront):
            turnLockOff += 1
        elif(isWallLeft and isWallFront):
            if(isWallRight):
                turnLeft += 1
            else:
                turnRight += 1
        if(noWallFront):
            forwardClear += 1
        if(turnLockOff == 2):
            turnLock = 0    
        if(turnWindow == 10):
            turnStop = 0
            turnLeft = 0
            turnRight = 0
            turnWindow = 0
            turnLockOff = 0
            forwardClear = 0
        print("wallFront = " + str(wallFront))
        # print("wallLeft = " + str(wallLeft))
        # print("wallRight = " + str(wallRight))
        # print(isWallLeft)
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
