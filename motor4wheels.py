import RPi.GPIO as gpio
import time

def init() :
    gpio.setmode(gpio.BOARD)
    gpio.setup(7, gpio.OUT)
    gpio.setup(11, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    gpio.setup(15, gpio.OUT)

def forward(tf) :
    init()
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(13, True)
    gpio.output(15, False)
    time.sleep(tf)
    gpio.cleanup()

def reverse(tf):
    init()
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    gpio.cleanup()

def turn_left(tf):
    init()
    gpio.output(7,  True)
    gpio.output(11, True)
    gpio.output(13, True )
    gpio.output(15, False)
    time.sleep(tf)
    gpio.cleanup()


def turn_right(tf):
    init()
    gpio.output(7,  False)
    gpio.output(11, True)
    gpio.output(13, False )
    gpio.output(15, False)
    time.sleep(tf)
    gpio.cleanup()

def pivot_left(tf):
    init()
    gpio.output(7,  True)
    gpio.output(11, False)
    gpio.output(13, True )
    gpio.output(15, False)
    time.sleep(tf)
    gpio.cleanup()

def pivot_right(tf):
    init()
    gpio.output(7,  False)
    gpio.output(11, True)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    gpio.cleanup()﻿

def sensor_distance():
    gpio.setmode(gpio.BOARD)
    TRIG = 7
    ECHO = 12
    gpio.setup(TRIG, gpio.OUT)
    gpio.output(TRIG, 0)
    gpio.setup(ECHO, gpio.IN)
    time.sleep(0.1)
    print "Starting Measurement..."
    gpio.output(TRIG, 1)
    time.sleep(0.00001)
    gpio.output(TRIG, 0)
    while gpio.input(ECHO) == 0:
        pass
    start = time.time()
    while gpio.input(ECHO) == 1:
        pass
    stop = time.time()
    return (stop - start) * 17000
    #gpio.cleanup()
    
