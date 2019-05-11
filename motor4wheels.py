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

def F_ultrasonic_distance(): #front ultrasonic
    ultrasonic_init()
    time.sleep(0.1)
    
    """ gpio.setmode(gpio.BOARD)
    TRIG = 29
    ECHO = 31
    start = 0
    stop = 1
    gpio.setup(TRIG, gpio.OUT)
    gpio.output(TRIG, 0)
    gpio.setup(ECHO, gpio.IN) """
    
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

def L_ultrasonic_distance(): #left ultrasonic
    ultrasonic_init()
    time.sleep(0.1)
    
    start = 0
    stop = 1

    print ("Starting Measurement from LEFT ultrasonic...")
    gpio.output(29, 1)
    time.sleep(0.00001)
    gpio.output(29, 0)
    
    while (gpio.input(22) == 0):
        pass
    start = time.time()
    while (gpio.input(22) == 1):
        pass
    stop = time.time()
    #gpio.cleanup()
    return ((stop - start) * 17000 )

def R_ultrasonic_distance(): #right ultrasonic
    ultrasonic_init()
    time.sleep(0.1)
    
    start = 0
    stop = 1
    
    print ("Starting Measurement from RIGHT ultrasonic...")
    gpio.output(29, 1)
    time.sleep(0.00001)
    gpio.output(29, 0)
    
    while (gpio.input(36) == 0):
        pass
    start = time.time()
    while (gpio.input(36) == 1):
        pass
    stop = time.time()
    #gpio.cleanup()
    return ((stop - start) * 17000 )

def B_ultrasonic_distance(): #back ultrasonic
    ultrasonic_init()
    time.sleep(0.1)
    
    start = 0
    stop = 1

    print ("Starting Measurement from BACK ultrasonic...")
    gpio.output(29, 1)
    time.sleep(0.00001)
    gpio.output(29, 0)
    
    while (gpio.input(37) == 0):
        pass
    start = time.time()
    while (gpio.input(37) == 1):
        pass
    stop = time.time()
    #gpio.cleanup()
    return ((stop - start) * 17000 )

"""   
def ultrasonic2():
    gpio.setmode(gpio.BOARD)
    gpio.setup(29, gpio.OUT)
    gpio.setup(31, gpio.IN)
    
    nosig = 0
    sig = 0
    
    gpio.output(29, False)
    while gpio.input(31) == 0:
        nosig = time.time()
    
    while gpio.input(31) ==1:
        sig = time.time()
        
    tl = sig - nosig
    
    distance = tl/0.000058 #in cm
    
    gpio.cleanup()
    return distance
"""

def ir_sensor_init():
    #init()
    gpio.setmode(gpio.BOARD)
    gpio.setup(16, gpio.IN) #left ir
    gpio.setup(18, gpio.IN) #right ir
    
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
    forward(0.75)
    reverse(0.75)
    #turn_left(2)
    #turn_right(0.5225)
    pivot_right(1.044)
    pivot_left(0.455)
    stop()
    
def autonomous():
    init() 
    try:
        while 1:  
            sensor1 = gpio.input(18)
            sensor2 = gpio.input(16)
            if not sensor1 or not sensor2:
                print('OBSTACLE!')
                stop()
                reverse(1)
                time.sleep(0.5)
                pivot_right(1)
                stop()
                time.sleep(0.5)
            forward(0.5)
    except KeyboardInterrupt:
        stop()
        gpio.cleanup()
        pass

    
def autonomous_ultrasonic():
    init() 
    try:
        while 1:  
            distance = F_ultrasonic_distance()
            print(distance)
            init()
            if distance < 50.01:
                print('OBSTACLE!')
                stop()
                reverse(0.5225)
                stop()
                time.sleep(0.5)
                pivot_right(0.48)
                stop()
                time.sleep(0.5)
            forward(0.5225)
    except KeyboardInterrupt:
        stop()
        gpio.cleanup()
        pass
    
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
            
            

def spontaneousAutonomous1Ultrasonic(ultrasonic_distance, irL, irR, orientation, m):
    if ultrasonic_distance < 50 or not irL or not irR:
        #pivot_right(0.875)
        pivot_right(0.85)
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

def recordMovement():
    position = (positionX, positionY)
    record_movement.append(position)
    
def f(n):
    i = 0
    while(i<n):
        forward(0.5225)
        Stop(0.5)
        time.sleep(0.5)
    
def testrun():
    f(14)
    pivot_left(0.875)
    Stop(0.5)
    time.sleep(0.5)
    f(22)
    pivot_left(0.875)
    Stop(0.5)
    time.sleep(0.5)
    f(22)
    pivot_left(0.875)
    Stop(0.5)
    time.sleep(0.5)
    f(3)
    pivot_left(0.875)
    Stop(0.5)
    time.sleep(0.5)
    f(22)
    pivot_right(0.875)
    Stop(0.5)
    time.sleep(0.5)
    f(1)
    pivot_right(0.875)
    Stop(0.5)
    time.sleep(0.5)
    f(22)
    pivot_right(0.875)
    Stop(0.5)
    time.sleep(0.5)
    pivot_right(0.875)
    Stop(0.5)
    time.sleep(0.5)
    f(2)

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
            forward(0.55)
            fxy = forwardByOrientation(orientation)
            global positionX
            global positionY
            positionX = positionX + fxy[0]
            positionY = positionY + fxy[1]
            m.setMapSpotTraveled(positionX, positionY)
        else:
            spontaneousAutonomous1Ultrasonic(ultrasonicFD, ir_sensor1, ir_sensor2, orientation, m)
    elif nextStep == 2:
        pivot_right(0.85)
        shiftOrientation("right")
        if ultrasonicFD > 50 or not ir_sensor1 or not ir_sensor2:
            forward(0.55)
            fxy = forwardByOrientation(orientation)
            global positionX
            global positionY
            positionX = positionX + fxy[0]
            positionY = positionY + fxy[1]
            m.setMapSpotTraveled(positionX, positionY)
        else:
            spontaneousAutonomous1Ultrasonic(ultrasonicFD, ir_sensor1, ir_sensor2, orientation, m)
    elif nextStep == 3:
        pivot_left(0.85)
        shiftOrientation("left")
        pivot_left(0.85)
        shiftOrientation("left")
        if ultrasonicFD > 50 or not ir_sensor1 or not ir_sensor2:
            forward(0.55)
            fxy = forwardByOrientation(orientation)
            global positionX
            global positionY
            positionX = positionX + fxy[0]
            positionY = positionY + fxy[1]
            m.setMapSpotTraveled(positionX, positionY)
        else:
            spontaneousAutonomous1Ultrasonic(ultrasonicFD, ir_sensor1, ir_sensor2, orientation, m)
    elif nextStep == 2:
        pivot_left(0.85)
        shiftOrientation("left")
        if ultrasonicFD > 50 or not ir_sensor1 or not ir_sensor2:
            forward(0.55)
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

#init()
ultrasonic_init()
#gpio.cleanup()
ir_sensor_init()


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
    m.printMap()
    gpio.cleanup()


#autonomous()
#init()
#ir_sensor_init()
#while 1:
#sensor = gpio.setup(18, gpio.IN) #ir
#

#try:
#    while 1:
#        init()
#        sensor1 = gpio.input(18)
#        sensor2 = gpio.input(16)
#        if not sensor1 and not sensor2:
#            print('OBSTACLE!')
#            stop()
#            reverse(0.5)
#            time.sleep(0.5)
#            turn_right(1)
#            stop()
#            time.sleep(0.5)
#        forward(1)
        
#except KeyboardInterrupt:
#    stop()
#    gpio.cleanup()
#    pass

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
