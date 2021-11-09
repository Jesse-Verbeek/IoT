import Adafruit_DHT
import time
import serial
import paho.mqtt.client as paho

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
broker = "192.168.178.20"
port = 1883


def on_publish(client, userdata, result):
    print("data published")
    pass


client1 = paho.Client("control1")
client1.on_publish = on_publish

while True:
    humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
    ser.flush()
    line = ser.readline().decode('utf-8').rstrip()
    print(line)
    if humidity is not None and temperature is not None:
        # print("Temp={0:0.1f}C Humidity={1:0.1f}%".format(temperature, humidity))
        client1.connect(broker, port)
        line = str(line)
        temperature = str(temperature)
        humidity = str(humidity)
        data = str(line + " " + temperature + " " + humidity)
        ret = client1.publish("iot/corne", data)
    else:
        print("Sensor failure. Check wiring.")
    time.sleep(5)
