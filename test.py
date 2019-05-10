import RPi.GPIO as GPIO
import time

#enA = 18
#enB = 12

#in1 = 17
#in2 = 27
#in3 = 22
#in4 = 23

# Pins for Motor Driver Inputs 
Motor1A = 7
Motor1B = 11

Motor2A = 13
Motor2B = 15

#Motor1E = 18
#Motor2E = 12

def init():
    GPIO.setmode(GPIO.BOARD)				# GPIO Numbering
    GPIO.setup(Motor1A, GPIO.OUT)  # All pins as Outputs
    GPIO.setup(Motor1B, GPIO.OUT)
    #GPIO.setup(Motor1E, GPIO.OUT)
    
    GPIO.setup(Motor2A, GPIO.OUT)  # All pins as Outputs
    GPIO.setup(Motor2B, GPIO.OUT)
    #GPIO.setup(Motor2E, GPIO.OUT)

def forward(tf) :
    init()
    #GPIO.output(Motor1E, True)
    #GPIO.output(Motor2E, True)
    
    GPIO.output(Motor1A, True)
    GPIO.output(Motor1B, True)
    GPIO.output(Motor2A, True)
    GPIO.output(Motor2B, False)
    
    
    time.sleep(tf)
    GPIO.cleanup()
    
forward(5)
