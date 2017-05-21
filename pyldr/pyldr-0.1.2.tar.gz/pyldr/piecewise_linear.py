import numpy as np
from algs import *

class piecewise_linear(algs):

    def piecewise(self):
        self.constant = self.script.constant
        self.xi = self.script.xi
        self.div_num = 7
        self.div_axis = {}
        for t in range(self.T):
            for j in range(self.J):
                for k in range(self.div_num):
                    self.div_axis[t,j,k] = self.low_bound[t,j] + (self.up_bound[t,j]-self.low_bound[t,j])/float(self.div_num - 1) * k
                    self.xi[t,j,k] = self.script.add_var(0,self.div_axis[t,j,k])

        for t in range(self.T):
            for j in range(self.J):
                left = {}
                for k in range(self.div_num):
                    left[self.xi[t,j,k]] = 1
                right = {}
                right[self.constant] = 1
                self.script.add_lin_equ(left,right)
                for k in range(self.div_num):
                    self.script.add_lin_greater({self.xi[t,j,k]:1},{self.constant:0})

        for t in range(self.T):
            for j in range(self.J):
                left = {self.xi[t,j]:1}
                right = {}
                for k in range(self.div_num):
                    right[self.xi[t,j,k]] = self.div_axis[t,j,k]
                self.script.add_lin_equ(left,right)

    def value(self,t,j,k,v):
        if k == self.div_num - 1 and v >= self.div_axis[t,j,self.div_num-1] :
            return 1
        elif k < self.div_num-1 and v >= self.div_axis[t,j,k+1]:
            return 0

        if k == 0 and v <= self.div_axis[t,j,0]:
            return 1
        elif k > 0 and v <= self.div_axis[t,j,k-1]:
            return 0

        if v > self.div_axis[t,j,k]:
            return (self.div_axis[t,j,k+1] - v) / (self.div_axis[t,j,k+1] - self.div_axis[t,j,k])
        else:
            return (v-self.div_axis[t,j,k-1]) / (self.div_axis[t,j,k] - self.div_axis[t,j,k-1])


    def lift_value(self,data):
        value = np.zeros((self.script.index,1))
        value[self.constant] = 1
        for t in range(self.T):
            for j in range(self.J):
                value[self.xi[t,j]] = data[t,j]
                for k in range(self.div_num):
                    value[self.xi[t,j,k]] = self.value(t,j,k,data[t,j])
        return value

    def relation(self):
        self.P = {}
        for t in range(self.T):
            for j in range(self.J):
                self.P[t,j] = []
                for k in range(self.div_num):
                    self.P[t,j].append(self.xi[t,j,k])

    def update(self):
        self.piecewise()
        self.relation()
        
    def strategy(self,t,history,X):
        product = np.zeros((self.script.J,1))
        for j in range(self.script.J):
            product[j] = X[t,j,self.xi[t,j,self.div_num-1]].X
                   
        return product