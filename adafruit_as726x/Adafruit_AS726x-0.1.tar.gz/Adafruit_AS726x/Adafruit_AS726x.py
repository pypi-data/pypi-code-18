# Copyright (c) 2017 Adafruit Industries
# Author: Dean Miller
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import logging
from Adafruit_bitfield import Adafruit_bitfield
from time import sleep
import struct

AS726x_ADDRESS  =  0x49

AS726X_HW_VERSION	=	0x00
AS726X_FW_VERSION	=	0x02
AS726X_CONTROL_SETUP =	0x04
AS726X_INT_T		=	0x05
AS726X_DEVICE_TEMP	 =	0x06
AS726X_LED_CONTROL	 =	0x07

#for reading sensor data
AS7262_V_HIGH	=		0x08
AS7262_V_LOW		=	0x09
AS7262_B_HIGH		=	0x0A
AS7262_B_LOW		=	0x0B
AS7262_G_HIGH		=	0x0C
AS7262_G_LOW		=	0x0D
AS7262_Y_HIGH		=	0x0E
AS7262_Y_LOW		=	0x0F
AS7262_O_HIGH		=	0x10
AS7262_O_LOW		=	0x11
AS7262_R_HIGH		=	0x12
AS7262_R_LOW		=	0x13

AS7262_V_CAL		=	0x14
AS7262_B_CAL		=	0x18
AS7262_G_CAL		=	0x1C
AS7262_Y_CAL		=	0x20
AS7262_O_CAL		=	0x24
AS7262_R_CAL		=	0x28

	
#hardware registers
AS726X_SLAVE_STATUS_REG = 0x00
AS726X_SLAVE_WRITE_REG = 0x01
AS726X_SLAVE_READ_REG = 0x02
AS726X_SLAVE_TX_VALID = 0x02
AS726X_SLAVE_RX_VALID = 0x01

AS7262_VIOLET = 0x08
AS7262_BLUE = 0x0A
AS7262_GREEN = 0x0C
AS7262_YELLOW = 0x0E
AS7262_ORANGE = 0x10
AS7262_RED = 0x12
AS7262_VIOLET_CALIBRATED = 0x14
AS7262_BLUE_CALIBRATED = 0x18
AS7262_GREEN_CALIBRATED = 0x1C
AS7262_YELLOW_CALIBRATED = 0x20
AS7262_ORANGE_CALIBRATED = 0x24
AS7262_RED_CALIBRATED = 0x28

#other defs
AS726x_MODE_0 = 0b00
AS726x_MODE_1 = 0b01
AS726x_MODE_2 = 0b10 #default
AS726x_ONE_SHOT = 0b11

AS726x_GAIN_1X = 0b00, #default
AS726x_GAIN_3X7 = 0b01
AS726x_GAIN_16X = 0b10
AS726x_GAIN_64X = 0b11

AS726x_LIMIT_1MA = 0b00 #default
AS726x_LIMIT_2MA = 0b01
AS726x_LIMIT_4MA = 0b10
AS726x_LIMIT_8MA = 0b11

AS726x_LIMIT_12MA5 = 0b00 #default
AS726x_LIMIT_25MA = 0b01
AS726x_LIMIT_50MA = 0b10
AS726x_LIMIT_100MA = 0b11
	
AS726x_NUM_CHANNELS = 6

class Adafruit_AS726x(object):
	def __init__(self, mode=AS726x_ONE_SHOT, address=AS726x_ADDRESS, i2c=None, **kwargs):
		self._logger = logging.getLogger('Adafruit_AS726x.AS726x')
		# Check that mode is valid.
		if mode not in [AS726x_MODE_0, AS726x_MODE_1, AS726x_MODE_2, AS726x_ONE_SHOT]:
			raise ValueError('Unexpected mode value {0}.  Set mode to one of AS726x_MODE_0, AS726x_MODE_1, AS726x_MODE_2 or AS726x_ONE_SHOT'.format(mode))
		self._mode = mode
		# Create I2C device.
		if i2c is None:
			import Adafruit_GPIO.I2C as I2C
			i2c = I2C
		self._device = i2c.get_i2c_device(address, **kwargs)

		#set up the registers
		self._control_setup = Adafruit_bitfield([('unused' , 1), ('DATA_RDY' , 1), ('BANK', 2), ('GAIN' , 2), ('INT' , 1), ('RST' , 1)])
		self._int_time = Adafruit_bitfield([('INT_T' , 8)])
		self._led_control = Adafruit_bitfield([('LED_IND', 1), ('ICL_IND', 2), ('LED_DRV', 1), ('ICL_DRV', 2)])
		
		self._control_setup.RST = 1
		self.virtualWrite(AS726X_CONTROL_SETUP, self._control_setup.get())
		self._control_setup.RST = 0
		
		#wait for it to boot up
		sleep(1)
		
		#try to read the version reg to make sure we can connect
		version = self.virtualRead(AS726X_HW_VERSION)
		
		#TODO: add support for other devices
		if(version != 0x40):
			raise ValueError("device could not be reached or this device is not supported!")
		
		self.setDrvCurrent(AS726x_LIMIT_12MA5)
		self.drvOff()
		
		self.setIndCurrent(AS726x_LIMIT_1MA)
		self.indicatorOff()
		
		self.setIntegrationTime(50)
		
		self.setGain(AS726x_GAIN_64X)
		
		self.setConversionType(AS726x_ONE_SHOT)
		
		
	#turn on the drv led
	def drvOn(self):
		self._led_control.LED_DRV = 1
		self.virtualWrite(AS726X_LED_CONTROL, self._led_control.get())

	#turn off the drv led
	def drvOff(self):
		self._led_control.LED_DRV = 0
		self.virtualWrite(AS726X_LED_CONTROL, self._led_control.get())

	#turn on the indicator led
	def indicatorOn(self):
		self._led_control.LED_IND = 1
		self.virtualWrite(AS726X_LED_CONTROL, self._led_control.get())
		
	#turn off the indicator led
	def indicatorOff(self):
		self._led_control.LED_IND = 0
		self.virtualWrite(AS726X_LED_CONTROL, self._led_control.get())

	#set current through drv led
	def setDrvCurrent(self, current):
		self._led_control.ICL_DRV = current
		self.virtualWrite(AS726X_LED_CONTROL, self._led_control.get())

	#set current through indicator led
	def setIndCurrent(self, current):
		self._led_control.ICL_IND = current
		self.virtualWrite(AS726X_LED_CONTROL, self._led_control.get())

	def setConversionType(self, type):
		self._control_setup.BANK = type
		self.virtualWrite(AS726X_CONTROL_SETUP, self._control_setup.get())
		
	def setGain(self, gain):
		self._control_setup.GAIN = gain
		self.virtualWrite(AS726X_CONTROL_SETUP, self._control_setup.get())
		
	def setIntegrationTime(self, time):
		self._int_time.INT_T = time
		self.virtualWrite(AS726X_INT_T, self._int_time.get())
		
	def enableInterrupt(self):
		self._control_setup.INT = 1
		self.virtualWrite(AS726X_CONTROL_SETUP, self._control_setup.get())
		
	def disableInterrupt(self):
		self._control_setup.INT = 0
		self.virtualWrite(AS726X_CONTROL_SETUP, self._control_setup.get())
		
	#read sensor data
	def startMeasurement(self):
		self._control_setup.DATA_RDY = 0
		self.virtualWrite(AS726X_CONTROL_SETUP, self._control_setup.get())
		
		self.setConversionType(AS726x_ONE_SHOT)
		

	def readChannel(self, channel):
		return (self.virtualRead(channel) << 8) | self.virtualRead(channel + 1)

	def readRawValues(self):
		buf = []
		buf.append(self.readViolet())
		buf.append(self.readBlue())
		buf.append(self.readGreen())
		buf.append(self.readYellow())
		buf.append(self.readOrange())
		buf.append(self.readRed())
		return buf	

	def readCalibratedValues(self):
		buf = []
		buf.append(self.readCalibratedViolet())
		buf.append(self.readCalibratedBlue())
		buf.append(self.readCalibratedGreen())
		buf.append(self.readCalibratedYellow())
		buf.append(self.readCalibratedOrange())
		buf.append(self.readCalibratedRed())
		return buf
	
	def dataAvailable(self):
		return self.virtualRead(AS726X_CONTROL_SETUP) & 0x02
		
	def readTemperature(self): 
		return self.virtualRead(AS726X_DEVICE_TEMP)
	
	#Get the various color readings
	def readViolet(self):
		return self.readChannel(AS7262_VIOLET)
	def readBlue(self): 
		return self.readChannel(AS7262_BLUE)
	def readGreen(self): 
		return self.readChannel(AS7262_GREEN)
	def readYellow(self): 
		return self.readChannel(AS7262_YELLOW)
	def readOrange(self): 
		return self.readChannel(AS7262_ORANGE)
	def readRed(self): 
		return self.readChannel(AS7262_RED)
	
	def readCalibratedViolet(self):  
		return self.readCalibratedValue(AS7262_VIOLET_CALIBRATED)
	def readCalibratedBlue(self):  
		return self.readCalibratedValue(AS7262_BLUE_CALIBRATED)
	def readCalibratedGreen(self):  
		return self.readCalibratedValue(AS7262_GREEN_CALIBRATED)
	def readCalibratedYellow(self):  
		return self.readCalibratedValue(AS7262_YELLOW_CALIBRATED)
	def readCalibratedOrange(self):  
		return self.readCalibratedValue(AS7262_ORANGE_CALIBRATED)
	def readCalibratedRed(self):  
		return self.readCalibratedValue(AS7262_RED_CALIBRATED)
	

	def readCalibratedValue(self, channel):
		val = (self.virtualRead(channel) << 24) | (self.virtualRead(channel + 1) << 16) | (self.virtualRead(channel + 2) << 8) | self.virtualRead(channel + 3)
		return struct.unpack('!f', val.decode('hex'))[0]
		

	def virtualRead(self, addr):
		while (1):
			# Read slave I2C status to see if the read buffer is ready.
			status = self._device.readU8(AS726X_SLAVE_STATUS_REG)
			if ((status & AS726X_SLAVE_TX_VALID) == 0):
				# No inbound TX pending at slave. Okay to write now.
				break
		# Send the virtual register address (setting bit 7 to indicate a pending write).
		self._device.write8(AS726X_SLAVE_WRITE_REG, addr)
		while (1):
			# Read the slave I2C status to see if our read data is available.
			status = self._device.readU8(AS726X_SLAVE_STATUS_REG)
			if ((status & AS726X_SLAVE_RX_VALID) != 0):
				# Read data is ready.
				break
		# Read the data to complete the operation.
		d = self._device.readU8(AS726X_SLAVE_READ_REG)
		return d
		

	def virtualWrite(self, addr, value):
		while (1):
			# Read slave I2C status to see if the write buffer is ready.
			status = self._device.readU8(AS726X_SLAVE_STATUS_REG)
			if ((status & AS726X_SLAVE_TX_VALID) == 0):
				break # No inbound TX pending at slave. Okay to write now.
		# Send the virtual register address (setting bit 7 to indicate a pending write).
		self._device.write8(AS726X_SLAVE_WRITE_REG, (addr | 0x80))
		while (1):
			# Read the slave I2C status to see if the write buffer is ready.
			status = self._device.readU8(AS726X_SLAVE_STATUS_REG)
			if ((status & AS726X_SLAVE_TX_VALID) == 0):
				break # No inbound TX pending at slave. Okay to write data now.
			
		# Send the data to complete the operation.
		self._device.write8(AS726X_SLAVE_WRITE_REG, value)
		

ams =  Adafruit_AS726x()

while(1):
	#read the device temperature
	temp = ams.readTemperature()
	print 'Temp: {0} degrees C'.format(temp)
	
	ams.startMeasurement()
  
	#wait till data is available
	rdy = False
	while not rdy:
		sleep(.005)
		rdy = ams.dataAvailable()

	#read the values!
	print ams.readRawValues()
	
	sleep(2)