#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 19:47:42 2017

@author: root
"""

import NETWORK
import numpy as np

from scipy.special import gamma
from scipy.stats import gamma as Gamma
from scipy.stats import poisson

net = NETWORK()

for i in range(20):
    net.addProfit(i,500)
    
for i in range(20,30):
    net.addProfit(i,300)

for i in range(30,50):
    net.addProfit(i,100)

for i in range(50,60):
    net.addProfit(i,80)

for i in range(10):
    net.addRes(i,400)
    
for i in range(10):
    net.addUsage(20+i,[i])
    net.addUsage(50+i,[i])

net.addUsage(0,[0,1])
net.addUsage(1,[0,2])
net.addUsage(2,[0,3])
net.addUsage(3,[0,4])
net.addUsage(4,[1,0])
net.addUsage(5,[1,2])
net.addUsage(6,[1,3])
net.addUsage(7,[1,4])
net.addUsage(8,[2,0])
net.addUsage(9,[2,1])
net.addUsage(10,[2,3])
net.addUsage(11,[2,4])
net.addUsage(12,[3,0])
net.addUsage(13,[3,1])
net.addUsage(14,[3,2])
net.addUsage(15,[3,4])
net.addUsage(16,[4,0])
net.addUsage(17,[4,1])
net.addUsage(18,[4,2])
net.addUsage(19,[4,3])


net.addUsage(30,[0,1])
net.addUsage(31,[0,2])
net.addUsage(32,[0,3])
net.addUsage(33,[0,4])
net.addUsage(34,[1,0])
net.addUsage(35,[1,2])
net.addUsage(36,[1,3])
net.addUsage(37,[1,4])
net.addUsage(38,[2,0])
net.addUsage(39,[2,1])
net.addUsage(40,[2,3])
net.addUsage(41,[2,4])
net.addUsage(42,[3,0])
net.addUsage(43,[3,1])
net.addUsage(44,[3,2])
net.addUsage(45,[3,4])
net.addUsage(46,[4,0])
net.addUsage(47,[4,1])
net.addUsage(48,[4,2])
net.addUsage(49,[4,3])

p = 10
Origin = 1000.0
div = int(Origin / p)
cons = np.zeros((p,2))
for t in range(0,p):            
    for tt in range(t*div,(t+1)*div):
        cons[t,0] +=  0.25 * 1.0/Origin * (float(tt)/Origin) ** (6 - 1) * (1- float(tt)/Origin) ** (2-1) * gamma(8)/gamma(2)/gamma(6)
        cons[t,1] +=  0.75 * 1.0/Origin * (float(tt)/Origin) ** (2 - 1) * (1- float(tt)/Origin) ** (6-1) * gamma(8)/gamma(2)/gamma(6)
        
monteSize = 1000
monteCarlo = np.zeros((t,60))
real = []
for k in range(monteSize):
    for t in range(0,t):
        simGamma = np.random.gamma(100,size=(1))
        for j in range(20):
            monteCarlo[t,j] = np.random.poisson(simGamma * cons[t,0])
        for j in range(30,50):
            monteCarlo[t,j] = np.random.poisson(simGamma * cons[t,1])
        simGamma = np.random.gamma(40,size=(1))
        for j in range(20,30):
            monteCarlo[t,j] = np.random.poisson(simGamma * cons[t,0])
        for j in range(50,60):
            monteCarlo[t,j] = np.random.poisson(simGamma * cons[t,1])
    net.addDemand(monteCarlo)

net.update()