import RPi.GPIO as GPIO
from time import sleep

print 'Enter w for forward, s for backward, a for left, d for right movements and p for pivot'
GPIO.setmode(GPIO.BOARD)

Motor1 = 3
Motor2 = 5
Motor3 = 7
Motor4 = 11
tf = 0.2

def fwd():
	print "forward"
	GPIO.output(Motor1,GPIO.HIGH)
	GPIO.output(Motor2,GPIO.LOW)
	GPIO.output(Motor3,GPIO.HIGH)
	GPIO.output(Motor4,GPIO.LOW)

def bwd():
	print "backward"
	GPIO.output(Motor1,GPIO.LOW)
	GPIO.output(Motor2,GPIO.HIGH)
	GPIO.output(Motor3,GPIO.LOW)
	GPIO.output(Motor4,GPIO.HIGH)	

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
        GPIO.output(Motor3,GPIO.HIGH)
        GPIO.output(Motor4,GPIO.LOW)

def pivot():
        print "Pivot"
        GPIO.output(Motor1,GPIO.HIGH)
        GPIO.output(Motor2,GPIO.LOW)
        GPIO.output(Motor3,GPIO.LOW)
        GPIO.output(Motor4,GPIO.HIGH)
	
GPIO.setup(Motor1,GPIO.OUT)
GPIO.setup(Motor2,GPIO.OUT)
GPIO.setup(Motor3,GPIO.OUT)
GPIO.setup(Motor4,GPIO.OUT)

def stop():
	GPIO.output(Motor1,GPIO.LOW)
	GPIO.output(Motor2,GPIO.LOW)
	GPIO.output(Motor3,GPIO.LOW)
	GPIO.output(Motor4,GPIO.LOW)

while True:
	stop()

	ch=raw_input("")
	if(ch=='w' or ch=='w'):
		fwd()
		sleep(tf)		
	if(ch=='s' or ch=='S'):
		bwd()
		sleep(tf)
	if(ch=='a' or ch=='A'):
		left()
		sleep(tf)
	if(ch=='d' or ch=='D'):
		right()
		sleep(tf)
	if(ch=='p' or ch=='P'):
		pivot()
		sleep(tf)
	if(ch=='e' or ch=='E'):
		break
	stop()

GPIO.cleanup()
