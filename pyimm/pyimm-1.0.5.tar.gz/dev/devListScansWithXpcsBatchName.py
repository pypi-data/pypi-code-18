'''
Created on Jun 13, 2016

@author: hammonds
'''
import os
from spec2nexus.spec import SpecDataFile

print ("Hello")
basepath = os.path.abspath(os.path.dirname(__file__))
print basepath
datapath = os.path.join(basepath, 'data')
print datapath
xpcsPluginSample = os.path.join(datapath, 
                                     'xpcs_plugin_sample.spec')
print xpcsPluginSample
sd = SpecDataFile(xpcsPluginSample)

scans = sd.getScanNumbers()
print scans
for scan in scans:
    thisScan = sd.scans[scan]
    print thisScan.data