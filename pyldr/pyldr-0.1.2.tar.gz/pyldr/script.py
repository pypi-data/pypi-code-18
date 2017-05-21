import numpy as np
import scipy as sp
class script(object):
    def __init__(self,A,D,V,C,algs):
        self.A = A
        self.D = D
        self.V = V
        self.C = C
        self.L = len(self.C)
        self.algs = algs
        self.index = 0
        self.lin_inequ_W = []
        self.lin_equ_W = []
        self.algs.set_D(self.D)
        self.algs.set_script(self)
        self.init_var()
        

    def init_var(self):
        self.train_num = len(self.D)
        self.T = np.shape(self.D[0])[0]
        self.J = np.shape(self.D[0])[1]

        self.low_bound, self.up_bound = self.algs.get_train_bound()

        self.xi = {}
        self.lb = {}
        self.ub = {}
        INF = 9999999
        self.constant = self.add_var(-INF,INF)
        for t in range(self.T):
            for j in range(self.J):
                self.xi[t,j] = self.add_var(0,0)
                self.add_lin_greater({self.xi[t,j]:1},{self.constant:self.low_bound[t,j]})
                self.add_lin_less({self.xi[t,j]:1},{self.constant:self.up_bound[t,j]})

    def add_var(self,lb,ub):
        self.lb[self.index] = lb
        self.ub[self.index] = ub
        self.index += 1
        return self.index - 1

    def add_lin_greater(self,left,right):
        self.add_lin_inequ(left,right)

    def add_lin_less(self,left,right):
        self.add_lin_inequ(right,left)

    def add_lin_inequ(self,left,right):
        self.lin_inequ_W.append((left,right))

    def add_lin_equ(self,left,right):
        self.lin_equ_W.append((left,right))

    def update(self):
        self.row_W = 2 + len(self.lin_inequ_W) + 2 * len(self.lin_equ_W)
        self.col_W = self.index
        self.W = sp.sparse.dok_matrix((self.row_W,self.col_W))
        #self.W = {}
        self.h = np.zeros((self.row_W,1))
        self.W[0,self.constant] = 1
        self.W[1,self.constant] = -1
        self.h[0] = 1
        self.h[1] = -1
        cur_row = 2
        for (left,right) in self.lin_inequ_W:
            for (a,b) in left.items():
                    self.W[cur_row,a] += b
                          
            for (a,b) in right.items():
                   self.W[cur_row,a] += -b
            cur_row += 1

        for (left,right) in self.lin_equ_W:
            for (a,b) in left.items():
                    self.W[cur_row,a] += b
                          
            for (a,b) in right.items():
                   self.W[cur_row,a] += -b
            cur_row += 1

            for (a,b) in left.items():
                    self.W[cur_row,a] += -b
                          
            for (a,b) in right.items():
                   self.W[cur_row,a] += b
            cur_row += 1
        '''
        for (left,right) in self.lin_inequ_W:
            for (a,b) in left.items():
                if (cur_row,a) in self.W:
                    self.W[cur_row,a] += b
                else:
                    self.W[cur_row,a] = b
                          
            for (a,b) in right.items():
                if (cur_row,a) in self.W:
                   self.W[cur_row,a] += -b
                else:
                    self.W[cur_row,a] = -b
            cur_row += 1

        for (left,right) in self.lin_equ_W:
            for (a,b) in left.items():
                if (cur_row,a) in self.W:
                    self.W[cur_row,a] += b
                else:
                    self.W[cur_row,a] = b
                          
            for (a,b) in right.items():
                if (cur_row,a) in self.W:
                   self.W[cur_row,a] += -b
                else:
                    self.W[cur_row,a] = -b
            cur_row += 1

            for (a,b) in left.items():
                if (cur_row,a) in self.W:
                    self.W[cur_row,a] += -b
                else:
                    self.W[cur_row,a] = -b
                          
            for (a,b) in right.items():
                if (cur_row,a) in self.W:
                   self.W[cur_row,a] += b
                else:
                    self.W[cur_row,a] = b
            cur_row += 1
        '''

        self.E = np.zeros((self.index,1))
        for data in self.D:
            self.E += self.algs.lift_value(data)
        self.E /= float(len(self.D))

        self.P = self.algs.get_relation()
        '''
        row = []
        col = []
        data = []
        for (a,b) in self.W.items():
            row.append(a[0])
            col.append(a[1])
            data.append(b)
            
        self.W = sp.sparse.csc_matrix((data,(row,col)))
        '''
        self.W = self.W.tocsc()
        
        #print "Sparse Ratio:", self.W.getnnz()/float(self.row_W*self.col_W)