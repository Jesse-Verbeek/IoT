import RPi.GPIO as GPIO
import time

servoPIN = 16
GPIO.setmode(GPIO.BCM)
GPIO.setup(servoPIN, GPIO.OUT)

#print('move')

p = GPIO.PWM(servoPIN, 50) # GPIO 17 for PWM with 50Hz
p.start(2.5) # Initialization
def boom():
  p.ChangeDutyCycle(5)
  time.sleep(0.5)
  p.ChangeDutyCycle(7.5)
  time.sleep(1)
  p.ChangeDutyCycle(7.5)
  time.sleep(0.5)
  p.ChangeDutyCycle(5)
  time.sleep(0.5)
  p.ChangeDutyCycle(2.5)
  time.sleep(0.5)
  p.stop()
  GPIO.cleanup()