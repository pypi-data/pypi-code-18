import numpy as np
from scipy.special import gamma

class SIM_Resolve_First(object):
    def __init__(self, t=10):
        self.t = t        
        self.set_para()

    def set_para(self):   
        self.i = 10
        self.j = 60
        
        #Fare
        self.v = np.zeros((self.j,1))
        for j in range(0,10):
            self.v[2*j] = 300
            self.v[2*j+1] = 80
        for j in range(10,30):
            self.v[2*j] = 500
            self.v[2*j+1] = 100
            
        #Capacity
        self.c = np.zeros((self.i,1))
        for i in range(0,10):
            self.c[i] = 400
        
        #matrix A I * J
        self.A = {}
        for j in range(0,10):
            self.A[2*j] = [j]
            self.A[2*j+1] = [j]
            
        for a in range(0,5):
            for b in range(0,5):
                if a == b:
                    continue
                j = j + 1

                self.A[2*j] = [2*a,2*b+1]
                self.A[2*j+1] = [2*a,2*b+1]
            
        totalLen = 1000.0
        div = int(totalLen / self.t)
        self.cons = np.zeros((self.t,2))
        for t in range(0,self.t):            
            for tt in range(t*div,(t+1)*div):
                self.cons[t,0] +=  0.25 * 1.0/totalLen * (float(tt)/totalLen) ** (6 - 1) * (1- float(tt)/totalLen) ** (2-1) * gamma(8)/gamma(2)/gamma(6)
                self.cons[t,1] +=  0.75 * 1.0/totalLen * (float(tt)/totalLen) ** (2 - 1) * (1- float(tt)/totalLen) ** (6-1) * gamma(8)/gamma(2)/gamma(6)

    def sim(self):        
        self.realDemand = np.zeros((self.t,self.j))
        for t in range(0,self.t):
            for j in range(0,10):
                g = np.random.gamma(40)
                self.realDemand[t,2*j] = np.random.poisson(g * self.cons[t][0])
                self.realDemand[t,2*j+1] = np.random.poisson(g * self.cons[t][1])
            for j in range(10,30):
                g = np.random.gamma(100)
                self.realDemand[t,2*j] = np.random.poisson(g * self.cons[t][0])
                self.realDemand[t,2*j+1] = np.random.poisson(g * self.cons[t][1])
        return self.realDemand