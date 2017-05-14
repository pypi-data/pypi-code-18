# -*- coding: utf-8 -*-

import os,sys
import serial #for port opening
import sys #for exceptions
import time
#from app import config

class Serializer: 
    def __init__(self, port=None, baudrate=None, timeout=20,stopbits=None,bytesize=None,parity=None,waiting=False):

        if waiting is False:
            self.port = serial.Serial(port = port, baudrate=baudrate, 
            timeout=timeout, writeTimeout=timeout,stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE)
        else:
            self.port = serial.Serial(port = port, baudrate=baudrate, 
            timeout=timeout, writeTimeout=timeout,stopbits=serial.STOPBITS_ONE,
            bytesize=serial.EIGHTBITS,parity=serial.PARITY_NONE)
            self.port.in_waiting

    def open(self): 
        ''' Open the serial port.'''
        self.port.open()

    def close(self): 
        ''' Close the serial port.'''
        self.port.close() 

    def send(self, msg):
        self.port.write(msg)

    def recv(self,numberline=None):
    	if numberline is None:
	        return self.port.readline()
        else:
	        return self.port.read(numberline)