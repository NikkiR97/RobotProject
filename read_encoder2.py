import RPi.GPIO as gpio
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

def reverse(tf):
    init()
    motor1PWM.ChangeDutyCycle(80)
    motor2PWM.ChangeDutyCycle(80)
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    #gpio.cleanup()

def turn_left(tf):
    init()
    motor1PWM.ChangeDutyCycle(100)
    motor2PWM.ChangeDutyCycle(100)
    gpio.output(7,  True)
    gpio.output(11, True)
    gpio.output(13, True )
    gpio.output(15, False)
    time.sleep(tf)
    #gpio.cleanup()

def turn_right(tf):
    init()
    motor1PWM.ChangeDutyCycle(100)
    motor2PWM.ChangeDutyCycle(100)
    gpio.output(7,  False)
    gpio.output(11, True)
    gpio.output(13, False )
    gpio.output(15, False)
    time.sleep(tf)
    #gpio.cleanup()
    
def turn_left_b(tf):
    init()
    motor1PWM.ChangeDutyCycle(80)
    motor2PWM.ChangeDutyCycle(80)
    gpio.output(7,  True)
    gpio.output(11, True)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    #gpio.cleanup()

def turn_right_b(tf):
    init()
    motor1PWM.ChangeDutyCycle(80)
    motor2PWM.ChangeDutyCycle(80)
    gpio.output(7,  True)
    gpio.output(11, False)
    gpio.output(13, True)
    gpio.output(15, True)
    time.sleep(tf)
    #gpio.cleanup()

def pivot_left(tf):
    init()
    motor1PWM.ChangeDutyCycle(80)
    motor2PWM.ChangeDutyCycle(80)
    gpio.output(7,  True)
    gpio.output(11, False)
    gpio.output(13, True )
    gpio.output(15, False)
    time.sleep(tf)
    #pio.cleanup()

def pivot_right(tf):
    init()
    motor1PWM.ChangeDutyCycle(80)
    motor2PWM.ChangeDutyCycle(80)
    gpio.output(7,  False)
    gpio.output(11, True)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    #gpio.cleanup()
    
def Stop(tf):
    init()
    gpio.output(7,False)
    gpio.output(11,False)
    gpio.output(13,False)
    gpio.output(15,False)
    time.sleep(tf)

def tick_count(tf, j, i):
    
    try:
        with timeout(tf,exception=RuntimeError):
              print("begin count")
              while True:
                 enc2 = gpio.input(36)
                 enc1 = gpio.input(22)
                 #enc2 = gpio.input(36)
                 #print("enc1: " + str(enc1) + "enc2: " + str(enc2))
                 if(enc1):
                     i = i+1
                 if(enc2):
                     j = j+1
                
    except RuntimeError:
        stop()
        print("enc1 count" + str(i) + "\n")
        print("enc2 count" + str(j) + "\n")
    
    return i,j

def tick_count_b(tf, j, i):
    
    try:
        with timeout(tf, exception=RuntimeError):
              print("begin count")
              while True:
                 enc2 = gpio.input(36)
                 enc1 = gpio.input(22)
                 #enc2 = gpio.input(36)
                 #print("enc1: " + str(enc1) + "enc2: " + str(enc2))
                 if(enc1):
                     i = i-1
                 if(enc2):
                     j = j-1
                
    except RuntimeError:
        stop()
        print("enc1 count" + str(i) + "\n")
        print("enc2 count" + str(j) + "\n")
    
    return i,j

def test():
    init()
    #forward(0.75)
    #reverse(0.75)
    #turn_left(2)
    #turn_right(0.5225)
    #pivot_right(1.044)
    #pivot_left(0.455)
    #turn_left_b(0.5)
    turn_right_b(0.5)
    stop()

try:
    print("Begin program")
    init()
    encoder_init()
    k=0
    for k in range (0,3):    
        forward(0.3)
        
        i = 0
        j = 0
        i,j = tick_count(0.3, 0, 0)       
         
        print("enc1 count " + str(i) + "\n")
        print("enc2 count " + str(j) + "\n")
        
        while(not(i>= 11050 and i <= 11200) or not(i>= 11050 and i <= 11300)): 
            if (i<= 11055):
                turn_right(0.01)
                i,j = tick_count(0.01, j, i)
            elif (i>=11300):
                turn_right_b(0.01)
                i,j = tick_count_b(0.01, j, i)                
            if(j<=11055):
                turn_left(0.01)
                i,j = tick_count(0.01, j, i)
            elif (j>=11300):
                turn_left_b(0.01)
                i,j = tick_count_b(0.01, j, i)              
            Stop(0.25)
        Stop(0.25)   
    stop()
    #pass
except KeyboardInterrupt:
    stop()
    gpio.cleanup()


































