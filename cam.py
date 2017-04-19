from picamera import PiCamera
from time import sleep

camera = PiCamera()

camera.start_preview()
camera.annotate_text = "Hello world!"
sleep(5)
camera.capture('/home/pi/Desktop/text.jpg')
camera.stop_preview()
