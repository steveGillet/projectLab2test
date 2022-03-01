import RPi.GPIO as GPIO
import time
import pigpio

pi = pigpio.pi()
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)
pi.read(18)

while True:
    print(pi.get_PWM_real_range(18))
    time.sleep(1)
