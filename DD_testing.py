import RPi.GPIO as GPIO
import time

#newly added
import os
import glob
from bluetooth import *

#newly added
os.system('modprobe w1-gpio')
#os.system('modprobe w1-therm')

GPIO.setmode(GPIO.BCM)


TRIG = 4   
ECHO = 18
#

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)
#GPIO.setup(17, GPIO.OUT)

#newly added , may not need
base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '28*')[0]
device_file = device_folder + '/w1_slave'


#Code for detecting distance
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

#connection points
# RFCOMM is a reliable stream-based protocol, allowing up to 60 simul.. connections to a bluetooth device at a time
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"

#
advertise_service( server_sock, "DistanceDetectServer",
                   service_id = uuid,
                   service_classes = [uuid, SERIAL_PORT_CLASS],
                   profiles = [SERIAL_PORT_PROFILE],
                   )
#
while True:
    print "Waiting for connection on RFCOMM channel %d" % port

    client_sock, client_info = server_sock.accept()
    print "Accepted connection  from ", client_info

    try:
        data = client_sock.recv(1024)
        if len(data) == 0: break
        print "received [%s]" % data

        if data == 'distance':
            print('Distance: {} inches'.format(dist))

        else:
            data = 'WTF!'
        client_sock.send(data)
        print "sending [%s]" % data

    except IOError:
        pass

    except KeyboardInterrupt:

        print "disconnected"

        client_sock.close()
        server_sock.close()
        print "Finite"

        break


    




 
