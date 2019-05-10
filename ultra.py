import RPi.GPIO as gpio
import time

def ultrasonic_distance():
    gpio.setmode(gpio.BOARD)
    TRIG = 29
    ECHO = 31
    gpio.setup(TRIG, gpio.OUT)
    gpio.output(TRIG, 0)
    gpio.setup(ECHO, gpio.IN)
    time.sleep(0.1)
    print ("Starting Measurement...")
    gpio.output(TRIG, 1)
    time.sleep(0.00001)
    gpio.output(TRIG, 0)
    while gpio.input(ECHO) == 0:
        pass
    start = time.time()
    while gpio.input(ECHO) == 1:
        pass
    stop = time.time()
    gpio.cleanup()
    return ((stop - start) * 17000 )

while(1):
    print(ultrasonic_distance())
    time.sleep(0.5)