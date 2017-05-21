import numpy as np
from scipy.special import gamma

class SIM_Resolve_Second:
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
        for j in range(10,22):
            self.v[2*j] = 500
            self.v[2*j+1] = 100
        for j in range(22,30):
            self.v[2*j] = 700
            self.v[2*j+1] = 200
            
        #Capacity
        self.c = np.zeros((self.i,1))
        for i in range(0,10):
            self.c[i] = 400
        self.c[4] = self.c[5] = 1000
        
        #matrix A 
        self.A = {}
        for j in range(0,10):
            self.A[2*j] = [j]
            self.A[2*j+1] = [j]
        self.pushTwoLeg(0,1,0,3,1,2,0)
        self.pushTwoLeg(0,5,0,4,5,1,1)
        self.pushTwoLeg(1,5,2,4,5,3,2)
        self.pushTwoLeg(2,4,6,5,4,7,3)
        self.pushTwoLeg(2,3,6,8,9,7,4)
        self.pushTwoLeg(3,4,9,5,4,8,5)
        self.pushThreeLeg(0,2,0,4,7,6,5,1,6)
        self.pushThreeLeg(0,3,0,4,8,9,5,1,7)
        self.pushThreeLeg(1,2,2,4,7,6,5,3,8)
        self.pushThreeLeg(1,3,2,4,8,9,5,3,9)
        
        totalLen = 1000.0
        div = int(totalLen / self.t)
        self.cons = np.zeros((self.t,2))
        for t in range(0,self.t):            
            for tt in range(t*div,(t+1)*div):
                self.cons[t,0] +=  0.25 * 1.0/totalLen * (float(tt)/totalLen) ** (6 - 1) * (1- float(tt)/totalLen) ** (2-1) * gamma(8)/gamma(2)/gamma(6)
                self.cons[t,1] +=  0.75 * 1.0/totalLen * (float(tt)/totalLen) ** (2 - 1) * (1- float(tt)/totalLen) ** (6-1) * gamma(8)/gamma(2)/gamma(6)
                
    
    def pushTwoLeg(self,s,t,a,b,c,d,id):
        self.A[20+4*id] = [a,b]
        self.A[20+4*id+1] = [a,b]
        self.A[20+4*id+2] = [c,d]
        self.A[20+4*id+3] = [c,d] 
    
    def pushThreeLeg(self,s,t,a,b,c,d,e,f,id):
        self.A[20+4*id] = [a,b,c]
        self.A[20+4*id+1] = [a,b,c] 
        self.A[20+4*id+2] = [d,e,f]
        self.A[20+4*id+3] = [d,e,f]

    def sim(self):    
        self.realDemand = np.zeros((self.t,self.j))
        for t in range(0,self.t):
            for j in range(0,10):
                g = np.random.gamma(60)
                self.realDemand[t,2*j]= np.random.poisson(g * self.cons[t][0])
                self.realDemand[t,2*j+1]= np.random.poisson(g * self.cons[t][1])
            for j in range(10,22):
                g = np.random.gamma(150)
                self.realDemand[t,2*j] = np.random.poisson(g * self.cons[t][0])
                self.realDemand[t,2*j+1] = np.random.poisson(g * self.cons[t][1])
            for j in range(22,30):
                g = np.random.gamma(100)
                self.realDemand[t,2*j] = np.random.poisson(g * self.cons[t][0])
                self.realDemand[t,2*j+1] = np.random.poisson(g * self.cons[t][1])
        return self.realDemand

    