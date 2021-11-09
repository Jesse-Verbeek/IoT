import time
import urllib.request
import requests
import threading
import json

def get_temp(dev_file):
    f = open(dev_file,"r")
    contents = f.readlines()
    f.close()
    index = contents[-1].find("t=")
    if index != -1 :
        temperature = contents[-1][index+2:]
        cels =float(temperature)/1000
        return cels


def thingspeak_post():
    threading.Timer(15, thingspeak_post).start()

    URl = 'https://api.thingspeak.com/update?api_key='
    KEY = "BEVU57D5YG3BPQV0"
    HEADER = '&field1={}'.format(temp0)
    NEW_URL = URl + KEY + HEADER
    #print(NEW_URL)
    data = urllib.request.urlopen(NEW_URL)




if __name__ == '__main__':
    while True:
        time.sleep(15)
        temp0 = print(get_temp("/sys/bus/w1/devices/28-0119210f2093/w1_slave"))
        thingspeak_post()





sensoren_data = [temp0,temp1,temp2]
print(sensoren_data)