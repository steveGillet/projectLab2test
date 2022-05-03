import RPi.GPIO as GPIO          
import time,board,busio
import numpy as np
import adafruit_mlx90640
import pigpio

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000) # setup I2C
mlx = adafruit_mlx90640.MLX90640(i2c) # begin MLX90640 with I2C comm
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ # set refresh rate

frame = np.zeros((24*32,))

GPIO.setwarnings(False)

front = 14
left = 4
right = 15
pwm1 = 19
pwm2 = 18
enA1 = 6
enB1 = 21
enA2 = 26
enB2 = 20
fire = 27

pi = pigpio.pi()
GPIO.setmode(GPIO.BCM)
GPIO.setup(front, GPIO.IN)
pi.read(front)
GPIO.setup(left, GPIO.IN)
pi.read(left)
GPIO.setup(right, GPIO.IN)
pi.read(right)

GPIO.setup(pwm1, GPIO.OUT)
GPIO.setup(pwm2, GPIO.OUT)
pwm1Set = GPIO.PWM(pwm1, 100)
pwm2Set = GPIO.PWM(pwm2, 100)

pwm1Set.start(0)
pwm2Set.start(0)

GPIO.setup(enA1, GPIO.OUT)
GPIO.setup(enB1, GPIO.OUT)
GPIO.setup(enA2, GPIO.OUT)
GPIO.setup(enB2, GPIO.OUT)
GPIO.setup(fire, GPIO.OUT)

fRiseTick = 0
fFallTick = 0
fpWidth = 0
lRiseTick = 0
lFallTick = 0
lpWidth = 0
rRiseTick = 0
rFallTick = 0
rpWidth = 0
thermalCounter = 0
pidSpeed = 20

def thermal():
    mlx.getFrame(frame) # read MLX temperatures into frame var
    # print out the average temperature from the MLX90640
    print('Average MLX90640 Temperature: {0:2.1f}C ({1:2.1f}F)'.\
    format(np.max(frame),(((9.0/5.0)*np.max(frame))+32.0)))
    return ((9.0/5.0)*np.max(frame)+32.0)

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
turnLockLeft = 1
turnLockRight = 1

while True:
    wallFront = fpWidth < 1300
    wallLeft = lpWidth < 1500
    wallRight = rpWidth < 1100
    
    if(state == "left"):
        print("left")
        GPIO.output(enA1, 0)
        GPIO.output(enB1, 1)
        GPIO.output(enA2, 1)
        GPIO.output(enB2, 0)
        pwm1Set.ChangeDutyCycle(pidSpeed)
        pwm2Set.ChangeDutyCycle(pidSpeed)
        time.sleep(1)
        if(not wallFront):
            state = "forward"
    
    elif(state == "right"):
        print("right")
        GPIO.output(enA1, 1)
        GPIO.output(enB1, 0)
        GPIO.output(enA2, 0)
        GPIO.output(enB2, 1)
        pwm1Set.ChangeDutyCycle(pidSpeed)
        pwm2Set.ChangeDutyCycle(pidSpeed)
        time.sleep(1)
        if(not wallFront):
            state = "forward"

    elif(state == "forward"):
        print("forward")
        GPIO.output(enA1, 1)
        GPIO.output(enB1, 0)
        GPIO.output(enA2, 1)
        GPIO.output(enB2, 0)
        pwm1Set.ChangeDutyCycle(pidSpeed)
        pwm2Set.ChangeDutyCycle(pidSpeed)
        if(wallLeft):
            turnLockLeft = 0
        if(wallRight):
            turnLockRight = 0    
        if(not wallLeft and not turnLockLeft):
            state = "left"
            turnLockLeft = 1
        elif(wallLeft and not wallRight and not turnLockRight):
            state = "right"
            turnLockRight = 1
        elif(wallFront):
            state = "left"
        else:
            state = "forward"        
    if(thermalCounter == 20):
        while(thermal() > 120):
            print("fire")
            GPIO.output(enA1, 0)
            GPIO.output(enB1, 0)
            GPIO.output(enA2, 0)
            GPIO.output(enB2, 0)
            pwm1Set.ChangeDutyCycle(0)
            pwm2Set.ChangeDutyCycle(0)
            GPIO.output(fire, 1)
        GPIO.output(fire, 0)
        thermalCounter = 0
    thermalCounter += 1
    time.sleep(.25)
