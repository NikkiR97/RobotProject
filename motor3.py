import RPi.GPIO as GPIO
import time

# Pins for Motor Driver Inputs 
Motor1A = 24
Motor1B = 23
Motor1E = 25

Motor2A = 27
Motor2B = 22

Motor3A = 5
Motor3B = 6

Motor4A = 26
Motor4B = 16

sensor = 17

TRIG = 18
ECHO = 12

 
def init():
    GPIO.setmode(GPIO.BCM)				# GPIO Numbering
    GPIO.setup(Motor1A,GPIO.OUT)  # All pins as Outputs
    GPIO.setup(Motor1B,GPIO.OUT)
    GPIO.setup(Motor1E,GPIO.OUT)
    
    GPIO.setup(Motor2A,GPIO.OUT)  # All pins as Outputs
    GPIO.setup(Motor2B,GPIO.OUT)
    
    GPIO.setup(Motor3A,GPIO.OUT)  # All pins as Outputs
    GPIO.setup(Motor3B,GPIO.OUT)
    
    GPIO.setup(Motor4A,GPIO.OUT)  # All pins as Outputs
    GPIO.setup(Motor4B,GPIO.OUT)
    
    GPIO.setup(sensor,GPIO.IN)

def forward(tf) :
    init()
    GPIO.output(Motor1A, True)
    GPIO.output(Motor1B, False)
    GPIO.output(Motor2A, True)
    GPIO.output(Motor2B, False)
    
    GPIO.output(Motor3A, True)
    GPIO.output(Motor3B, False)
    GPIO.output(Motor4A, True)
    GPIO.output(Motor4B, False)
    
    sleep(tf)
    GPIO.cleanup()

def reverse(tf):
    init()
    GPIO.output(Motor1A, False)
    GPIO.output(Motor1B, True)
    GPIO.output(Motor2A, False)
    GPIO.output(Motor2B, True)
    
    GPIO.output(Motor3A, False)
    GPIO.output(Motor3B, True)
    GPIO.output(Motor4A, False)
    GPIO.output(Motor4B, True)
    
    time.sleep(tf)
    GPIO.cleanup()

def turn_left(tf):
    init()
    GPIO.output(Motor1A, True)
    GPIO.output(Motor1B, True)
    GPIO.output(Motor2A, True)
    GPIO.output(Motor2B, True)
    
    GPIO.output(Motor3A, True)
    GPIO.output(Motor3B, False)
    GPIO.output(Motor4A, True)
    GPIO.output(Motor4B, False)
    
    time.sleep(tf)
    GPIO.cleanup()


def turn_right(tf):
    init()
    GPIO.output(Motor1A, True)
    GPIO.output(Motor1B, False)
    GPIO.output(Motor2A, True)
    GPIO.output(Motor2B, False)
    
    GPIO.output(Motor3A, False)
    GPIO.output(Motor3B, False)
    GPIO.output(Motor4A, False)
    GPIO.output(Motor4B, False)
    
    time.sleep(tf)
    GPIO.cleanup()

def pivot_left(tf):
    init()
    GPIO.output(Motor1A, False)
    GPIO.output(Motor1B, True)
    GPIO.output(Motor2A, False)
    GPIO.output(Motor2B, True)
    
    GPIO.output(Motor3A, True)
    GPIO.output(Motor3B, False)
    GPIO.output(Motor4A, True)
    GPIO.output(Motor4B, False)

    time.sleep(tf)
    GPIO.cleanup()

def pivot_right(tf):
    init()
    GPIO.output(Motor1A, False)
    GPIO.output(Motor1B, True)
    GPIO.output(Motor2A, False)
    GPIO.output(Motor2B, True)
    
    GPIO.output(Motor3A, True)
    GPIO.output(Motor3B, False)
    GPIO.output(Motor4A, True)
    GPIO.output(Motor4B, False)
    
    time.sleep(tf)
    GPIO.cleanup()


def stop():
    GPIO.output(Motor1A,GPIO.LOW)
    GPIO.output(Motor1B,GPIO.LOW)
    GPIO.output(Motor2A,GPIO.LOW)
    GPIO.output(Motor2B,GPIO.LOW)
    GPIO.output(Motor3A,GPIO.LOW)
    GPIO.output(Motor3B,GPIO.LOW)
    GPIO.output(Motor4A,GPIO.LOW)
    GPIO.output(Motor4B,GPIO.LOW)
    GPIO.cleanup()
 
def sensor_distance():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(TRIG, GPIO.OUT)
    GPIO.output(TRIG, 0)
    GPIO.setup(ECHO, GPIO.IN)
    time.sleep(0.1)
    print ("Starting Measurement...")
    GPIO.output(TRIG, 1)
    time.sleep(1)
    GPIO.output(TRIG, 0)
    while GPIO.input(ECHO) == 0:
        pass
    start = time.time()
    while GPIO.input(ECHO) == 1:
        pass
    stop = time.time()
    print ((stop - start) * 17000)
    GPIO.cleanup()
 

#main
init()
try:
    while 1:
        sensor_distance()
    #while 1:
      #  print ("forward!")
      #  forward(5)
      #  print ("turn right!")
      #  turn_right(5)
      #  print ("pivot right!")
      #  pivot_right(5)
      #  print ("turn left!")
      #  turn_left(5)
      #  print ("pivot left!")
      #  pivot_left(5)
      #  print ("Reverse!")
      #  reverse(5)
        #destroy()
except KeyboardInterrupt:
    stop()
    pass
