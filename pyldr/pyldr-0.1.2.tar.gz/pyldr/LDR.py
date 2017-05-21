# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 19:19:54 2017

@author: dy403
"""

import numpy as np
from gurobipy import *

class LDR:
    def __init__(self,A,E,W,h,P,V,T,J,C,xi,lb,ub):
        self.A = A
        self.E = E
        self.W = W
        self.h = h
        self.P = P
        self.V = V
        self.T = T
        self.J = J
        self.C = C
        self.L = len(self.C)
        self.xi = xi
        self.lb = lb
        self.ub = ub

    def build_model(self):
        self.model = Model("Decision Rule Approch")
        self.X = {}
        for t in range(self.T):
            for j in range(self.J):
                for k in self.P[t,j]:
                    self.X[t,j,k] = self.model.addVar(lb = self.lb[k], ub = self.ub[k])

        obj = LinExpr()
        for t in range(self.T):
            for j in range(self.J):
                for k in self.P[t,j]:
                    obj += self.X[t,j,k] * self.V[j] * self.E[k]

        self.model.setObjective(obj,GRB.MAXIMIZE)


        print "Constriant:Used Resource <= Total Resource"
        self.invA = {}
        for l in range(self.L):
            self.invA[l] = []

        for (a,b) in self.A.items():
            for r in b:
                self.invA[r].append(a)

        for l in range(self.L):
            left = {}
            for j in self.invA[l]:
                for t in range(self.T):
                    for k in self.P[t,j]:
                        if k in left:
                            left[k] += self.X[t,j,k]
                        else:
                            left[k] = self.X[t,j,k]

            right = {0:LinExpr()}
            right[0] += self.C[l] * 2
            for j in self.invA[l]:
                for t in range(self.T):
                    for k in self.P[t,j]:
                        right[0] = right[0] - self.X[t,j,k] * self.E[k]
            self.add_less(left,right)

        print "Update Model"
        self.model.update()

    def add_less(self,left,right):
        self.add_greater(right,left)

    def add_greater(self,left,right):
        self.row_W = np.shape(self.W)[0]
        self.col_W = np.shape(self.W)[1]
        Lambda = {}
        for i in range(self.row_W):
            Lambda[i] = self.model.addVar(lb = 0, ub = GRB.INFINITY)

        for (a,b) in right.items():
            if a in left:
                left[a] -= b
            else:
                left[a] = -b

        for i in left.keys():
            temp = LinExpr()
            col_index = self.W[:,i].indices
            col_data = self.W[:,i].data
            for k in range(len(col_data)):
                j = col_index[k]
                temp += Lambda[j] * col_data[k]

            self.model.addConstr(temp == left[i])

        I = set(range(self.col_W))
        DIFF = set(left.keys())
        I = I.difference(DIFF)

        for i in I:
            temp = LinExpr()
            col_index = self.W[:,i].indices
            col_data = self.W[:,i].data
            for k in range(len(col_data)):
                j = col_index[k]
                temp += Lambda[j] * col_data[k]


            self.model.addConstr(temp == 0)

        temp = LinExpr()
        for i in range(self.row_W):
            temp += Lambda[i] * self.h[i]

        self.model.addConstr(temp >= 0)

    def solve_model(self):
        print "Optimize Model"
        self.model.optimize()