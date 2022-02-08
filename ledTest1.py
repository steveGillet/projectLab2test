import RPi.GPIO as GPIO
import time

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(22, GPIO.OUT)
GPIO.setup(4, GPIO.IN)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

GPIO.output(17, 1)
GPIO.output(22, 0)

while True:
    GPIO.output(26, 0)
    if (GPIO.input(4)):
        GPIO.output(22, 1)
    else:
        GPIO.output(22, 0)
    