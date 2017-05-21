#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 26 18:57:03 2017

@author: root
"""
import sys
sys.path.append('..\MSSP')
import MSSP

class NETWORK:
    def __init__(self):
        self.resource = {}
        self.profit = {}
        self.usage = {}
        self.demand = []
        
    def addRes(self,num,res):
        self.resource[num] = res
    
    def addProfit(self,num,pro):
        self.profit[num] = pro
    
    def addUsage(self,num,usage):
        self.usage[num] = usage

    def setStage(self,stage):
        self.stage = stage
    
    def addDemand(self,demand):
        self.demand += demand
    
    def update(self):
        self.mssp = MSSP()
        self.mssp.setStage(self.stage)
        self.mssp.setLeg(len(self.resource.keys()))
        self.mssp.setClass(len(self.profit.keys()))
        for item in self.usage.items():
            self.mssp.addA(item[0],item[1],-1)
        for item in self.usage.items():
            self.mssp.setPrice(item[0],item[1])
        self.mssp.setDemand(self.demand)
        """
        self.mssp.setC(0,1)
        for i in range(self.stage*self.mssp.cl):
            self.mssp.setC(i+1,0)
        for i in range(self.cl):
            self.mssp.setB(0,i,-1)
        for i in range(1,self.stage+1):
            for j in range(self.mssp.cl):
                self.mssp.setB(i,j,0)
        """
        self.mssp.update()
            
    