import RPi.GPIO as GPIO
import time

#newly added
import os
import glob
from bluetooth import *



GPIO.setmode(GPIO.BCM)


TRIG = 4   
ECHO = 18
#

GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)


#def read_dist():
#Code for detecting distance

def read_dist():
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
   
        pulse_width = end-start

        dist = pulse_width / 0.000148
        #print('Distance: {} inches'.format(dist))  
        return dist
         



#connection points
# RFCOMM is a reliable stream-based protocol, allowing up to 60 simul.. connections to a bluetooth device at a time
server_sock=BluetoothSocket( RFCOMM )
server_sock.bind(("",PORT_ANY))
server_sock.listen(1)

port = server_sock.getsockname()[1]

uuid = "00001101-0000-1000-8000-00805F9B34FB" #this doesn't seem correct

#
advertise_service( server_sock, "DistanceDetectServer",
                   service_id = uuid,
                   service_classes = [uuid, SERIAL_PORT_CLASS],
                   profiles = [ SERIAL_PORT_PROFILE ]
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
            data = str(read_dist()) + "!"
            client_sock.send(data)
            print "sending [%s]" % data
            
        else:
            data = 'NAH!'
            client_sock.send(data)
            print "sending [%s]" % data

    except IOError:
        pass

    #except KeyboardInterrupt:

        print "disconnected"

        client_sock.close()
        server_sock.close()
        print "Fin"

        break

GPIO.cleanup()
    




 
