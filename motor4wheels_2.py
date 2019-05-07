import RPi.GPIO as gpio
import time
from Map import Map

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
global direction1
global direction2
global flag

direction1 = True
direction2 = True

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
    #gpio.setup(22, gpio.IN) #using encoder left 
    #gpio.setup(36, gpio.IN) #using encoder right
    gpio.setup(37, gpio.IN)

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

def my_callback1(channel):
    #print("edge 1!")
    global counter1
    global direction1
    
    if(direction1 == True):
        counter1 = counter1 + 1
    else:
        counter1 = counter1 - 1
   
def my_callback2(channel):
    #print("edge 2!")
    global counter2
    global direction2
    if(direction2 == True):
        counter2 = counter2 + 1
    else:
        counter2 = counter2 - 1

def forward(tf) :
    init()
    motor1PWM.ChangeDutyCycle(80)
    motor2PWM.ChangeDutyCycle(80)
    gpio.output(7, False)
    gpio.output(11, True)
    gpio.output(13, True)
    gpio.output(15, False)
    time.sleep(tf)
    
    direction1 = True
    direction2 = True
    counter1 = 0
    counter2 = 0
    
    """
    direction1 = True
    direction2 = True
    counter1 = 0
    counter2 = 0
    while((counter1 != 40) or (counter2!=40)):
        print("count: " + str(counter1) + " " + str(counter2) + "\n")
        if(counter1<40 or counter1>40):
            if (counter1<40):
                direction1 = True
                adjust_left_wheels(0.025)
            elif (counter1>40):
                direction1 = False
                adjust_left_wheels_b(0.025)
        if(counter2<40 or counter2>40):
            if (counter2<40):
                direction2 = True
                adjust_right_wheels(0.025)
            elif (counter2>40):
                direction2 = False
                adjust_right_wheels_b(0.025)
        Stop(0.25)
    """    
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
    
    direction1 = True
    direction2 = False
    counter1 = 0
    counter2 = 0
    
    """
    direction1 = True
    direction2 = False
    counter1 = 0
    counter2 = 0
    while((counter1 != 29) or (counter2!=-29)):
        print("count: " + str(counter1) + " " + str(counter2) + "\n")
        if(counter1<29 or counter1>29):
            if (counter1<29):
                direction1 = True
                adjust_left_wheels(0.025)
            elif (counter1>29):
                adjust_left_wheels_b(0.025)
        if(counter2<-31 or counter2>-31):
            if (counter2<-29):
                direction2 = True
                adjust_right_wheels(0.025)
            elif (counter2>-29):
                direction2 = False
                adjust_right_wheels_b(0.025)
        Stop(0.25)"""
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
            
            

def spontaneousAutonomous1Ultrasonic(ultrasonic_distance, irL, irR, orientation):
    global flag
    if ultrasonic_distance < 50 or not irL or not irR:
        #pivot_right(0.875)
        flag = False;
        pivot_right(0.7)
        shiftOrientation("right")
        #print(sensor1)
        #print(sensor2)
    else:
        #forward(0.5225)
        flag = True;
        forward(0.55)
        fxy = forwardByOrientation(orientation)
        global positionX
        global positionY
        positionX = positionX + fxy[0]
        positionY = positionY + fxy[1]
        
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

def autonomousPath(map, ultrasonicFD, ultrasonicRD, ultrasonicLD,
                          ultrasonicBD, orientation):
    #generateMapFrom1Point4Block(positionX, positionY, ultrasonicFD,
    #                            ultrasonicRD, ultrasonicLD, ultrasonicBD,
    #                            orientation)
    nextLoc = map.getNextLoc(positionX, positionY)
    nextStep = map.nextStep((positionX, positionY), nextLoc, orientation)
    if nextStep == 1:
        if ultrasonicFD > 50:
            forward(0.5225)
            fxy = forwardByOrientation(orientation)
            global positionX
            global positionY
            positionX = positionX + fxy[0]
            positionY = positionY + fxy[1]
        else:
            spontaneousAutonomous1Ultrasonic(ultrasonicFD, False, False, orientation)
    elif nextStep == 2:
        pivot_right(0.875)
        shiftOrientation("right")
        if ultrasonicFD > 50:
            forward(0.5225)
            fxy = forwardByOrientation(orientation)
            global positionX
            global positionY
            positionX = positionX + fxy[0]
            positionY = positionY + fxy[1]
        else:
            spontaneousAutonomous1Ultrasonic(ultrasonicFD, False, False, orientation)
    elif nextStep == 3:
        pivot_right(0.875)
        shiftOrientation("right")
        pivot_right(0.875)
        shiftOrientation("right")
        if ultrasonicFD > 50:
            forward(0.5225)
            fxy = forwardByOrientation(orientation)
            #global positionX
            #global positionY
            positionX = positionX + fxy[0]
            positionY = positionY + fxy[1]
        else:
            spontaneousAutonomous1Ultrasonic(ultrasonicFD, False, False, orientation)
    elif nextStep == 4:
        pivot_left(0.875)
        shiftOrientation("left")
        if ultrasonicFD > 50:
            forward()
            forward(0.5225)
            fxy = forwardByOrientation(orientation)
            global positionX
            global positionY
            positionX = positionX + fxy[0]
            positionY = positionY + fxy[1]
        else:
            spontaneousAutonomous1Ultrasonic(ultrasonicFD, False, False, orientation)
    else:
        spontaneousAutonomous1Ultrasonic(ultrasonicFD, False, False, orientation)

init()
ultrasonic_init()
ir_sensor_init()
encoder_init()

try:
    #m = Map()
    global flag
    gpio.add_event_detect(22, gpio.FALLING, callback=my_callback1)
    gpio.add_event_detect(36, gpio.FALLING, callback=my_callback2)
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
        #m.generateMapFrom1Point4Block(positionX, positionY, distanceF, distanceR,
         #                             distanceB, distanceL, orientation)
        #autonomous_ultrasonic()
        spontaneousAutonomous1Ultrasonic(distanceF, irL, irR, orientation)
        #autonomousPath(m, distanceF, distanceR, distanceL, distanceB, orientation)
        #gpio.cleanup()
        if(flag):
            val1 = 40
            val2 = 40
        else:
            val1 = 29
            val2 = -29
        #direction1 = True
        #direction2 = True
        #counter1 = 0
        #counter2 = 0
        while((counter1 != val1) or (counter2!=val2)):
            print("count: " + str(counter1) + " " + str(counter2) + "\n")
            if(counter1<val1 or counter1>val1):
                if (counter1<val1):
                    direction1 = True
                    print("left forward")
                    adjust_left_wheels(0.025)
                elif (counter1>val1):
                    direction1 = False
                    print("left back")
                    adjust_left_wheels_b(0.025)
            if(counter2<val2 or counter2>val2):
                if (counter2<val2):
                    direction2 = True
                    print("right forward")
                    adjust_right_wheels(0.025)
                elif (counter2>val2):
                    direction2 = False
                    print("right back")
                    adjust_right_wheels_b(0.025)
            Stop(0.25)
        
        Stop(0.5)
        time.sleep(0.5)
except KeyboardInterrupt:
    stop()
    #m.printMap()
    gpio.cleanup()


