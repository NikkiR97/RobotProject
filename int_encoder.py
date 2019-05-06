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
    
def reverse(tf):
    init()
    motor1PWM.ChangeDutyCycle(80)
    motor2PWM.ChangeDutyCycle(80)
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    
def adjust_right_wheels(tf, direction):
    init()
    motor1PWM.ChangeDutyCycle(100)
    motor2PWM.ChangeDutyCycle(100)
    if (direction == "forward"):
        gpio.output(7,  True)
        gpio.output(11, True)
        gpio.output(13, True)
        gpio.output(15, False)
    elif (direction == "reverse"):
        gpio.output(7,  False)
        gpio.output(11, False)
        gpio.output(13, False)
        gpio.output(15, True)
    else:
        print("ERROR: unknown direction.")
        
    time.sleep(tf)
    
def adjust_left_wheels(tf, direction):
    init()
    motor1PWM.ChangeDutyCycle(100)
    motor2PWM.ChangeDutyCycle(100)
    if (direction == "forward"):
        gpio.output(7,  False)
        gpio.output(11, True)
        gpio.output(13, False)
        gpio.output(15, False)
    elif (direction == "reverse"):
        gpio.output(7,  True)
        gpio.output(11, False)
        gpio.output(13, True)
        gpio.output(15, True)
    else:
        print("ERROR: unknown direction.")
        
    time.sleep(tf)

def stop():
    init()
    gpio.output(7,False)
    gpio.output(11,False)
    gpio.output(13,False)
    gpio.output(15,False)

def L_encoder_callback(channel):
    #print("edge 1!")
    global counter1
    counter1 = counter1 + 1
   
def R_encoder_callback(channel):
    #print("edge 2!")
    global counter2
    counter2 = counter2 + 1
    
# compares each encoder and adjusts the wheels according to the set threshold    
def callibrate_orientation(threshold, direction):
    difference = counter1 - counter2
    while (abs(difference) > threshold): # while the encoders are above threshold difference, adjust accordingly
        if (difference > threshold): #left wheels faster than right wheels
            adjust_right_wheels(.3, direction)
        elif (difference < -threshold): #right wheels faster than left wheels
            adjust_left_wheels(.3, direction)
        difference = counter1 - counter2 

init()
encoder_init()

gpio.add_event_detect(22, gpio.FALLING, callback=L_encoder_callback)
gpio.add_event_detect(36, gpio.FALLING, callback=R_encoder_callback)

try:
    #forward(2)
    reverse(3)
    callibrate_orientation(5, "reverse") # set the chosen threshold for the encoders and direction of movement  
            

except KeyboardInterrupt:
    stop()
    gpio.cleanup()
    
stop()
print("enc1: " + str(counter1) + " enc2: " + str(counter2))
gpio.cleanup()

'''
try:
    init()
    encoder_init()
    forward(1)
    with timeout(1, exception=RuntimeError):
         while True:
             enc1 = gpio.input(22)
             if (enc1):
                 counter1 += 1
             enc2 = gpio.input(36)
             if (enc2):
                 counter2 += 1
             #print("enc1: " + str(enc1) + "enc2: " + str(enc2))
             print("enc1: " + str(counter1) + " enc2: " + str(counter2))

    #print("enc1: " + str(counter1) + "enc2: " + str(counter2))
    stop()
    
except RuntimeError:
    stop()
    pass
    
'''
