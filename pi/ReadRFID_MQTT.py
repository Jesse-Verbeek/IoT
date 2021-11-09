#!/usr/bin/env python
#---Eigen Import-----
from Move_Servo import boom
from Led_Move import walk,kitt
from Active_Directory_Connect import valid
#---Eigen Import-----
#---standard Import----
import time
import RPi.GPIO as GPIO
from mfrc522 import SimpleMFRC522
from subprocess import call
#---standard Import----
#nieuw--Corné
import paho.mqtt.client as paho
#nieuw--Corné

broker="192.168.137.29"  #IP Aanpassen naar de mqtt broker die benodigd is
port=1883

def on_publish(client,userdata,result):
    print("data published")
    pass

client1= paho.Client("control1")
client1.on_publish = on_publish
#TM Hier
herrie_pin = 21
clock_pin = 19
data_pin = 26

reader = SimpleMFRC522()

def RFIDcheck():
    id,text = reader.read()
    client1.connect(broker, port)                       #N

    if valid(str(id)) == True:
        led(),slagboom()
        data = ("ID klopt", id)                         #N
        ret = client1.publish("iot/mauro", data)        #N

    else:
        data = ("ID klopt niet", id)                    #N
        ret = client1.publish("iot/mauro", data)        #N
        walk(clock_pin,data_pin,0.03)
        GPIO.setup(21, GPIO.OUT)
        GPIO.output(21, GPIO.HIGH)
        time.sleep(1)
        GPIO.output(21, GPIO.LOW)
        call(["python", "Sendmail_Gmail.py"])


def led():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(0)

    kitt(clock_pin,data_pin,0.05)

def slagboom():
    boom()

RFIDcheck()