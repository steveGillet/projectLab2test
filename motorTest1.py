import RPi.GPIO as GPIO
import time
import board
import adafruit_mpu6050
from math import atan2, degrees

i2c = board.I2C()  # uses board.SCL and board.SDA
mpu = adafruit_mpu6050.MPU6050(i2c)

pwm1 = 19
pwm2 = 18
enA1 = 6
enB1 = 21
enA2 = 26
enB2 = 20

GPIO.setmode(GPIO.BCM)
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

gyroLock = 0

while True:
    x,y,z = mpu.acceleration
    angle = degrees(atan2(z,x))
    if angle < 0:
        angle += 360
    
    if(angle > 80 and angle < 85):
        gyroLock = 0
    if(angle > 85 and gyroLock == 0): 
        # negative x, less than 1
        pwm1Set.ChangeDutyCycle(100)
        pwm2Set.ChangeDutyCycle(100)
        GPIO.output(enA1, 0)
        GPIO.output(enB1, 1)
        GPIO.output(enA2, 0)
        GPIO.output(enB2, 1)
        gyroLock = 1

    elif(angle < 80 and gyroLock == 0): 
        # positive x, greater than 2
        pwm1Set.ChangeDutyCycle(100)
        pwm2Set.ChangeDutyCycle(100)
        GPIO.output(enA1, 1)
        GPIO.output(enB1, 0)
        GPIO.output(enA2, 1)
        GPIO.output(enB2, 0)
        gyroLock = 1

    elif(gyroLock == 0):
        pwm1Set.ChangeDutyCycle(0)
        pwm2Set.ChangeDutyCycle(0)
        GPIO.output(enA1, 0)
        GPIO.output(enB1, 0)
        GPIO.output(enA2, 0)
        GPIO.output(enB2, 0)
    time.sleep(.1)
    print(angle)
