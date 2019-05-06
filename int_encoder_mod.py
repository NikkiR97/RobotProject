import RPi.GPIO as gpio
import time
import threading
from interruptingcow import timeout

gpio.setmode(gpio.BOARD)
gpio.setup(12, gpio.OUT) #enA
gpio.setup(32, gpio.OUT) #enB
motor1PWM = gpio.PWM(12, 100)
motor2PWM = gpio.PWM(32, 100)

global counter1
global counter2
global direction
direction = True

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

    
def encoder_init():
    global counter1
    global counter2
    counter1 = 0
    counter2 = 0
    gpio.setmode(gpio.BOARD)
    #gpio.setup(22, gpio.IN) #encoder 1
    #gpio.setup(36, gpio.IN) #encoder 2
    gpio.setup(22, gpio.IN, pull_up_down=gpio.PUD_DOWN) #enc1
    gpio.setup(36, gpio.IN, pull_up_down=gpio.PUD_DOWN) #enc2

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
    
def adjust_right_wheels(tf):
    init()
    motor1PWM.ChangeDutyCycle(100)
    motor2PWM.ChangeDutyCycle(100)
    gpio.output(7,  True)
    gpio.output(11, True)
    gpio.output(13, True )
    gpio.output(15, False)
    time.sleep(tf)
    
def adjust_left_wheels(tf):
    init()
    motor1PWM.ChangeDutyCycle(100)
    motor2PWM.ChangeDutyCycle(100)
    gpio.output(7,  False)
    gpio.output(11, True)
    gpio.output(13, False)
    gpio.output(15, False)
    time.sleep(tf)

def adjust_right_wheels_b(tf):
    init()
    motor1PWM.ChangeDutyCycle(80)
    motor2PWM.ChangeDutyCycle(80)
    gpio.output(7,  True)
    gpio.output(11, True)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    #gpio.cleanup()

def adjust_left_wheels_b(tf):
    init()
    motor1PWM.ChangeDutyCycle(80)
    motor2PWM.ChangeDutyCycle(80)
    gpio.output(7,  True)
    gpio.output(11, False)
    gpio.output(13, True)
    gpio.output(15, True)
    time.sleep(tf)

def stop():
    init()
    gpio.output(7,False)
    gpio.output(11,False)
    gpio.output(13,False)
    gpio.output(15,False)

def Stop(tf):
    init()
    gpio.output(7,False)
    gpio.output(11,False)
    gpio.output(13,False)
    gpio.output(15,False)
    time.sleep(tf)

def my_callback1(channel):
    #print("edge 1!")
    global counter1
    global direction
    
    if(direction == True):
        counter1 = counter1 + 1
    else:
        counter1 = counter1 - 1
   
def my_callback2(channel):
    #print("edge 2!")
    global counter2
    global direction
    if(direction == True):
        counter2 = counter2 + 1
    else:
        counter2 = counter2 - 1
    
def test():
    adjust_right_wheels(1)
    adjust_right_wheels_b(1)
    stop()

init()
encoder_init()

gpio.add_event_detect(22, gpio.FALLING, callback=my_callback1)
gpio.add_event_detect(36, gpio.FALLING, callback=my_callback2)

try:
    direction = True
    forward(0.4) #read as 39
    counter1 = 0
    counter2 = 0
    while((counter1 != 40) or (counter2!=40)):
        print("count: " + str(counter1) + " " + str(counter2) + "\n")
        if(counter1<40 or counter1>40):
            if (counter1<40):
                direction = True
                print("left forward")
                adjust_left_wheels(0.02)
            elif (counter1>40):
                direction = False
                print("left back")
                adjust_left_wheels_b(0.02)
        if(counter2<40 or counter2>40):
            if (counter2<40):
                direction = True
                print("right forward")
                adjust_right_wheels(0.02)
            elif (counter2>40):
                direction = False
                print("right back")
                adjust_right_wheels_b(0.02)
        Stop(0.1)

    #adjust_right_wheels_b(0.02)

except KeyboardInterrupt:
    stop()
    gpio.cleanup()
    
stop()
print("enc1: " + str(counter1) + " enc2: " + str(counter2))
gpio.cleanup()
