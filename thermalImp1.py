
import time,board,busio
import numpy as np
import adafruit_mlx90640
import RPi.GPIO as GPIO

extinguishLED = 12

GPIO.setup(extinguishLED, GPIO.OUT)
GPIO.output(extinguishLED, 0)

i2c = busio.I2C(board.SCL, board.SDA, frequency=400000)
mlx = adafruit_mlx90640.MLX90640(i2c)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ

frame = np.zeros((24*32,)) 
while True:
    mlx.getFrame(frame) 
    if(np.maximum(frame) > 100):
        GPIO.output(extinguishLED, 1)




