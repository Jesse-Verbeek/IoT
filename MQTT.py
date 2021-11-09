import paho.mqtt.client as mqtt
import mysql.connector
from datetime import datetime

mydb = mysql.connector.connect(
    host="192.168.178.20",
    user="corne",
    password="Welkom01",
    database="iot"
)
mycursor = mydb.cursor()


def mysqldata(onderwerp, data):
    vardatetime = (datetime.now()).strftime("%Y-%m-%d %H:%M:%S")
    print(data)
    onderwerp = onderwerp.replace("/", "")
    print(onderwerp)
    if onderwerp == "iotjesse":
        sql = "INSERT INTO iotjesse (Beweging, Recorded) VALUES (%s, %s)"
        val = (data, vardatetime)
        mycursor.execute(sql, val)
        mydb.commit()
    elif onderwerp == "iotcorne":
        ldata = []
        ldata = str(data)
        ldata = ldata.replace('.0', '')
        ldata = str.split(ldata)
        print(ldata)
        try:
            val = (int(ldata[0]), int(ldata[1]), int(ldata[2]), vardatetime)
            print(val)
        except ValueError:
            val = (0, int(ldata[0]), int(ldata[1]), vardatetime)
            print(val)
        except IndexError:
            val = (0, int(ldata[0]), int(ldata[1]), vardatetime)
            print(val)
        sql = "INSERT INTO iotcorne (C02, Temperatuur, Humidity, Recorded) VALUES (%s, %s, %s, %s)"
        mycursor.execute(sql, val)
        mydb.commit()
    elif onderwerp == "iotmauro":
        ldata = []
        ldata = str(data)
        ldata = ldata.replace('.0', '')
        ldata = str.split(ldata)
        print(ldata)
        val = (str(ldata[0]), int(ldata[1]), vardatetime)
        sql = "INSERT INTO iotmauro (Waarde, TagID, Recorded) VALUES (%s, %s, %s)"
        mycursor.execute(sql, val)
        mydb.commit()
    elif onderwerp == "iotsam":
        val = (data, vardatetime)
        sql = "INSERT INTO iotsam (Waarde, Recorded) VALUES (%s, %s)"
        mycursor.execute(sql, val)
        mydb.commit()


def on_connect(client, userdata, flags, rc):  # The callback for when the client connects to the broker
    print("Connected with result code {0}".format(str(rc)))  # Print result of connection attempt
    client.subscribe([("iot/corne", 0), ("iot/jesse", 1), ("iot/mauro", 2),
                      ("iot/sam", 3)])  # Subscribe to the topic “digitest/test1”, receive any messages published on it


def on_message(client, userdata, msg):  # The callback for when a PUBLISH message is received from the server.
    #    print(msg.topic)
    #    print("Message received-> " + msg.topic + " " + str(msg.payload))  # Print a received msg
    mysqldata(msg.topic, str(msg.payload.decode()))


#    mysqldata(msg.payload)

client = mqtt.Client("digi_mqtt_test")  # Create instance of client with client ID “digi_mqtt_test”
client.on_connect = on_connect  # Define callback function for successful connection
client.on_message = on_message  # Define callback function for receipt of a message
# client.connect("m2m.eclipse.org", 1883, 60)  # Connect to (broker, port, keepalive-time)
client.connect('192.168.178.20', 1883)
client.loop_forever()  # Start networking daemon
