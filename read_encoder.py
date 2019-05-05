#import RPi.GPIO as gpio
import time
import threading
from interruptingcow import timeout

gpio.setmode(gpio.BOARD)
gpio.setup(12, gpio.OUT) #enA
gpio.setup(32, gpio.OUT) #enB
motor1PWM = gpio.PWM(12, 100)
motor2PWM = gpio.PWM(32, 100)

def init() :
    gpio.setmode(gpio.BOARD)
    gpio.setup(7, gpio.OUT) #in1
    gpio.setup(11, gpio.OUT) #in2
    gpio.setup(13, gpio.OUT) #in3
    gpio.setup(15, gpio.OUT) #in4
    gpio.setup(18, gpio.IN)
    gpio.setup(16, gpio.IN)
    
    motor1PWM.start(80)
    motor2PWM.start(80)
    #sensor = gpio.setup(18, gpio.IN) #ir
    #gpio.setup(12, gpio.OUT) #enA
    #gpio.setup(32, gpio.OUT) #enB
    #motor1PWM = gpio.PWM(12, 100)
    #motor2PWM = gpio.PWM(32, 100)
    
    #gpio.output(12, True)
    #gpio.output(32, True)
    
def encoder_init():
    gpio.setmode(gpio.BOARD)
    gpio.setup(22, gpio.IN) #encoder 1
    gpio.setup(36, gpio.IN) #encoder 2

def forward(tf) :
    init()
    motor1PWM.ChangeDutyCycle(80)
    motor2PWM.ChangeDutyCycle(80)
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(13, True)
    gpio.output(15, False)
    time.sleep(tf)
    #gpio.cleanup()
    
def stop():
    init()
    gpio.output(7,False)
    gpio.output(11,False)
    gpio.output(13,False)
    gpio.output(15,False)

try:
    init()
    encoder_init()
    forward(1)
    with timeout(60, exception=RuntimeError):
         while True:
             enc1 = gpio.input(22)
             enc2 = gpio.input(36)
             print("enc1: " + str(enc1) + "enc2: " + str(enc2))

     stop()
except RuntimeError:
    stop()
    pass



































