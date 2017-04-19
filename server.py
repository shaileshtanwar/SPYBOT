import SimpleHTTPServer
import SocketServer
import BaseHTTPServer
from os import curdir, sep
import urlparse
import RPi.GPIO as GPIO
import sys
from time import sleep
import time as time

GPIO.setmode(GPIO.BOARD)

Motor1 = 3
Motor2 = 5
Motor3 = 11
Motor4 = 7
TRIG = 22
ECHO = 18

dtf = 0.2
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
		angle1= angle1+5
	duty1= float(angle1)/10 + 2.5
	pwm1.ChangeDutyCycle(duty1) 
	sleep(0.1)
	
def pandw():
	global pwm1
	global angle1
	print "pandw"
	if(10<angle1):
                angle1= angle1-5
        duty1= float(angle1)/10 + 2.5
        pwm1.ChangeDutyCycle(duty1)
	sleep(0.1)
	
def tiltup():
	global pwm2
        global angle2
	print "tiltup"
	if(angle2<170):
                angle2= angle2+5
        duty2= float(angle2)/10 + 2.5
        pwm2.ChangeDutyCycle(duty2)
	sleep(0.1)	

def tiltdw():
	global pwm2
        global angle2
	print "tiltdw"
	if(10<angle2):
                angle2= angle2-5
        duty2= float(angle2)/10 + 2.5
        pwm2.ChangeDutyCycle(duty2)
	sleep(0.1)

print "Setting Up"
	
GPIO.setup(Motor1,GPIO.OUT)
GPIO.setup(Motor2,GPIO.OUT)
GPIO.setup(Motor3,GPIO.OUT)
GPIO.setup(Motor4,GPIO.OUT)
GPIO.setup(12, GPIO.OUT)
GPIO.setup(16, GPIO.OUT)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)

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
	if distance<8:
		print"obstruction detected"
		pivot()
		sleep(1)
def stop():
	GPIO.output(Motor1,GPIO.LOW)
	GPIO.output(Motor2,GPIO.LOW)
	GPIO.output(Motor3,GPIO.LOW)
	GPIO.output(Motor4,GPIO.LOW)

stop()
init()

class MyHandler(BaseHTTPServer.BaseHTTPRequestHandler):
  def do_HEAD(s):
    s.send_response(200)
    s.send_header("Content-type", "text/html")
    s.end_headers()
  
  def do_GET(self):
    print "GETTER"
    if self.path=="/":
      self.path="/index.html"

    qs = {}
    path = self.path
    if '?' in path:
        path, tmp = path.split('?', 1)
        qs = urlparse.parse_qs(tmp)
    print path, qs

    if(bool(qs)):
        if(qs['dir']==['w']):
	    fwd()
	    sleep(dtf)
	    obs()
	    stop()

        if(qs['dir']==['s']):
            bwd()
	    sleep(dtf)
	    obs()
            stop()

        if(qs['dir']==['a']):
            left()
	    sleep(dtf)
	    obs()
            stop()

        if(qs['dir']==['d']):
            right()
	    sleep(dtf)
	    obs()
            stop()
	
	if(qs['dir']==['p']):
            pivot()
            sleep(dtf)
            stop()
	
	if(qs['dir']==['pd']):
            panup()
            sleep(dtf)
            stop()
	
	if(qs['dir']==['pu']):
            pandw()
            sleep(dtf)
            stop()
	
	if(qs['dir']==['td']):
            tiltup()
            sleep(dtf)
            stop()
	
	if(qs['dir']==['tu']):
            tiltdw()
            sleep(dtf)
            stop()





    try:
      sendReply = False
      if self.path.endswith(".html"):
        mimetype='text/html'
        sendReply = True
      
      if sendReply == True:
        f = open(curdir + sep + self.path) 
        self.send_response(200)
        self.send_header('Content-type',mimetype)
        self.end_headers()
        self.wfile.write(f.read())
        f.close()
      return


    except IOError:
      self.send_error(404,'File Not Found: %s' % self.path)


port = 80

handler = SimpleHTTPServer.SimpleHTTPRequestHandler

httpd = SocketServer.TCPServer(("", port), MyHandler)

print "serving at ", port

httpd.serve_forever()
