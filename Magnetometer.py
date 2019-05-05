import smbus
import time
 
import RPi.GPIO as gpio
 
PWR_M   = 0x6B
DIV   = 0x19
CONFIG   = 0x1A
INT_PIN_CFG = 0x37
GYRO_CONFIG  = 0x1B
MAG_ID = 0x00 #Device ID
MAG_INFO = 0x01 #Information
MAG_CNTL1 = 0x0A #Control 1
MAG_CNTL2 = 0x0B #Control 2
MAG_ST1 = 0x02 #Status 1
MAG_ST2 = 0x09 #Status 2
MAG_ASTC = 0x0c #Self-test
INT_EN   = 0x38 #Interrupt Enable
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
Magnetometer_Address = 0x0c  
 
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
    bus.write_byte_data(Device_Address, PWR_M, 0x01)
    bus.write_byte_data(Device_Address, CONFIG, 0x00)
    bus.write_byte_data(Device_Address, GYRO_CONFIG, 0x00) #24
    bus.write_byte_data(Device_Address, INT_PIN_CFG, 0x22)
    #enable other chips to join the I2C network
    bus.write_byte_data(Device_Address, INT_EN, 0x01)
    #set bypass mode for magnetometer
    bus.write_byte_data(Device_Address, 0x37, 0x02)
    
    time.sleep(1)
    
def initMag():
    #request continuous magnetometer measurements in 16 bits, mode 1
    bus.write_byte_data(Magnetometer_Address, MAG_CNTL1, 0x12)
    #make sure self test is 0
    bus.write_byte_data(Magnetometer_Address, MAG_ASTC, 0)
    
def readMPU(addr):
    high = bus.read_byte_data(Device_Address, addr)
    time.sleep(0.01)
    low = bus.read_byte_data(Device_Address, addr+1)
    value = ((high << 8) | low)
    if(value > 32768):
        value = value - 65536
    return value

def I2Cread(addr, reg, bytes):
    data = []
    index = 0
    
    for i in bytes:
        data[index] = bus.read_byte_data(Device_Address, addr)
        index += 1
        
    return data

def readComp(addr):
    low = bus.read_byte_data(Magnetometer_Address, addr)
    time.sleep(0.01)
    high = bus.read_byte_data(Magnetometer_Address, addr+1)
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
  
  
  st1 = bus.read_byte_data(Magnetometer_Address, 0x02)
  #st2 = bus.read_byte_data(Magnetometer_Address, 0x09)
  while (not (st1 & 0x01)):
      st1 = bus.read_byte_data(Magnetometer_Address, 0x02)
      #print("st1:"+str(st1))
  #bus.write_byte_data(Magnetometer_Address, MAG_CNTL1, 0x12)
  
  x = 0
  y = 0
  z = 0
      
  for i in range(50):
      #bus.write_byte_data(Magnetometer_Address, MAG_CNTL1, 0x12)
      x = x+readComp(HXL)
      y = y+readComp(HYL)
      z = z+readComp(HZL)
  Hx = (x/50) #- HxCal
  Hy = (y/50) #- HyCal
  Hz = (z/50) #- HzCal
  
  print ("x="+str(Hx))
  print ("y="+str(Hy))
  print ("z="+str(Hz))
  
  #time.sleep(.01)
 
def calibrate():
  """global AxCal
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
  """
  #read info register of magnetometer
  print ("Device ID"+ str(readComp(0x00)) + '\n')
  print ("Info"+ str(readComp(0x01)))
 
  global HxCal
  global HyCal
  global HzCal
  x=0
  y=0
  z=0
  for i in range(25):
    x = x + readComp(HXL)
    y = y + readComp(HYL)
    z = z + readComp(HZL)
  x= x/50
  y= y/50
  z= z/50
  HxCal = x
  HyCal = y
  HzCal = z
 
  print (HyCal)
  print (HyCal)
  print (HzCal)

def conv(self, msb, lsb):
    value = lsb | (msb << 8)
    
    return ctypes.c_short(value).value

"""
time.sleep(2)
InitMPU()
calibrate()
while 1:
  InitMPU()
  for i in range(10):
    comp()
  print("Accel")
  time.sleep(1)
  for i in range(10):
    accel()
    time.sleep(1)
  print("Gyro")
  time.sleep(1)
  for i in range(10):
    gyro()
    time.sleep(0.5)
"""
def test():
    try:
        InitMPU()
        initMag()
        calibrate()
        print("\n")
        while 1:
            initMag()
            #calibrate()
            print("data:")
            comp()
            time.sleep(0.05)
            #gpio.cleanup()
            print("\n")
    except KeyboardInterrupt:
        gpio.cleanup()
            
"""try:
    InitMPU()
    calibrate()
    while 1:
        comp()
        time.sleep(0.5)
    
except KeyboardInterrupt:
    gpio.cleanup()
"""