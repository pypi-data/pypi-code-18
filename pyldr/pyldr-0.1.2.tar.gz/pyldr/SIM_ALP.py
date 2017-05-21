import Input
import numpy as np

class SIM_ALP:
    def __init__(self,t = 5, T = 40):
        self.reader = Input.Input()
        self.reader.readIn('data/rm_200_4_1.0_4.0.txt')
        self.reader.product()
        self.reader.leg()
        self.reader.construct()
        self.t = t
        self.T = T
        self.set_para()
        
    def set_para(self):

        self.i = self.reader.f
        self.j = self.reader.i
        
        #Sparse P
        #self.P = np.zeros((20000,20000),dtype=np.float)
        
        #construct A
        self.A = {}
        self.c = np.zeros((self.i,1),dtype=np.float)
        self.v = np.zeros((self.j,1),dtype=np.float)

        self.prob = np.zeros((self.t*self.T,self.j), dtype=np.float)
        for t in range(0,self.t * self.T):
            for j in range(0,self.j):
                index = self.reader.prdic[j]
                self.prob[t,j] = self.reader.bdic[(t,index[0],index[1],index[2])]

        #construct A
        for item in self.reader.listA:
        	if item[1]-1 in self.A.keys():
        		self.A[item[1]-1].append(item[0])
        	else:
        		self.A[item[1]-1] = [item[0]]
        #construct c
        for item in range(0,self.i):
            self.c[item] = self.reader.flight[item][2]
            #self.c[item] = 2
        #construct v
        for j in range(0,self.j):
            self.v[j] = self.reader.pval[j]

    def sim(self):
        tmpDemand = np.zeros((self.t*self.T,self.j), dtype=np.float)
        for t in range(0,self.t*self.T):
            p = np.random.uniform()
            for j in range(0,self.j):
                p-= self.prob[t,j]
                if p<=0 :
                    tmpDemand[t,j] += 1
                    break
        self.realDemand = np.zeros((self.t,self.j))
        for t in range(0,self.t):
            for j in range(0,self.j):
                self.realDemand[t,j] = np.sum(tmpDemand[t*self.T:(t+1)*self.T,j])
        return self.realDemand
        