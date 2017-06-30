'''
 Copyright (c) 2016, UChicago Argonne, LLC
 See LICENSE file.
'''
from spec2nexus.spec import SpecDataFile
import os

print os.getcwd()
specFile = '../testData/zhou160224.spc'

sd = SpecDataFile(specFile)

scans = sd.getScanNumbers()

def imagesBeforeScan(scanNo):
    numImages = 0
    for scanno in xrange(1, scanNo):
        scan = sd.scans[str(scanno)]
        numImages += len(scan.data_lines)
        
    return numImages
        
    
def imagesInScan(scanNo):
    scan = sd.scans[str(scanNo)]
    numImages = len(scan.data_lines)
    return numImages
    

for scan in range(1,len(scans)+1):
    print sd.scans[str(scan)]
    print ("Number of images in scan: " +str(imagesInScan(scan)))
    print ("Number of images before scan: " +str(imagesBeforeScan(scan)))
    
    
