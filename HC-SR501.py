import RPi.GPIO as GPIO
import time
import paho.mqtt.client as paho
import urllib.request

broker = "192.168.112.74"
port = 1883
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
PIR_PIN = 23
LED_PIN = 14

URL = 'https://api.thingspeak.com/update?api_key='
KEY = '8RAMNJI0HY9Z5VPT'

GPIO.setup(PIR_PIN, GPIO.IN)
GPIO.setup(LED_PIN, GPIO.OUT)

print('Starting up the PIR Module (click on STOP to exit)')
time.sleep(1)
print('Ready')


def on_publish(client, userdata, result):
    print("data published")
    pass


client1 = paho.Client("control1")
client1.on_publish = on_publish

while True:
    time.sleep(5)
    if GPIO.input(PIR_PIN):
        GPIO.output(LED_PIN, GPIO.HIGH)
        print('Motion Detected')
        HEADER = '&field1=1'
        NEW_URL = URL + KEY + HEADER
        urllib.request.urlopen(NEW_URL)
        client1.connect(broker, port)
        data = "Motion detected"
        ret = client1.publish("iot/jesse", data)
    else:
        GPIO.output(LED_PIN, GPIO.LOW)
        HEADER = '&field1=0'
        NEW_URL = URL + KEY + HEADER
        urllib.request.urlopen(NEW_URL)
        print('No Motion Detected')
