import RPi.GPIO as GPIO
from time import sleep
import sys
from  Tkinter import *
from time import sleep
import time as time

GPIO.setmode(GPIO.BOARD)

Motor1 = 3
Motor2 = 5
Motor3 = 7
Motor4 = 11
tf = 0.2
TRIG = 22
ECHO = 18


def bwd(tf):
	print "backword"
	GPIO.output(Motor1,GPIO.LOW)
	GPIO.output(Motor2,GPIO.HIGH)
	GPIO.output(Motor3,GPIO.LOW)
	GPIO.output(Motor4,GPIO.HIGH)
	sleep(tf)
	stop()

def fwd(tf):
	print "forward"
	GPIO.output(Motor1,GPIO.HIGH)
	GPIO.output(Motor2,GPIO.LOW)
	GPIO.output(Motor3,GPIO.HIGH)
	GPIO.output(Motor4,GPIO.LOW)	
	sleep(tf)
	stop()

def left(tf):
        print "Left"
        GPIO.output(Motor1,GPIO.HIGH)
        GPIO.output(Motor2,GPIO.LOW)
        GPIO.output(Motor3,GPIO.LOW)
        GPIO.output(Motor4,GPIO.LOW)
	sleep(tf)
	stop()


def right(tf):
        print "Right"
        GPIO.output(Motor1,GPIO.LOW)
        GPIO.output(Motor2,GPIO.LOW)
        GPIO.output(Motor3,GPIO.HIGH)
        GPIO.output(Motor4,GPIO.LOW)
	sleep(tf)
	stop()

def pivot(tf):
        print "Pivot"
        GPIO.output(Motor1,GPIO.LOW)
        GPIO.output(Motor2,GPIO.HIGH)
        GPIO.output(Motor3,GPIO.HIGH)
        GPIO.output(Motor4,GPIO.LOW)
	sleep(tf)
	stop()

GPIO.setup(Motor1,GPIO.OUT)
GPIO.setup(Motor2,GPIO.OUT)
GPIO.setup(Motor3,GPIO.OUT)
GPIO.setup(Motor4,GPIO.OUT)
GPIO.setup(TRIG,GPIO.OUT)
GPIO.setup(ECHO,GPIO.IN)


def stop():
	GPIO.output(Motor1,GPIO.LOW)
	GPIO.output(Motor2,GPIO.LOW)
	GPIO.output(Motor3,GPIO.LOW)
	GPIO.output(Motor4,GPIO.LOW)

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
                pivot(1)
                sleep(1)

def key_input(event):
	print 'key',event.char
	key_press = event.char
	sleep_time = 0.30

	if key_press.lower() == 'w':
		obs()
		fwd(sleep_time)
	elif key_press.lower() == 's':
                obs()
		bwd(sleep_time)
	elif key_press.lower() == 'a':
                obs()
		left(sleep_time)
	elif key_press.lower() == 'd':
                obs()
		right(sleep_time)
	elif key_press.lower() == 'p':
                pivot(sleep_time)

command = Tk()
command.bind('<KeyPress>',key_input)
command.mainloop()
