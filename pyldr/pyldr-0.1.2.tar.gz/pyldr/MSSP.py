# -*- coding: utf-8 -*-
"""
Created on Wed Feb 22 16:33:30 2017

@author: dy403
"""

import numpy as np
import scipy as sp

class MSSP:
    
    def __init__(self):
        self.demandPre = []
        self.pricePre = []
        self.APre = []
        self.cPre = []
        self.bPre = []
        self.WPre = []
        self.demand = []
        self.price = []
        self.A = []
        self.c = []
        self.b = []
        self.W = []
        self.h = []
        
    #Number of Stage
    def setStage(self,t):
        self.t = t
    
    #Number of Legs
    
    def setLeg(self,l):
        self.l = l
    
    #Number of Classes
    def setClass(self,cl):
        self.cl = cl
    
    #Add Demand
    def addDemand(self,d):
        self.demand.append(d)
    
    def setDemand(self,d):
        self.demand = d
    
    #Add usage to construct A, only non-zero item needed
    def addA(self,i,j,t):
        self.APre.append((i,j,t))
    
    #Add C
    def setC(self,i,c):
        self.cPre.append((i,c))
    
    #Add b
    def setb(self,t,b):
        self.bPre.append((t,b))
    
    #Add W, only non-zero item needed
    def setW(self,i,j,value):
        self.WPre.append((i,j,value))
    
    def seth(self,i,h):
        self.h.append((i,h))
    
    def constructA(self):
        data = []
        row = []
        col = []
        self.cltoleg = np.empty(self.cl,list)
        for i in range(self.cl):
            self.cltoleg[i] = []
        for item in self.APre:
            row.append(item[0])
            col.append(item[1])
            data.append(item[2])
            self.cltoleg[item[1]].append(item[0])
        self.A = sp.sparse.coo_matrix((data,(row,col)))
        #Use non-sparse structure temporarily
        self.A = self.A.todense()
        
    def constructW(self):
        data = []
        row = []
        col = []
        for item in self.WPre:
            row.append(item[0])
            col.append(item[1])
            data.append(item[2])
        self.W = sp.sparse.coo_matrix((data,(row,col)))
        #Use non-sparse structure temporarily
        self.W = self.W.todense()
        
    def constructh(self):
        tmp = np.zeros(np.shape(self.W)[0])
        for item in self.h:
            tmp[item[0]] = item[1]
        self.h = np.arry(tmp)
    
    def constructb(self):
        self.b = np.zeros(self.l)
        for item in self.bPre:
            t = item[0]
            real = item[1]
            self.b[t] = real
    
    def constructc(self):
        self.c = np.zeros(self.cl)
        for item in self.cPre:
            t = item[0]
            real = item[1]
            self.c[t] = real
            
    #Construct coefficient
    def update(self):
        self.constructA()
        self.constructW()
        self.constructh()
        self.constructb()
        self.constructc()