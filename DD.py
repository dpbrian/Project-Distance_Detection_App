import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)

TRIG = 4   
ECHO = 18
#

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

for x in range(0,50):
    print('Setup')
    GPIO.output(TRIG, False)
    time.sleep(2)

    print('Ping Pulse (trigger)')
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    while GPIO.input(ECHO)==False:
        start = time.time()
        
    while GPIO.input(ECHO)==True:
        end = time.time()
    #print('Finished Reading')
    pulse_width = end-start

    dist = pulse_width / 0.000148
    print('Distance: {} inches'.format(dist))
    #if dist > 2 and dist < 400:
    #    print('Distance ', dist)
    #else:
    #    print ('Nothing Close')

GPIO.cleanup()


 
