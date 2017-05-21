import numpy as np
class algs(object):

    def get_train_bound(self):
        return self.low_bound, self.up_bound

    def train_bound(self):
        self.low_bound = np.zeros((self.T,self.J))
        self.up_bound = np.zeros((self.T,self.J))
        for t in range(self.T):
            for j in range(self.J):
                stat = []
                for data in self.D:
                    stat.append(data[t,j])
                self.low_bound[t,j] = np.percentile(stat,0.5)
                self.up_bound[t,j] = np.percentile(stat,99.5)
                
                self.low_bound[t,j] = max(self.low_bound[t,j]-2,0)
                if self.low_bound[t,j] == self.up_bound[t,j]:
                    self.up_bound[t,j] += 1
    
    def set_D(self,D):
        self.D = D
        self.T = np.shape(self.D[0])[0]
        self.J = np.shape(self.D[0])[1]
        self.train_bound()

    def set_script(self,script):
        self.script = script

    def get_relation(self):
        return self.P

