import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BOARD)
gpio.setup(12, gpio.OUT) #enA
gpio.setup(32, gpio.OUT) #enB
motor1PWM = gpio.PWM(12, 100)
motor2PWM = gpio.PWM(32, 100)

def init() :
    gpio.setmode(gpio.BOARD)
    gpio.setup(7, gpio.OUT)
    gpio.setup(11, gpio.OUT)
    gpio.setup(13, gpio.OUT)
    gpio.setup(15, gpio.OUT)
    gpio.setup(18, gpio.IN)
    gpio.setup(16, gpio.IN)
    #sensor = gpio.setup(18, gpio.IN) #ir
    #gpio.setup(12, gpio.OUT) #enA
    #gpio.setup(32, gpio.OUT) #enB
    #motor1PWM = gpio.PWM(12, 100)
    #motor2PWM = gpio.PWM(32, 100)
    
    #gpio.output(12, True)
    #gpio.output(32, True)
    

def forward(tf) :
    init()
    motor1PWM.ChangeDutyCycle(60)
    motor2PWM.ChangeDutyCycle(60)
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(13, True)
    gpio.output(15, False)
    time.sleep(tf)
    gpio.cleanup()

def reverse(tf):
    init()
    motor1PWM.ChangeDutyCycle(60)
    motor2PWM.ChangeDutyCycle(60)
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    gpio.cleanup()

def turn_left(tf):
    init()
    motor1PWM.start(100)
    motor2PWM.start(100)
    gpio.output(7,  True)
    gpio.output(11, True)
    gpio.output(13, True )
    gpio.output(15, False)
    time.sleep(tf)
    gpio.cleanup()

def turn_right(tf):
    init()
    motor1PWM.start(100)
    motor2PWM.start(100)
    gpio.output(7,  False)
    gpio.output(11, True)
    gpio.output(13, False )
    gpio.output(15, False)
    time.sleep(tf)
    gpio.cleanup()

def pivot_left(tf):
    init()
    motor1PWM.ChangeDutyCycle(60)
    motor2PWM.ChangeDutyCycle(60)
    gpio.output(7,  True)
    gpio.output(11, False)
    gpio.output(13, True )
    gpio.output(15, False)
    time.sleep(tf)
    pio.cleanup()

def pivot_right(tf):
    init()
    motor1PWM.ChangeDutyCycle(60)
    motor2PWM.ChangeDutyCycle(60)
    gpio.output(7,  False)
    gpio.output(11, True)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    gpio.cleanup()
    
def stop():
    init()
    gpio.output(7,False)
    gpio.output(11,False)
    gpio.output(13,False)
    gpio.output(15,False)

    gpio.cleanup() 


def test():
    #forward(0.5225)
    #reverse(0.5225)
    #turn_left(2)
    #turn_right(0.5225)
    #pivot_right(0.48)
    #pivot_left(0.455)
    forward(1)
    stop()
    #gpio.cleanup() 

init()
test()
