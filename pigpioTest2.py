import RPi.GPIO as GPIO
import time
import pigpio

front = 2
left = 3
right = 4
frontLED = 21
leftLED = 16
rightLED = 20

pi = pigpio.pi()
GPIO.setmode(GPIO.BCM)
GPIO.setup(front, GPIO.IN)
pi.read(front)
GPIO.setup(left, GPIO.IN)
pi.read(left)
GPIO.setup(right, GPIO.IN)
pi.read(right)

GPIO.setup(frontLED, GPIO.OUT)
GPIO.setup(leftLED, GPIO.OUT)
GPIO.setup(rightLED, GPIO.OUT)
GPIO.output(frontLED, 1)
GPIO.output(leftLED, 0)
GPIO.output(rightLED, 0)

fRiseTick = 0
fFallTick = 0
fpWidth = 0
lRiseTick = 0
lFallTick = 0
lpWidth = 0
rRiseTick = 0
rFallTick = 0
rpWidth = 0

def callBackFront(gpio, level, tick):
    global fRiseTick
    global fFallTick
    global fpWidth
    if(level == 1):
        fRiseTick = tick
    if(level == 0):
        fFallTick = tick
        fpWidth = fFallTick - fRiseTick

def callBackLeft(gpio, level, tick):
    global lRiseTick
    global lFallTick
    global lpWidth
    if(level == 1):
        lRiseTick = tick
    if(level == 0):
        lFallTick = tick
        lpWidth = lFallTick - lRiseTick        

def callBackRight(gpio, level, tick):
    global rRiseTick
    global rFallTick
    global rpWidth
    if(level == 1):
        rRiseTick = tick
    if(level == 0):
        rFallTick = tick
        rpWidth = rFallTick - rRiseTick

cbF = pi.callback(front, pigpio.EITHER_EDGE, callBackFront)
cbL = pi.callback(left, pigpio.EITHER_EDGE, callBackLeft)
cbR = pi.callback(right, pigpio.EITHER_EDGE, callBackRight)

state = "forward"
turnLock = 1

while True:
    wallFront = fpWidth < 1200
    wallLeft = lpWidth < 1500
    wallRight = rpWidth < 1200
    
    if(state == "left"):
        GPIO.output(frontLED, 0)
        GPIO.output(leftLED, 1)
        GPIO.output(rightLED, 0)
        if(not wallFront):
            state = "forward"
    
    elif(state == "forward"):
        GPIO.output(frontLED, 1)
        GPIO.output(leftLED, 0)
        GPIO.output(rightLED, 0)
        if(wallLeft):
            turnLock = 0
        if(not wallLeft and not turnLock):
            state = "left"
            turnLock = 1
        elif(wallLeft and wallFront and not wallRight):
            state = "right"
        elif(wallFront and wallRight):
            state = "left"
        else:
            state = "forward"
    
    elif(state == "right"):
        GPIO.output(frontLED, 0)
        GPIO.output(leftLED, 0)
        GPIO.output(rightLED, 1)
        if(not wallFront):
            state = "forward"
    print(rpWidth)
    time.sleep(1)
