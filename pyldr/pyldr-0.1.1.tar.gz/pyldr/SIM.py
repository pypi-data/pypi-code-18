from processer import *
from script import *
from inter import *
class SIM(object):
    def __init__(self,simulator,algs):
        self.simulator = simulator
        self.algs = algs

    def generate_data(self):
        train_num = 1000
        self.D = []
        for i in range(train_num):
            self.D.append(self.simulator.sim())

    def update(self):
        self.generate_data()
        self.script = script(self.simulator.A,self.D,self.simulator.v,self.simulator.c,self.algs)
        self.algs.update()
        self.script.update()
        self.processer = processer(self.script)
        self.processer.set_inter(inter_ceil)
        self.processer.update()

    def train_mab(self):
        train_data = []
        train_mab_num = 100
        for i in range(train_mab_num):
            train_data.append(self.simulator.sim())
        self.processer.train(train_data)
        self.processer.set_inter(self.processer.mab_inter.inter)

    def once(self):
        sample = self.simulator.sim()
        return self.processer.test(sample)
    
    def avg(self,times):
        ans = 0.
        for i in range(times):
            ans += self.once()
        
        return ans / float(times)