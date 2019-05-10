import smbus
import time
 
import RPi.GPIO as gpio
 
PWR_M   = 0x6B
DIV   = 0x19
CONFIG   = 0x1A
GYRO_CONFIG  = 0x1B
INT_EN   = 0x38
ACCEL_X = 0x3B
ACCEL_Y = 0x3D
ACCEL_Z = 0x3F
GYRO_X  = 0x43
GYRO_Y  = 0x45
GYRO_Z  = 0x47

#compass
HXL = 0x03
HXH = 0x04
HYL = 0x05
HYH = 0x06
HZL = 0x07
HZH = 0x08

bus = smbus.SMBus(1)
Device_Address = 0x68   # device address
 
AxCal=0
AyCal=0
AzCal=0
GxCal=0
GyCal=0
GzCal=0
HxCal=0
HyCal=0
HzCal=0
 
def InitMPU():
    bus.write_byte_data(Device_Address, DIV, 7)
    bus.write_byte_data(Device_Address, PWR_M, 1)
    bus.write_byte_data(Device_Address, CONFIG, 0)
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 0) #24
    bus.write_byte_data(Device_Address, INT_EN, 1)
    time.sleep(1)
 
def readMPU(addr):
    high = bus.read_byte_data(Device_Address, addr)
    low = bus.read_byte_data(Device_Address, addr+1)
    value = ((high << 8) | low)
    if(value > 32768):
        value = value - 65536
    return value

def accel():
    x = readMPU(ACCEL_X)
    y = readMPU(ACCEL_Y)
    z = readMPU(ACCEL_Z)
     
    Ax = (x/16384.0-AxCal) 
    Ay = (y/16384.0-AyCal) 
    Az = (z/16384.0-AzCal)
     
    print ("X="+str(Ax))
    print ("Y="+str(Ay))
    print ("Z="+str(Az))
    #display(Ax,Ay,Az)
    time.sleep(.01)
 
def gyro():
  global GxCal
  global GyCal
  global GzCal
  x = readMPU(GYRO_X)
  y = readMPU(GYRO_Y)
  z = readMPU(GYRO_Z)
  Gx = x/131.0 - GxCal
  Gy = y/131.0 - GyCal
  Gz = z/131.0 - GzCal
  #print "X="+str(Gx)
  #display(Gx,Gy,Gz)
  print ("Gx="+str(Gx))
  print ("Gy="+str(Gy))
  print ("Gz="+str(Gz))
  
  time.sleep(.01)

def comp():
  global HxCal
  global HyCal
  global HzCal
  x = readMPU(HXL)
  y = readMPU(HYL)
  z = readMPU(HZL)
  Gx = x - GxCal
  Gy = y - GyCal
  Gz = z - GzCal
  
  print ("x="+str(x))
  print ("y="+str(y))
  print ("z="+str(z))
  
  time.sleep(.01)
 
def calibrate():
  global AxCal
  global AyCal
  global AzCal
  x=0
  y=0
  z=0
  for i in range(50):
      x = x + readMPU(ACCEL_X)
      y = y + readMPU(ACCEL_Y)
      z = z + readMPU(ACCEL_Z)
  x= x/50
  y= y/50
  z= z/50
  AxCal = x/16384.0
  AyCal = y/16384.0
  AzCal = z/16384.0
  
  print (AxCal)
  print (AyCal)
  print (AzCal)
 
  global GxCal
  global GyCal
  global GzCal
  x=0
  y=0
  z=0
  for i in range(50):
    x = x + readMPU(GYRO_X)
    y = y + readMPU(GYRO_Y)
    z = z + readMPU(GYRO_Z)
  x= x/50
  y= y/50
  z= z/50
  GxCal = x/131.0
  GyCal = y/131.0
  GzCal = z/131.0
 
  print (GxCal)
  print (GyCal)
  print (GzCal)
 
  #read info register of magnetometer
  print ("Info"+ str(readMPU(0x01)))
 
  global HxCal
  global HyCal
  global HzCal
  x=0
  y=0
  z=0
  for i in range(50):
    x = x + readMPU(HXL)
    y = y + readMPU(HYL)
    z = z + readMPU(HZL)
  x= x/50
  y= y/50
  z= z/50
  HxCal = x
  HyCal = y
  HzCal = z
 
  print (HyCal)
  print (HyCal)
  print (HzCal)
 
time.sleep(2)
InitMPU()
calibrate()
while 1:
  InitMPU()
  for i in range(100):
    comp()
  """Print("Accel")
  time.sleep(1)
  for i in range(100):
    accel()
    time.sleep(1)
  clear()"""
  """Print("Gyro")
  time.sleep(1)
  for i in range(50):
    gyro()
    time.sleep(0.5)
  clear()
  """