import RPi.GPIO as GPIO
import time
import board
import adafruit_mpu6050

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
pwm1Set = GPIO.PWM(pwm1, 50)
pwm2Set = GPIO.PWM(pwm2, 50)

pwm1Set.start(0)
pwm2Set.start(0)

GPIO.setup(enA1, GPIO.OUT)
GPIO.setup(enB1, GPIO.OUT)
GPIO.setup(enA2, GPIO.OUT)
GPIO.setup(enB2, GPIO.OUT)

pwm1Set.ChangeDutyCycle(50)
pwm2Set.ChangeDutyCycle(50)
GPIO.output(enA1, 0)
GPIO.output(enB1, 1)
GPIO.output(enA2, 0)
GPIO.output(enB2, 1)
time.sleep(2)
pwm1Set.ChangeDutyCycle(50)
pwm2Set.ChangeDutyCycle(50)
GPIO.output(enA1, 1)
GPIO.output(enB1, 0)
GPIO.output(enA2, 1)
GPIO.output(enB2, 0)
time.sleep(2)
pwm1Set.ChangeDutyCycle(0)
pwm2Set.ChangeDutyCycle(0)
GPIO.output(enA1, 0)
GPIO.output(enB1, 0)
GPIO.output(enA2, 0)
GPIO.output(enB2, 0)
time.sleep(2)
        
print(mpu.acceleration[0])
