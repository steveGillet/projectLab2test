import numpy as np
import RPi.GPIO as GPIO
import time
import board
import adafruit_mpu6050

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

i2c = board.I2C()  # uses board.SCL and board.SDA
mpu = adafruit_mpu6050.MPU6050(i2c)

pwm1 = 19
pwm2 = 18
enA1 = 6
enB1 = 21
enA2 = 26
enB2 = 20

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

K = 0.98
Kn = 1 - K

timeDiff = .01

aX = mpu.acceleration[0]
aY = mpu.acceleration[1]
aZ = mpu.acceleration[2]

gX = mpu.gyro[0]
gY = mpu.gyro[1]
gZ = mpu.gyro[2]

def distance(a, b):
    return np.sqrt(a*a + b*b)

def yAngle(x, y, z):
    radians = np.arctan2(x, distance(y, z))
    return -np.degrees(radians)

def xAngle(x, y, z):
    radians = np.arctan2(y, distance(x, z))
    return np.degrees(radians)

lastX = xAngle(aX, aY, aZ)
lastY = yAngle(aX, aY, aZ)

xOffset = gX
yOffset = gY

xTotal = lastX - xOffset
yTotal = lastY - yOffset

class pidC:
    def __init__(self, P, I, D):
        self.KP = P
        self.KI = I
        self.KD = D
        self.target = 0

        self.lastError = 0
        self.integrator = 0

    def setTarget(self, newTarget):
        self.target = newTarget
        self.integrator = 0
        self.dt = 0

    def step(self, currentValue):
        error = currentValue - self.target

        output = (self.KP * error + self.KI * self.integrator + self.KD * error / self.dt)

        self.lastError = error
        self.dt += timeDiff
        self.integrator += error * self.dt

        return output

initialX = lastX

pid = pidC(P=17, I=100, D=0.8)

pid.setTarget(initialX)

while True:
    aX = mpu.acceleration[0]
    aY = mpu.acceleration[1]
    aZ = mpu.acceleration[2]

    gX = mpu.gyro[0]
    gY = mpu.gyro[1]
    gZ = mpu.gyro[2]

    gX -= xOffset
    gY -= yOffset

    gXd = (gX * timeDiff)
    gYd = (gY * timeDiff)

    xTotal += gXd
    yTotal += gYd

    angleX = xAngle(aX, aY, aZ)
    angleY = yAngle(aX, aY, aZ)

    lastX = K * (lastX + gXd) + (Kn * angleX)

    if(np.absolute(initialX-lastX) < .2):
        pid.setTarget(initialX)

    pidX = pid.step(lastX)
    
    if(pidX > 0.0):
        print("forward")
        pidSpeed = np.clip(np.absolute(pidX), 0, 100)
        GPIO.output(enA1, 1)
        GPIO.output(enB1, 0)
        GPIO.output(enA2, 1)
        GPIO.output(enB2, 0)
        pwm1Set.ChangeDutyCycle(pidSpeed)
        pwm2Set.ChangeDutyCycle(pidSpeed)

    elif(pidX < 0.0):
        print("backward")
        pidSpeed = np.clip(np.absolute(pidX), 0, 100)
        GPIO.output(enA1, 1)
        GPIO.output(enB1, 0)
        GPIO.output(enA2, 1)
        GPIO.output(enB2, 0)
        pwm1Set.ChangeDutyCycle(pidSpeed)
        pwm2Set.ChangeDutyCycle(pidSpeed)

    else:
        GPIO.output(enA1, 0)
        GPIO.output(enB1, 0)
        GPIO.output(enA2, 0)
        GPIO.output(enB2, 0)
        pwm1Set.ChangeDutyCycle(0)
        pwm2Set.ChangeDutyCycle(0)
        
    # print("Target: " + str(pid.target))
    print(lastX, pidX)    
    time.sleep(timeDiff)
        
