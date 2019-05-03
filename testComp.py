import time
import sys
import smbus
import RPi.GPIO as GPIO

FIFO_EN = 0x23

class I2C:

    def __init__(self, address, bus=smbus.SMBus(1)):
        self.address = address
        self.bus = bus
        self.misses = 0

    def writeByte(self, value):
        self.bus.write_byte(self.address, value)

    def write8(self, reg, value):
        self.bus.write_byte_data(self.address, reg, value)

    def writeList(self, reg, list):
        self.bus.write_i2c_block_data(self.address, reg, list)

    def readU8(self, reg):
        result = self.bus.read_byte_data(self.address, reg)
        return result

    def readS8(self, reg):
        result = self.bus.read_byte_data(self.address, reg)
        result = result - 256 if result > 127 else result
        return result

    def readU16(self, reg):
        hibyte = self.bus.read_byte_data(self.address, reg)
        result = (hibyte << 8) + self.bus.read_byte_data(self.address, reg+1)
        return result

    def readS16(self, reg):
        hibyte = self.bus.read_byte_data(self.address, reg)
        hibyte = hibyte - 256 if hibyte > 127 else hibyte
        result = (hibyte << 8) + self.bus.read_byte_data(self.address, reg+1)
        return result

    def readList(self, reg, length):
        "Reads a byte array value from the I2C device. The content depends on the device.  The "
        "FIFO read return sequential values from the same register.  For all other, sequestial"
        "regester values are returned"
        result = self.bus.read_i2c_block_data(self.address, reg, length)
        return result
    

def readList(reg, length):
    "Reads a byte array value from the I2C device. The content depends on the device.  The "
    "FIFO read return sequential values from the same register.  For all other, sequestial"
    "regester values are returned"
    result = self.bus.read_i2c_block_data(Device_Address, reg, length)
    return result

def flushFIFO():
    #-------------------------------------------------------------------------------------------
    # First shut off the feed in the FIFO.
    #-------------------------------------------------------------------------------------------
    self.i2c.write8(self.__MPU6050_RA_FIFO_EN, 0x00)

    #-------------------------------------------------------------------------------------------
    # Empty the FIFO by reading whatever is there
    #-------------------------------------------------------------------------------------------
    SMBUS_MAX_BUF_SIZE = 32

    fifo_bytes = self.i2c.readU16(self.__MPU6050_RA_FIFO_COUNTH)

    for ii in range(int(fifo_bytes / SMBUS_MAX_BUF_SIZE)):
        self.i2c.readList(self.__MPU6050_RA_FIFO_R_W, SMBUS_MAX_BUF_SIZE)

    fifo_bytes = self.i2c.readU16(self.__MPU6050_RA_FIFO_COUNTH)

    for ii in range(fifo_bytes):
        self.i2c.readU8(self.__MPU6050_RA_FIFO_R_W)

    #-------------------------------------------------------------------------------------------
    # Finally start feeding the FIFO with sensor data again
    #-------------------------------------------------------------------------------------------
    self.i2c.write8(self.__MPU6050_RA_FIFO_EN, 0x78)

def calibrateCompass():
    mgx_offset = 0.0
    mgy_offset = 0.0
    mgz_offset = 0.0
    mgx_gain = 1.0
    mgy_gain = 1.0
    mgz_gain = 1.0
    offs_rc = False

    #-------------------------------------------------------------------------------------------
    # First we need gyro offset calibration.  Flush the FIFO, collect roughly half a FIFO full
    # of samples and feed back to the gyro offset calibrations.
    #-------------------------------------------------------------------------------------------
    raw_input("First, put me on a stable surface, and press enter.")

    flushFIFO()
    time.sleep(FULL_FIFO_BATCHES / sampling_rate)
    nfb = mpu6050.numFIFOBatches()
    qax, qay, qaz, qrx, qry, qrz, dt = mpu6050.readFIFO(nfb)
    mpu6050.setGyroOffsets(qrx, qry, qrz)

    print "OK, thanks.  That's the gyro calibrated."

    #-------------------------------------------------------------------------------------------
    # Open the offset file for this run
    #-------------------------------------------------------------------------------------------
    try:
        with open('CompassOffsets', 'ab') as offs_file:

            mgx, mgy, mgz = self.readCompass()
            max_mgx = mgx
            min_mgx = mgx
            max_mgy = mgy
            min_mgy = mgy
            max_mgz = mgz
            min_mgz = mgz

            #-----------------------------------------------------------------------------------
            # Collect compass X. Y compass values
            #-------------------------------------------------------------------------------
            GPIO.output(GPIO_BUZZER, GPIO.LOW)
            print "Now, pick me up and rotate me horizontally twice until the buzzing stop."
            raw_input("Press enter when you're ready to go.")

            self.flushFIFO()

            yaw = 0.0
            total_dt = 0.0

            print "ROTATION:    ",
            number_len = 0

            #-------------------------------------------------------------------------------
            # While integrated Z axis gyro < 2 pi i.e. 360 degrees, keep flashing the light
            #-------------------------------------------------------------------------------
            while abs(yaw) < 4 * math.pi:
                time.sleep(10 / sampling_rate)

                nfb = mpu6050.numFIFOBatches()
                ax, ay, az, gx, gy, gz, dt = self.readFIFO(nfb)
                ax, ay, az, gx, gy, gz = self.scaleSensors(ax, ay, az, gx, gy, gz)

                yaw += gz * dt
                total_dt += dt

                mgx, mgy, mgz = self.readCompass()

                max_mgx = mgx if mgx > max_mgx else max_mgx
                max_mgy = mgy if mgy > max_mgy else max_mgy
                min_mgx = mgx if mgx < min_mgx else min_mgx
                min_mgy = mgy if mgy < min_mgy else min_mgy

                if total_dt > 0.2:
                    total_dt %= 0.2

                    number_text = str(abs(int(math.degrees(yaw))))
                    if len(number_text) == 2:
                        number_text = " " + number_text
                    elif len(number_text) == 1:
                        number_text = "  " + number_text

                    print "\b\b\b\b%s" % number_text,
                    sys.stdout.flush()

                    GPIO.output(GPIO_BUZZER, not GPIO.input(GPIO_BUZZER))
            print

            #-------------------------------------------------------------------------------
            # Collect compass Z values
            #-------------------------------------------------------------------------------
            GPIO.output(GPIO_BUZZER, GPIO.LOW)
            print "\nGreat!  Now do the same but with my nose down."
            raw_input("Press enter when you're ready to go.")

            self.flushFIFO()

            rotation = 0.0
            total_dt = 0.0

            print "ROTATION:    ",
            number_len = 0

            #-------------------------------------------------------------------------------
            # While integrated X+Y axis gyro < 4 pi i.e. 720 degrees, keep flashing the light
            #-------------------------------------------------------------------------------
            while abs(rotation) < 4 * math.pi:
                time.sleep(10 / sampling_rate)

                nfb = self.numFIFOBatches()
                ax, ay, az, gx, gy, gz, dt = self.readFIFO(nfb)
                ax, ay, az, gx, gy, gz = self.scaleSensors(ax, ay, az, gx, gy, gz)

                rotation += math.pow(math.pow(gx, 2) + math.pow(gy, 2), 0.5) * dt
                total_dt += dt

                mgx, mgy, mgz = self.readCompass()

                max_mgz = mgz if mgz > max_mgz else max_mgz
                min_mgz = mgz if mgz < min_mgz else min_mgz

                if total_dt > 0.2:
                    total_dt %= 0.2

                    number_text = str(abs(int(math.degrees(rotation))))
                    if len(number_text) == 2:
                        number_text = " " + number_text
                    elif len(number_text) == 1:
                        number_text = "  " + number_text

                    print "\b\b\b\b%s" % number_text,
                    sys.stdout.flush()

                    GPIO.output(GPIO_BUZZER, not GPIO.input(GPIO_BUZZER))
            print

            #-------------------------------------------------------------------------------
            # Turn the light off regardless of the result
            #-------------------------------------------------------------------------------
            GPIO.output(GPIO_BUZZER, GPIO.LOW)

            #-------------------------------------------------------------------------------
            # Write the good output to file.
            #-------------------------------------------------------------------------------
            mgx_offset = (max_mgx + min_mgx) / 2
            mgy_offset = (max_mgy + min_mgy) / 2
            mgz_offset = (max_mgz + min_mgz) / 2
            mgx_gain = 1 / (max_mgx - min_mgx)
            mgy_gain = 1 / (max_mgy - min_mgy)
            mgz_gain = 1 / (max_mgz - min_mgz)

            offs_file.write("%f %f %f %f %f %f\n" % (mgx_offset, mgy_offset, mgz_offset, mgx_gain, mgy_gain, mgz_gain))

            #-------------------------------------------------------------------------------
            # Sanity check.
            #-------------------------------------------------------------------------------
            print "\nLooking good, just one last check to confirm all's well."
            self.checkCompass()

            print "All done - ready to go!"
            offs_rc = True

    except EnvironmentError as e:
        print "Environment Error: '%s'" % e

    return offs_rc


def readCompass():
        compass_bytes = readList(HXL, 7)
        
        #-------------------------------------------------------------------------------------------
        # Convert the array of 6 bytes to 3 shorts - 7th byte kicks off another read.
        # Note compass X, Y, Z are aligned with GPS not IMU i.e. X = 0, Y = 1 => 0 degrees North
        #-------------------------------------------------------------------------------------------
        compass_data = []
        for ii in range(0, 6, 2):
            lobyte = compass_bytes[ii]
            hibyte = compass_bytes[ii + 1]
            hibyte = hibyte - 256 if hibyte > 127 else hibyte
            compass_data.append((hibyte << 8) + lobyte)

        [mgx, mgy, mgz] = compass_data

        mgx = (mgx - mgx_offset) * mgx_gain
        mgy = (mgy - mgy_offset) * mgy_gain
        mgz = (mgz - mgz_offset) * mgz_gain

        return mgx, mgy, mgz
