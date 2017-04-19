import io
import picamera
import cv2
import numpy
import RPi.GPIO as GPIO
import time
from time import sleep
import random
GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
TRIG = 22
ECHO = 18
Motor1 = 3
Motor2 = 5
Motor3 = 11
Motor4 = 7

print "Setting Up"
GPIO.setup(Motor1,GPIO.OUT)
GPIO.setup(Motor2,GPIO.OUT)
GPIO.setup(Motor3,GPIO.OUT)
GPIO.setup(Motor4,GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

dtf = 0.5
global angle1
global angle2
global pwm1
global pwm2

def init():
        global angle1
        global angle2
        angle1=90
        angle2=90
        global pwm1
        global pwm2
        pwm1=GPIO.PWM(12,100)
        pwm1.start(5)
        pwm2=GPIO.PWM(16,100)
        pwm2.start(5)

def fwd():
    print "forward"
    GPIO.output(Motor1,GPIO.HIGH)
    GPIO.output(Motor2,GPIO.LOW)
    GPIO.output(Motor3,GPIO.LOW)
    GPIO.output(Motor4,GPIO.HIGH)

def bwd():
    print "backward"
    GPIO.output(Motor1,GPIO.LOW)
    GPIO.output(Motor2,GPIO.HIGH)
    GPIO.output(Motor3,GPIO.HIGH)
    GPIO.output(Motor4,GPIO.LOW)

def left():
        print "Left"
        GPIO.output(Motor1,GPIO.HIGH)
        GPIO.output(Motor2,GPIO.LOW)
        GPIO.output(Motor3,GPIO.LOW)
        GPIO.output(Motor4,GPIO.LOW)


def right():
        print "Right"
        GPIO.output(Motor1,GPIO.LOW)
        GPIO.output(Motor2,GPIO.LOW)
        GPIO.output(Motor3,GPIO.LOW)
        GPIO.output(Motor4,GPIO.HIGH)
def pivot():
        print "Pivot"
        GPIO.output(Motor1,GPIO.HIGH)
        GPIO.output(Motor2,GPIO.LOW)
        GPIO.output(Motor3,GPIO.HIGH)
        GPIO.output(Motor4,GPIO.LOW)

def panup():
        global pwm1
        global angle1
        print "Panup"
        if(angle1<170):
                angle1= angle1+1
        duty1= float(angle1)/10 + 2.5
        pwm1.ChangeDutyCycle(duty1)
        sleep(0.1)

def pandw():
        global pwm1
        global angle1
        print "pandw"
        if(10<angle1):
                angle1= angle1-1
        duty1= float(angle1)/10 + 2.5
        pwm1.ChangeDutyCycle(duty1)
        sleep(0.1)

def tiltup():
        global pwm2
        global angle2
        print "tiltup"
        if(angle2<170):
                angle2= angle2+1
        duty2= float(angle2)/10 + 2.5
        pwm2.ChangeDutyCycle(duty2)
        sleep(0.1)

def tiltdw():
        global pwm2
        global angle2
        print "tiltdw"
        if(10<angle2):
                angle2= angle2-1
        duty2= float(angle2)/10 + 2.5
        pwm2.ChangeDutyCycle(duty2)
        sleep(0.1)


def obs():
        GPIO.output(TRIG, False)
        print "Waiting For Sensor To Settle"
        time.sleep(0.1)
        GPIO.output(TRIG, True)
        time.sleep(0.00001)
        GPIO.output(TRIG, False)
        while GPIO.input(ECHO)==0:
                pulse_start = time.time()
        while GPIO.input(ECHO)==1:
                pulse_end = time.time()
        pulse_duration = pulse_end - pulse_start
        distance = pulse_duration * 17150
        distance = round(distance, 2)
	print distance
        if distance<8 :
                print"obstruction detected"
                pivot()
		sleep(1)

def fd():
	timestr = time.strftime("%Y%m%d-%H%M%S")
	stream = io.BytesIO()
	with picamera.PiCamera() as camera:
	    camera.resolution = (320, 240)
	    camera.capture(stream, format='jpeg')

	buff = numpy.fromstring(stream.getvalue(), dtype=numpy.uint8)
	image = cv2.imdecode(buff, 1)
	face_cascade = cv2.CascadeClassifier('/usr/share/opencv/haarcascades/haarcascad$
	gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
	faces = face_cascade.detectMultiScale(gray, 1.1, 5)
	print "Found "+str(len(faces))+" face(s)"
	for (x,y,w,h) in faces:
    		cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
	print "len="+str(len(faces))+">0"
	num = (len(faces))
	if(num>0):
        	cv2.imwrite(timestr+'.jpg',image)
	else:
        	print "not saved"

def stop():
	print"stop"
        GPIO.output(Motor1,GPIO.LOW)
        GPIO.output(Motor2,GPIO.LOW)
        GPIO.output(Motor3,GPIO.LOW)
        GPIO.output(Motor4,GPIO.LOW)

stop()
init()

def automode():
	dtf = 2
	print"start"
	while(1):
		print"working"	
		num = random.randrange(0,3)
		if num == 0:
			fwd()
			sleep(dtf)
			obs()
			stop()
		if num == 1:
			bwd()
			sleep(dtf)
			obs()
			stop()
		if num == 2:
			left()
			sleep(dtf)
			obs()
			stop()
		if num == 3:
			right()
			sleep(dtf)
			obs()
			stop()

		
automode()	
