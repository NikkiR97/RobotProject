import RPi.GPIO as gpio
import time
from Map import Map

global positionX
global positionY
positionX = 50
positionY = 50

front_o = 1
right_o = 2
back_o = 3
left_o = 4
global orientation
orientation = front_o

gpio.setmode(gpio.BOARD)
gpio.setup(12, gpio.OUT) #enA
gpio.setup(32, gpio.OUT) #enB
motor1PWM = gpio.PWM(12, 100)
motor2PWM = gpio.PWM(32, 100)


###################################
#         MOTOR FUNCTIONS         #
###################################

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
    
def stop():
    init()
    gpio.output(7,False)
    gpio.output(11,False)
    gpio.output(13,False)
    gpio.output(15,False)

    #gpio.cleanup()
    
def Stop(tf):
    init()
    gpio.output(7,False)
    gpio.output(11,False)
    gpio.output(13,False)
    gpio.output(15,False)
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


###################################
#       INFRARED FUNCTIONS        #
###################################

def ir_sensor_init():
    #init()
    gpio.setmode(gpio.BOARD)
    gpio.setup(16, gpio.IN) #left ir
    gpio.setup(18, gpio.IN) #right ir
    
    time.sleep(0.1)

###################################
#      ULTRASONIC FUNCTIONS       #
###################################  
    
def ultrasonic_init() :
    gpio.setmode(gpio.BOARD)
    
    TRIG = 29 #trig is the same for all ultrasonic sensors
    gpio.setup(TRIG, gpio.OUT)
    gpio.output(TRIG, 0)
    
   # ECHO values: front=31, left=22, right=36, back=37
    gpio.setup(31, gpio.IN)
    gpio.setup(22, gpio.IN) #using encoder left 
    gpio.setup(36, gpio.IN) #using encoder right
    gpio.setup(37, gpio.IN)

def F_ultrasonic_distance(): #front ultrasonic
    ultrasonic_init()
    time.sleep(0.1)
    
    start = 0
    stop = 1
    
    print ("Starting Measurement from FRONT ultrasonic...")
    gpio.output(29, 1) #enable trigger
    time.sleep(0.00001)
    gpio.output(29, 0) #disable trigger
    
    while (gpio.input(31) == 0):
        pass
    start = time.time()
    while (gpio.input(31) == 1):
        pass
    stop = time.time()
    #gpio.cleanup()
    return ((stop - start) * 17000 )

###################################
#       ENCODER FUNCTIONS         #
###################################
    
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
            adjust_right_wheels(.025, direction)
        elif (difference < -threshold): #right wheels faster than left wheels
            adjust_left_wheels(.025, direction)
        difference = counter1 - counter2 


###################################
#       MAPPING FUNCTIONS         #
###################################

def shiftOrientation(newShift):
    global orientation
    if newShift == "left":
        orientation = orientation - 1
        if orientation < 1:
            orientation = 4
    elif newShift == "right":
        orientation = orientation + 1
        if orientation > 4:
            orientation = 1
            
def forwardByOrientation(orientation):
    f = (0, 1) #(x, y)
    if orientation == 1:
        f = (0, 1)
    elif orientation == 2:
        f = (1, 0)
    elif orientation == 3:
        f = (0, -1)
    elif orientation == 4:
        f = (-1, 0)
    return f            

def spontaneousAutonomous1Ultrasonic(ultrasonic_distance, irL, irR, orientation, m):
    if ultrasonic_distance < 50 or not irL or not irR:
        #pivot_right(0.875)
        pivot_right(0.9)
        shiftOrientation("right")
        #print(sensor1)
        #print(sensor2)
    else:
        #forward(0.5225)
        forward(0.55)
        fxy = forwardByOrientation(orientation)
        global positionX
        global positionY
        positionX = positionX + fxy[0]
        positionY = positionY + fxy[1]
        m.setMapSpotTraveled(positionX, positionY)
    
    callibrate_orientation(0, "forward") # set the chosen threshold for the encoders and direction of movement
    

def autonomousPath(map, ultrasonicFD, orientation, ir_sensor1, ir_sensor2, m):
    #generateMapFrom1Point4Block(positionX, positionY, ultrasonicFD,
    #                            ultrasonicRD, ultrasonicLD, ultrasonicBD,
    #                            orientation)
    nextLoc = map.getNextLoc(positionX, positionY)
    nextStep = map.nextStep((positionX, positionY), nextLoc, orientation)
    print("next location")
    print(nextLoc)
    print("next step")
    print(nextStep)
    print("prev orientation")
    print(orientation)
    if nextStep == 1:
        if ultrasonicFD > 50 or not ir_sensor1 or not ir_sensor2:
            forward(0.5225)
            fxy = forwardByOrientation(orientation)
            global positionX
            global positionY
            positionX = positionX + fxy[0]
            positionY = positionY + fxy[1]
            m.setMapSpotTraveled(positionX, positionY)
        else:
            spontaneousAutonomous1Ultrasonic(ultrasonicFD, ir_sensor1, ir_sensor2, orientation, m)
    elif nextStep == 2:
        pivot_right(0.875)
        shiftOrientation("right")
        if ultrasonicFD > 50 or not ir_sensor1 or not ir_sensor2:
            forward(0.5225)
            fxy = forwardByOrientation(orientation)
            global positionX
            global positionY
            positionX = positionX + fxy[0]
            positionY = positionY + fxy[1]
            m.setMapSpotTraveled(positionX, positionY)
        else:
            spontaneousAutonomous1Ultrasonic(ultrasonicFD, ir_sensor1, ir_sensor2, orientation, m)
    elif nextStep == 3:
        pivot_left(0.875)
        shiftOrientation("left")
        pivot_left(0.875)
        shiftOrientation("left")
        if ultrasonicFD > 50 or not ir_sensor1 or not ir_sensor2:
            forward(0.5225)
            fxy = forwardByOrientation(orientation)
            global positionX
            global positionY
            positionX = positionX + fxy[0]
            positionY = positionY + fxy[1]
            m.setMapSpotTraveled(positionX, positionY)
        else:
            spontaneousAutonomous1Ultrasonic(ultrasonicFD, ir_sensor1, ir_sensor2, orientation, m)
    elif nextStep == 2:
        pivot_left(0.875)
        shiftOrientation("left")
        if ultrasonicFD > 50 or not ir_sensor1 or not ir_sensor2:
            forward(0.5225)
            fxy = forwardByOrientation(orientation)
            global positionX
            global positionY
            positionX = positionX + fxy[0]
            positionY = positionY + fxy[1]
            m.setMapSpotTraveled(positionX, positionY)
        else:
            spontaneousAutonomous1Ultrasonic(ultrasonicFD, ir_sensor1, ir_sensor2, orientation, m)
    else:
        spontaneousAutonomous1Ultrasonic(ultrasonicFD, ir_sensor1, ir_sensor2, orientation, m)
        
    callibrate_orientation(0, "forward") # set the chosen threshold for the encoders and direction of movement    
        
        

#init()
ultrasonic_init()
ir_sensor_init()
encoder_init()

gpio.add_event_detect(22, gpio.FALLING, callback=L_encoder_callback)
gpio.add_event_detect(36, gpio.FALLING, callback=R_encoder_callback)
try:
    m = Map()
    while 1:
        distanceF= F_ultrasonic_distance()
        #distanceR = R_ultrasonic_distance()
        #distanceB = B_ultrasonic_distance()
        #distanceL = L_ultrasonic_distance()
        gpio.setmode(gpio.BOARD)
        irL = gpio.input(16)
        irR = gpio.input(18)
        print(distanceF)
        #init()
        m.generateMapFrom1Point4BlockX(positionX, positionY, distanceF, irL, irR, orientation)
        #autonomous_ultrasonic()
        #spontaneousAutonomous1Ultrasonic(distanceF, irL, irR, orientation, m)
        autonomousPath(m, distanceF, orientation, irL, irR, m)
        #gpio.cleanup()
        Stop(0.5)
        time.sleep(0.5)
except KeyboardInterrupt:
    stop()
    #m.printMap()
    print("enc1: " + str(counter1) + " enc2: " + str(counter2))
    gpio.cleanup()






'''
import RPi.GPIO as gpio
import time
from Map import Map
#from interruptingcow import timeout

global positionX
global positionY
positionX = 0
positionY = 0

front_o = 1
right_o = 2
back_o = 3
left_o = 4
orientation = front_o

global counter1
global counter2


gpio.setmode(gpio.BOARD)
gpio.setup(12, gpio.OUT) #enA
gpio.setup(32, gpio.OUT) #enB
motor1PWM = gpio.PWM(12, 100)
motor2PWM = gpio.PWM(32, 100)


###################################
#         MOTOR FUNCTIONS         #
###################################

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

def pivot_left(tf):
    init()
    motor1PWM.ChangeDutyCycle(80)
    motor2PWM.ChangeDutyCycle(80)
    gpio.output(7,  True)
    gpio.output(11, False)
    gpio.output(13, True )
    gpio.output(15, False)
    time.sleep(tf)

def pivot_right(tf):
    init()
    motor1PWM.ChangeDutyCycle(80)
    motor2PWM.ChangeDutyCycle(80)
    gpio.output(7,  False)
    gpio.output(11, True)
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

###################################
#       INFRARED FUNCTIONS        #
###################################

def ir_sensor_init():
    #init()
    gpio.setmode(gpio.BOARD)
    gpio.setup(16, gpio.IN) #left ir
    gpio.setup(18, gpio.IN) #right ir
    
    time.sleep(0.1)

###################################
#      ULTRASONIC FUNCTIONS       #
###################################
    
def ultrasonic_init() :
    gpio.setmode(gpio.BOARD)
    
    TRIG = 29 #trig is the same for all ultrasonic sensors
    gpio.setup(TRIG, gpio.OUT)
    gpio.output(TRIG, 0)
    
   # ECHO values: front=31, left=22, right=36, back=37
    gpio.setup(31, gpio.IN)
    #gpio.setup(22, gpio.IN) #using encoder left 
    #gpio.setup(36, gpio.IN) #using encoder right
    gpio.setup(37, gpio.IN)

def F_ultrasonic_distance(): #front ultrasonic
    ultrasonic_init()
    time.sleep(0.1)
    
    start = 0
    stop = 1
    
    print ("Starting Measurement from FRONT ultrasonic...")
    gpio.output(29, 1) #enable trigger
    time.sleep(0.00001)
    gpio.output(29, 0) #disable trigger
    
    while (gpio.input(31) == 0):
        pass
    start = time.time()
    while (gpio.input(31) == 1):
        pass
    stop = time.time()
    #gpio.cleanup()
    return ((stop - start) * 17000 )

###################################
#       ENCODER FUNCTIONS         #
###################################
    
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
            adjust_right_wheels(.025, direction)
        elif (difference < -threshold): #right wheels faster than left wheels
            adjust_left_wheels(.025, direction)
        difference = counter1 - counter2 

###################################
#       MAPPING FUNCTIONS         #
###################################

def shiftOrientation(newShift):
    global orientation
    if newShift == "left":
        orientation = orientation - 1
        if orientation < 1:
            orientation = 4
    elif newShift == "right":
        orientation = orientation + 1
        if orientation > 4:
            orientation = 1

def forwardByOrientation(orientation):
    f = (0, 1) #(x, y)
    if orientation == 1:
        f = (0, 1)
    elif orientation == 2:
        f = (1, 0)
    elif orientation == 3:
        f = (0, -1)
    elif orientation == 4:
        f = (-1, 0)
    return f

def spontaneousAutonomous1Ultrasonic(ultrasonic_distance, irL, irR, orientation, m):
    if ultrasonic_distance < 50 or not irL or not irR:
        #pivot_right(0.875)
        pivot_right(0.775)
        shiftOrientation("right")
        #print(sensor1)
        #print(sensor2)
    else:
        #forward(0.5225)
        forward(0.55)
        fxy = forwardByOrientation(orientation)
        global positionX
        global positionY
        positionX = positionX + fxy[0]
        positionY = positionY + fxy[1]
        m.setMapSpotTraveled(positionX, positionY)
        
    callibrate_orientation(0, "forward") # set the chosen threshold for the encoders and direction of movement

def autonomousPath(map, ultrasonicFD, orientation, ir_sensor1, ir_sensor2, m):
    #generateMapFrom1Point4Block(positionX, positionY, ultrasonicFD,
    #                            ultrasonicRD, ultrasonicLD, ultrasonicBD,
    #                            orientation)
    nextLoc = map.getNextLoc(positionX, positionY)
    nextStep = map.nextStep((positionX, positionY), nextLoc, orientation)
    print("next location")
    print(nextLoc)
    print("next step")
    print(nextStep)
    print("prev orientation")
    print(orientation)
    if nextStep == 1:
        if ultrasonicFD > 50 or not ir_sensor1 or not ir_sensor2:
            forward(0.5225)
            fxy = forwardByOrientation(orientation)
            global positionX
            global positionY
            positionX = positionX + fxy[0]
            positionY = positionY + fxy[1]
            m.setMapSpotTraveled(positionX, positionY)
        else:
            spontaneousAutonomous1Ultrasonic(ultrasonicFD, ir_sensor1, ir_sensor2, orientation, m)
    elif nextStep == 2:
        pivot_right(0.875)
        shiftOrientation("right")
        if ultrasonicFD > 50 or not ir_sensor1 or not ir_sensor2:
            forward(0.5225)
            fxy = forwardByOrientation(orientation)
            global positionX
            global positionY
            positionX = positionX + fxy[0]
            positionY = positionY + fxy[1]
            m.setMapSpotTraveled(positionX, positionY)
        else:
            spontaneousAutonomous1Ultrasonic(ultrasonicFD, ir_sensor1, ir_sensor2, orientation, m)
    elif nextStep == 3:
        pivot_left(0.875)
        shiftOrientation("left")
        pivot_left(0.875)
        shiftOrientation("left")
        if ultrasonicFD > 50 or not ir_sensor1 or not ir_sensor2:
            forward(0.5225)
            fxy = forwardByOrientation(orientation)
            global positionX
            global positionY
            positionX = positionX + fxy[0]
            positionY = positionY + fxy[1]
            m.setMapSpotTraveled(positionX, positionY)
        else:
            spontaneousAutonomous1Ultrasonic(ultrasonicFD, ir_sensor1, ir_sensor2, orientation, m)
    elif nextStep == 2:
        pivot_left(0.875)
        shiftOrientation("left")
        if ultrasonicFD > 50 or not ir_sensor1 or not ir_sensor2:
            forward(0.5225)
            fxy = forwardByOrientation(orientation)
            global positionX
            global positionY
            positionX = positionX + fxy[0]
            positionY = positionY + fxy[1]
            m.setMapSpotTraveled(positionX, positionY)
        else:
            spontaneousAutonomous1Ultrasonic(ultrasonicFD, ir_sensor1, ir_sensor2, orientation, m)
    else:
        spontaneousAutonomous1Ultrasonic(ultrasonicFD, ir_sensor1, ir_sensor2, orientation, m)
        
    callibrate_orientation(0, "forward") # set the chosen threshold for the encoders and direction of movement



init()
ultrasonic_init()
ir_sensor_init()
encoder_init()

gpio.add_event_detect(22, gpio.FALLING, callback=L_encoder_callback)
gpio.add_event_detect(36, gpio.FALLING, callback=R_encoder_callback)

try:
    m = Map()
    
    
    #forward(0.55)
    #reverse(1.5)
    pivot_right(0.774)
    forward(0.55)
    callibrate_orientation(0, "forward") # set the chosen threshold for the encoders and direction of movement
    
    while 1:
        distanceF= F_ultrasonic_distance()
        irL = gpio.input(16)
        irR = gpio.input(18)
        print(distanceF)
        
        m.generateMapFrom1Point4BlockX(positionX, positionY, distanceF, irL, irR, orientation)
        autonomousPath(m, distanceF, orientation, irL, irR, m)
        
        stop()
        time.sleep(0.5)
            

except KeyboardInterrupt:
    stop()
    #m.printMap()
    gpio.cleanup()
    
stop()
print("enc1: " + str(counter1) + " enc2: " + str(counter2))
gpio.cleanup()
'''
