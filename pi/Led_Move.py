import time
import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(0)

#print("neopixels walk")

clock_pin = 19
data_pin = 26

GPIO.setup(clock_pin, GPIO.OUT)
GPIO.setup(data_pin, GPIO.OUT)


def apa102_send_bytes(clock_pin, data_pin, bytes):
    """
    zend de bytes naar de APA102 LED strip die is aangesloten op de clock_pin en data_pin
    """
    for byte in bytes:
        for bit in byte:
            if bit == '1':
                GPIO.output(data_pin, GPIO.HIGH)
            elif bit == '0':
                GPIO.output(data_pin, GPIO.LOW)

            GPIO.output(clock_pin, GPIO.HIGH)
            GPIO.output(clock_pin, GPIO.LOW)


def apa102(clock_pin, data_pin, colors):
    """
    zend de colors naar de APA102 LED strip die is aangesloten op de clock_pin en data_pin

    De colors moet een list zijn, met ieder list element een list van 3 integers,
    in de volgorde [ blauw, groen, rood ].
    Iedere kleur moet in de range 0..255 zijn, 0 voor uit, 255 voor vol aan.

    bv: colors = [ [ 0, 0, 0 ], [ 255, 255, 255 ], [ 128, 0, 0 ] ]
    zet de eerste LED uit, de tweede vol aan (wit) en de derde op blauw, halve strekte.
    """
    apa102_send_bytes(clock_pin, data_pin,
                      [['0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0'],
                       ['0', '0', '0', '0', '0', '0', '0', '0'], ['0', '0', '0', '0', '0', '0', '0', '0']])

    for x in colors:
        binary = [['1', '1', '1', '1', '1', '1', '1', '1']]
        for y in x:
            binar = '{:08b}'.format(y)
            output_controlled = list(binar)
            binary.append(output_controlled)
        apa102_send_bytes(clock_pin, data_pin, binary)

    apa102_send_bytes(clock_pin, data_pin,
                      [['1', '1', '1', '1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1', '1', '1', '1'],
                       ['1', '1', '1', '1', '1', '1', '1', '1'], ['1', '1', '1', '1', '1', '1', '1', '1']])


blue = [8, 0, 0]
green = [0, 255, 0]
red = [0, 0, 255]


def colors(x, n, on, off):
    result = []
    for i in range(0, n):
        if i == x:
            result.append(on)
        else:
            result.append(off)
    return result


def walk(clock_pin, data_pin, delay, n=8):

    for x in range(0, n):
        apa102(clock_pin, data_pin, colors(x, n,[0,0,255],[0,0,0]))#x, n, red, blue)
        time.sleep(delay)
    for x in range(n - 1, 1, -1):
        apa102(clock_pin, data_pin, colors(x, n, [0,0,255],[0,0,0]))#x, n, red, blue
        time.sleep(delay)
    for x in range(0, n):
        apa102(clock_pin, data_pin, colors(x, n,[0,0,255],[0,0,0]))#x, n, red, blue)
        time.sleep(delay)
    for x in range(n - 1, 1, -1):
        apa102(clock_pin, data_pin, colors(x, n, [0,0,255],[0,0,0]))#x, n, red, blue
        time.sleep(delay)

def kitt(clock_pin, data_pin, delay, n=8):

    for x in range(0, n, 1):
        apa102(clock_pin, data_pin, colors(x, n, [0, 255, 0], [0, 0, 0]))
        time.sleep(delay)
    for x in range(n -1, 1, -1):
        apa102(clock_pin, data_pin, colors(x, n, [255, 255, 0], [0, 0, 0]))
        time.sleep(delay)
    for x in range(0, n, 1):
        apa102(clock_pin, data_pin, colors(x, n, [255, 255, 0], [0, 0, 0]))
        time.sleep(delay)
    for x in range(n -1, 1, -1):
        apa102(clock_pin, data_pin, colors(x, n, [255, 255, 0], [0, 0, 0]))
        time.sleep(delay)
    for x in range(0, n, 1):
        apa102(clock_pin, data_pin, colors(x, n, [0, 255, 0], [0, 0, 0]))
        time.sleep(delay)
    for x in range(n -1, 1, -1):
        apa102(clock_pin, data_pin, colors(x, n, [0, 255, 0], [0, 0, 0]))
        time.sleep(delay)