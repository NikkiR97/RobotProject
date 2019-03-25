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
    #gpio.cleanup()

def reverse(tf):
    init()
    motor1PWM.ChangeDutyCycle(60)
    motor2PWM.ChangeDutyCycle(60)
    gpio.output(7, True)
    gpio.output(11, False)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    #gpio.cleanup()

def turn_right(tf):
    init()
    motor1PWM.start(100)
    motor2PWM.start(100)
    gpio.output(7,  True)
    gpio.output(11, True)
    gpio.output(13, True )
    gpio.output(15, False)
    time.sleep(tf)
    #gpio.cleanup()

def turn_left(tf):
    init()
    motor1PWM.start(100)
    motor2PWM.start(100)
    gpio.output(7,  False)
    gpio.output(11, True)
    gpio.output(13, False )
    gpio.output(15, False)
    time.sleep(tf)
    #gpio.cleanup()

def pivot_left(tf):
    init()
    motor1PWM.ChangeDutyCycle(60)
    motor2PWM.ChangeDutyCycle(60)
    gpio.output(7,  True)
    gpio.output(11, False)
    gpio.output(13, True )
    gpio.output(15, False)
    time.sleep(tf)
    #pio.cleanup()

def pivot_right(tf):
    init()
    motor1PWM.ChangeDutyCycle(60)
    motor2PWM.ChangeDutyCycle(60)
    gpio.output(7,  False)
    gpio.output(11, True)
    gpio.output(13, False)
    gpio.output(15, True)
    time.sleep(tf)
    #gpio.cleanup()
    
def stop():
    init()
    gpio.output(7,False)
    gpio.output(11,False)
    gpio.output(13,False)
    gpio.output(15,False)

    #gpio.cleanup()

def ultrasonic_distance():
    gpio.setmode(gpio.BOARD)
    TRIG = 16
    ECHO = 18
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
    return (stop - start) * 17000
    gpio.cleanup()

def ir_sensor_init():
    init()
    gpio.setmode(gpio.BOARD)
    time.sleep(0.1)
    
def ir_sensor():
    #ir_sensor_init()
    sensor = gpio.input(18)
    if not sensor:
        print(1)
        #stop()
        #time.sleep(1)
        forward(1)
    else:
        print(0)
        stop()
        time.sleep(2)
        reverse(2)

def test():
    forward(2)
    reverse(2)
    turn_left(2)
    turn_right(2)
    stop()

#init()
#ir_sensor_init()
#while 1:
#sensor = gpio.setup(18, gpio.IN) #ir
#

try:
    while 1:
        init()
        #gpio.setmode(gpio.BOARD)
        sensor = gpio.input(18)
        
        #forward(1)
        
        
        if not sensor:
            print('OBSTACLE!')
            stop()
            time.sleep(0.5)
            reverse(0.5)
            time.sleep(0.5)
            turn_right(1)
            stop()

        forward(1)
        
except KeyboardInterrupt:
    stop()
    gpio.cleanup()
    pass

#i=0;
#sensor = gpio.input(18)
#while sensor==1:
    #sensor.input(18)
    #print(sensor)
    #if not sensor:
       # print(1)
        #stop()
        #time.sleep(1)
        #forward(1)
    #else:
        #print(0)
        #stop()
        #time.sleep(2)
        #reverse(2)
#stop()

#test()
#stop()
    #print(sensor)
#forward(1)
#if not sensor:
        #stop()
        #time.sleep(1)
        #turn_right(1)
#while 1:
    #forward(1)
    #ir_sensor()
