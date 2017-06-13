#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 13:38:46 2017

@author: diezg@Inelta.local0,784
"""
### Based on u3allio.c
import u3
from datetime import datetime

chanels=[0,2,3]
numChannels = len(chanels)
quickSample = 1
longSettling = 0
latestAinValues = [0] * numChannels
numIterations = 1000

d = u3.U3()

try:
    #Configure the IOs before the test starts
    
    FIOEIOAnalog = ( 2 ** numChannels ) - 1;
    fios = FIOEIOAnalog & (0xFF)
    eios = FIOEIOAnalog/256
    
#    dconfigIO( FIOAnalog = fios, EIOAnalog = eios )
#    
    d.getFeedback(u3.PortDirWrite(Direction = [0, 0, 0], WriteMask = [0, 0, 15]))
#    
#    
    feedbackArguments = []
    
    feedbackArguments.append(u3.DAC0_8(Value = 125))
    feedbackArguments.append(u3.PortStateRead())
    
    #Check if the U3 is an HV
    if d.configU3()['VersionInfo']&18 == 18:
        isHV = True
    else:
        isHV = False
#
    for i in range(numChannels):
        feedbackArguments.append( u3.AIN(chanels[i], 31, QuickSample = quickSample, LongSettling = longSettling ) )
##    
#    print ("\n \n ",feedbackArguments,"\n \n ")
#    
    start = datetime.now()
    # Call Feedback 1000 times
    i = 0
    while i < numIterations:
        results = d.getFeedback( feedbackArguments )
        #print results
        for j in range(numChannels):
            #Figure out if the channel is low or high voltage to use the correct calibration
            if isHV == True and j < 4:
                lowVoltage = False
            else:
                lowVoltage = True
            latestAinValues[j] = d.binaryToCalibratedAnalogVoltage(results[ 2 + j ], isLowVoltage = lowVoltage, isSingleEnded = True)
        i += 1

    end = datetime.now()
    print(" \n \n Latest readings: ", latestAinValues)

finally:
    d.close()
d.close()
###################################################################################################
# Based on u6allio.c
#from labjack import u3
#from datetime import datetime
#
#
#chanels=[0,1]
#numChannels = len(chanels)
#resolutionIndex = 1
#gainIndex = 0
#settlingFactor = 0
#differential = False
#
#latestAinValues = [0] * numChannels
#
#numIterations = 1
#
#d = u3.U3()
#d.getCalibrationData()
#
#try:
#    #Configure the IOs before the test starts
#    
#    FIOEIOAnalog = ( 2 ** numChannels ) - 1;
#    fios = FIOEIOAnalog & (0xFF)
#    eios = FIOEIOAnalog/256   
#    d.getFeedback(u3.PortDirWrite(Direction = [0, 0, 0], WriteMask = [0, 0, 15]))   
#    feedbackArguments = []    
#    feedbackArguments.append(u3.DAC0_8(Value = 125))
#    feedbackArguments.append(u3.PortStateRead())    
#    for i in range(numChannels):
#        feedbackArguments.append( u3.AIN24(chanels[i], resolutionIndex, gainIndex, settlingFactor, differential) )       
#    start = datetime.now()
#    # Call Feedback 1000 times
#    i = 0
#    while i < numIterations:
#        results = d.getFeedback( feedbackArguments )
#        
#        for j in range(numChannels):
#            latestAinValues[j] = d.binaryToCalibratedAnalogVoltage(gainIndex, results[ 2 + j ])
##            print("read: ", results[ 2 + j ],"------- latestAinValues:", latestAinValues[j] ,"------- gainIndex:",gainIndex)
#        i += 1
#    dac = d.writeRegister(5000, 1)
#    print("Latest readings: ", latestAinValues)
#
#finally:
#    d.close()