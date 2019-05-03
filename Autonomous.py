from Map import Map

positionX = 0
positionY = 0

front_o = 1
right_o = 2
back_o = 3
left_o = 4
orientation = front_o


p1 = Map()
p1.printMap()

#1 grid 30x30cm
#measure how many seconds for left/right,forward/backwards to move 1 grid
#forward & reverse 1 grid 0.5225 seconds and 60pwm(speed)
#rotate right/left 0.48 seconds/0.455
#turn right/left is do rotate right/left then forward

def forward():
    print("forward")
    positionY = positionY + 1

def back():
    print("back")
    positionY = positionY - 1

def right():
    print("right")
    positionX = positionX + 1
    shiftOrientation("right")

def left():
    print("left")
    positionX = positionX - 1
    shiftOrientation("left")

def rotate_right():
    print("pivot right")
    shiftOrientation("right")

def rotate_left():
    print("pivot left")
    shiftOrientation("left")

def stop():
    print("stop")

def shiftOrientation(newShift):
    if newShift == "left":
        orientation = orientation - 1
        if orientation < 1:
            orientation = 4
    elif newShift == "right":
        orientation = orientation + 1
        if orientation > 4:
            orientation = 1

def spontaneousAutonomous4ultrasonic(ultrasonicFD, ultrasonicRD, ultrasonicLD, ultrasonicBD):
    if ultrasonicFD > 30:
        forward(0.5225)
    elif ultrasonicRD > 30:
        right(0.48)
    elif ultrasonicBD > 30:
        back(0.5225)
    elif ultrasonicLD > 30:
        left(0.)
    else:
        stop()

def spontaneousAutonomous1ultrasonic(ultrasonic_distance):
    if ultrasonic_distance > 30:
        forward()
    else:
        rotate_right()

def autonomous4ultrasonicPlusMapGathering(ultrasonicFD, ultrasonicRD, ultrasonicLD,
                          ultrasonicBD, orientation):
    generateMapFrom1Point4Block(positionX, positionY, ultrasonicFD,
                                ultrasonicRD, ultrasonicLD, ultrasonicBD,
                                orientation)
    if ultrasonicFD > 30:
        forward()
    elif ultrasonicRD > 30:
        right()
    elif ultrasonicBD > 30:
        back()
    elif ultrasonicLD > 30:
        left()
    else:
        stop()