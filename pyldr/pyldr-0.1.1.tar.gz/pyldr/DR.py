# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 17:25:20 2017

@author: dy403
"""


import numpy as np
from LDR import *

class DR:
    def __init__(self,script):
        self.script = script
        self.ldr = LDR(A = script.A, E = script.E, W = script.W, h = script.h, P = script.P, V = script.V, T = script.T, J = script.J, C = script.C, xi = script.xi, lb = script.lb, ub = script.ub)

    def update(self):
        self.ldr.build_model()
        self.ldr.solve_model()
        self.X = self.ldr.X

    def strategy(self,t,history):
        tran_his = np.vstack((history,np.zeros(((self.script.T-t),self.script.J))))
        return self.script.algs.strategy(t,tran_his,self.X)
        #tran_his = self.script.algs.lift_value(tran_his)
        #for j in range(self.script.J):
         #   for k in self.script.P[t,j]:
          #      product[j] += self.X[t,j,k].X * tran_his[k]
