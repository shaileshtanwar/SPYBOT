import RPi.GPIO as GPIO
import sys
from time import sleep

GPIO.setmode(GPIO.BOARD)

Motor1 = 3
Motor2 = 5
Motor3 = 7
Motor4 = 11

def do_OPTIONS(self):
	self.sendResponse(200)
	self.processRequest()
	self.send_header('Access-Control-Allow-Origin', '*')
	self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
	self.send_header('Access-Control-Allow-Headers', 'X-Requested-With')

def do_GET(self):
	self.send_response(200)
	self.send_header('Access-Control-Allow-Origin', '*')
	self.send_header('Content-type', 'text/html')
	self.end_headers()
	self.wfile.write("<htmL><body>Hello!</body></html>")
	self.connection.shutdown(1)

def fwd():
	print "forward"
	GPIO.output(Motor1,GPIO.LOW)
	GPIO.output(Motor2,GPIO.HIGH)
	GPIO.output(Motor3,GPIO.LOW)
	GPIO.output(Motor4,GPIO.HIGH)

def bwd():
	print "backward"
	GPIO.output(Motor1,GPIO.HIGH)
	GPIO.output(Motor2,GPIO.LOW)
	GPIO.output(Motor3,GPIO.HIGH)
	GPIO.output(Motor4,GPIO.LOW)	

print "Setting Up"
	
GPIO.setup(Motor1,GPIO.OUT)
GPIO.setup(Motor2,GPIO.OUT)
GPIO.setup(Motor3,GPIO.OUT)
GPIO.setup(Motor4,GPIO.OUT)

def stop():
	GPIO.output(Motor1,GPIO.LOW)
	GPIO.output(Motor2,GPIO.HIGH)
	GPIO.output(Motor3,GPIO.LOW)
	GPIO.output(Motor4,GPIO.HIGH)

stop()

ch=sys.stdin
if(ch=='w' or ch=='W'):
	fwd()
	sleep(20)		
if(ch=='s' or ch=='S'):
	bwd()
	sleep(20)
if(ch=='e' or ch=='E'):
	print "exit"
stop()

GPIO.cleanup()
