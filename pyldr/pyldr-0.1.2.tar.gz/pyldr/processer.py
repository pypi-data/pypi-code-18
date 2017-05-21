from DR import *
from mabinter import *
import numpy as np
class processer(object):
    def __init__(self,script):
        self.DR = DR(script)
        self.script = script

    def update(self):
        self.DR.update()

    def set_inter(self,inter):
        self.inter = inter

    def test(self,sample):
        C = self.script.C.copy()
        V = self.script.V.copy()
        val = 0
        for t in range(self.script.T):
            product = self.DR.strategy(t, sample[0:t,:])
            
            product = product.reshape(self.script.J)
            
            for j in range(self.script.J):
                product[j] = self.inter(t,j,product[j])
                
            product = np.fmin(product, sample[t,:].T)

            for j in range(self.script.J):
                for l in self.script.A[j]:
                    product[j] = min(product[j],C[l])

                val += product[j] * V[j]
                for l in self.script.A[j]:
                    C[l] -= product[j]

        return val

    def train(self,data):
        self.mab_inter = mabinter(data,self.script)#Todo
        self.inter = self.mab_inter.inter
        self.mab_inter.train(self.test)