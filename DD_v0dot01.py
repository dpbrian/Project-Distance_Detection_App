#Distance Code Version 0.01

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

Trig = 4
Echo = 18

GPIO.setup(Trig, GPIO.OUT)
GPIO.setup(Echo, GPIO.IN)

GPIO.output(Trig, True)
time.sleep(0.0001)
GPIO.output(Trig, False)

while GPIO.input(Echo)==False:
    start = time.time()
while GPIO.input(Echo)==True:
    end = time.time()

sig_time = end-start
distance = sig_time/0.000148
print('Distance: {} inches'.format(distance))

GPIO.cleanup()
