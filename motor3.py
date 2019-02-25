import RPi.GPIO as GPIO
from time import sleep

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
 
def setup():
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
 
def loop():
	# Going forwards
	GPIO.output(Motor1A,GPIO.HIGH)
	GPIO.output(Motor1B,GPIO.LOW)
	GPIO.output(Motor1E,GPIO.HIGH)
	
	GPIO.output(Motor2A,GPIO.HIGH)
	GPIO.output(Motor2B,GPIO.LOW)
	
	GPIO.output(Motor3A,GPIO.HIGH)
	GPIO.output(Motor3B,GPIO.LOW)
	
	GPIO.output(Motor4A,GPIO.HIGH)
	GPIO.output(Motor4B,GPIO.LOW)
 
	#sleep(5)
 	# Going backwards
	#GPIO.output(Motor1A,GPIO.LOW)
	#GPIO.output(Motor1B,GPIO.HIGH)
	#GPIO.output(Motor1E,GPIO.HIGH)
	
	#GPIO.output(Motor2A,GPIO.HIGH)
	#GPIO.output(Motor2B,GPIO.LOW)
 	
        if GPIO.input(sensor) == GPIO.LOW :
             GPIO.output(Motor1E,GPIO.LOW)
             sleep(2)
             print("Stopped")
             GPIO.output(Motor1E,GPIO.HIGH)
            

def destroy():	
	GPIO.cleanup()

if __name__ == '__main__':     # Program start from here
	setup()
	while(1):#try:
    		loop()
  	#except KeyboardInterrupt:
		#destroy()
