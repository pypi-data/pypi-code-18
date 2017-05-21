from algs import *
import numpy as np
class tri_linear(algs):

    def sum_history(self,data):
        sum_history = np.zeros((self.T,self.J))
            
        for t in range(1,self.T):
            for j in range(self.J):
                sum_history[t,j] = sum_history[t-1,j] + data[t-1,j]
        return sum_history

    def train_history_bound(self):
        history_D = []
        for data in self.D:
            history_D.append(self.sum_history(data))

        self.history_low_bound = np.zeros((self.T,self.J))
        self.history_up_bound = np.zeros((self.T,self.J))
        for t in range(1,self.T):
            for j in range(self.J):
                stat = []
                for data in history_D:
                    stat.append(data[t,j])
                self.history_low_bound[t,j] = np.percentile(stat,0.5)
                self.history_up_bound[t,j] = np.percentile(stat,99.5)
                if self.history_low_bound[t,j] == self.history_up_bound[t,j]:
                    self.history_up_bound[t,j] += 1
        
        for j in range(self.J):
            self.history_up_bound[0,j] = 1.
            self.history_low_bound[0,j] = 0.

    def mesh(self):
        self.div_x_num = 7
        self.div_y_num = 10
        self.div_x_axis = {}
        self.div_y_axis = {}
        
        self.constant = self.script.constant
        self.xi = self.script.xi

        for t in range(self.T):
            for j in range(self.J):
                for x in range(self.div_x_num):
                    self.div_x_axis[t,j,x] = self.low_bound[t,j] + (self.up_bound[t,j]-self.low_bound[t,j])/float(self.div_x_num - 1) * x

                for y in range(self.div_y_num):
                    self.div_y_axis[t,j,y] = self.history_low_bound[t,j] + (self.history_up_bound[t,j]-self.history_low_bound[t,j])/float(self.div_y_num - 1) * y
                    
        for t in range(self.T):
            for j in range(self.J):
                for x in range(self.div_x_num):
                    for y in range(self.div_y_num):
                        self.xi[t,j,x,y] = self.script.add_var(0,self.div_x_axis[t,j,x])



    def piecewise(self):
        for t in range(self.T):
            for j in range(self.J):
                left = {}
                for x in range(self.div_x_num):
                    for y in range(self.div_y_num):
                        left[self.xi[t,j,x,y]] = 1
                right = {}
                right[self.constant] = 1
                self.script.add_lin_equ(left,right)

                for x in range(self.div_x_num):
                    for y in range(self.div_y_num):
                        self.script.add_lin_greater({self.xi[t,j,x,y]:1},{self.constant:0})

        for t in range(self.T):
            for j in range(self.J):
                left = {self.xi[t,j]:1}
                right = {}
                for x in range(self.div_x_num):
                    for y in range(self.div_y_num):
                        right[self.xi[t,j,x,y]] = self.div_x_axis[t,j,x]

                self.script.add_lin_equ(left,right)

                left = {}
                for r in range(t):
                    left[self.xi[r,j]] = 1
                right = {}
                for x in range(self.div_x_num):
                    for y in range(self.div_y_num):
                        right[self.xi[t,j,x,y]] = self.div_y_axis[t,j,y]

                self.script.add_lin_equ(left,right)

    def value(self,t,j,x,y,v_x,v_y):
        if y < self.div_y_num - 1 and v_y >= self.div_y_axis[t,j,y+1]:
            return 0
        if y > 0 and v_y <= self.div_y_axis[t,j,y-1]:
            return 0
        if x < self.div_x_num - 1 and v_x >= self.div_x_axis[t,j,x+1]:
            return 0
        if x > 0 and v_x <= self.div_x_axis[t,j,x-1] :
            return 0
        
        if x == self.div_x_num - 1 and v_x >= self.div_x_axis[t,j,self.div_x_num - 1] \
        or x == 0 and v_x <= self.div_x_axis[t,j,0]:
            if y == self.div_y_num - 1 and v_y >= self.div_y_axis[t,j,self.div_y_num -1] :
                return 1
            elif y < self.div_y_num - 1 and v_y >= self.div_y_axis[t,j,y+1]:
                return 0

            if y == 0 and v_y <= self.div_y_axis[t,j,0]:
                return 1
            elif y > 0 and v_y <= self.div_y_axis[t,j,y-1]:
                return 0

            if v_y > self.div_y_axis[t,j,y]:
                return (self.div_y_axis[t,j,y+1] - v_y) / (self.div_y_axis[t,j,y+1] - self.div_y_axis[t,j,y])
            else:
                return (v_y-self.div_y_axis[t,j,y-1]) / (self.div_y_axis[t,j,y] - self.div_y_axis[t,j,y-1])


        if y == self.div_y_num - 1 and v_y >= self.div_y_axis[t,j,self.div_y_num - 1] \
        or y == 0 and v_y <= self.div_y_axis[t,j,0]:
            if x == self.div_x_num - 1 and v_x >= self.div_x_axis[t,j,self.div_x_num - 1]:
                return 1
            elif x < self.div_x_num - 1 and v_x >= self.div_x_axis[t,j,x+1]:
                return 0

            if x == 0 and v_x <= self.div_x_axis[t,j,0]:
                return 1
            elif x > 0 and v_x <= self.div_x_axis[t,j,x-1]:
                return 0

            if v_x > self.div_x_axis[t,j,x]:
                return (self.div_x_axis[t,j,x+1] - v_x) / (self.div_x_axis[t,j,x+1] - self.div_x_axis[t,j,x])
            else:
                return (v_x-self.div_x_axis[t,j,x-1]) / (self.div_x_axis[t,j,x] - self.div_x_axis[t,j,x-1])
        
        def solve_linalg(x,y):
            '''
            print t,j
            print x
            print [self.div_x_axis[t,j,x[0]],self.div_x_axis[t,j,x[1]],self.div_x_axis[t,j,x[2]]]
            print y
            print [self.div_y_axis[t,j,y[0]],self.div_y_axis[t,j,y[1]],self.div_y_axis[t,j,y[2]]]
            
            latter = x[1]*y[2] - y[1]*x[2]
            return (v_x*y[1]+x[2]*v_y-y[2]*v_x-v_y*x[1] + latter)\
                    /(x[0]*y[1]+x[2]*y[0]-y[2]*x[0]-y[0]*x[1] + latter)
            '''
            A = np.zeros((3,3))
            b = np.zeros((3,1))
            A[0,0] = self.div_x_axis[t,j,x[0]]
            A[0,1] = self.div_x_axis[t,j,x[1]]
            A[0,2] = self.div_x_axis[t,j,x[2]]
            A[1,0] = self.div_y_axis[t,j,y[0]]
            A[1,1] = self.div_y_axis[t,j,y[1]]
            A[1,2] = self.div_y_axis[t,j,y[2]]
            A[2,:] = np.ones((1,3))
            b[0] = v_x
            b[1] = v_y
            b[2] = 1
            Lambda = np.linalg.solve(A,b)
            return Lambda[0]
            

        if v_y >= self.div_y_axis[t,j,y] and v_x >= self.div_x_axis[t,j,x]:
            p = np.array([v_x - self.div_x_axis[t,j,x], v_y - self.div_y_axis[t,j,y+1]])
            q = np.array([self.div_x_axis[t,j,x+1] - self.div_x_axis[t,j,x], self.div_y_axis[t,j,y] - self.div_y_axis[t,j,y+1]])
            if np.cross(p,q) <= 0:
                return 0
            else:
                return solve_linalg([x,x,x+1],[y,y+1,y])

        if v_y >= self.div_y_axis[t,j,y] and v_x <= self.div_x_axis[t,j,x]:
            '''
            print x,y
            print v_x,v_y
            print self.div_x_axis[t,j,x], self.div_y_axis[t,j,y]
            '''
            p = np.array([v_x - self.div_x_axis[t,j,x], v_y - self.div_y_axis[t,j,y]])
            q = np.array([self.div_x_axis[t,j,x-1] - self.div_x_axis[t,j,x], self.div_y_axis[t,j,y+1] - self.div_y_axis[t,j,y]])
            if np.cross(p,q) >= 0:
                return solve_linalg([x,x,x-1],[y,y+1,y+1])
            else:
                return solve_linalg([x,x-1,x-1],[y,y+1,y])

        if v_y <= self.div_y_axis[t,j,y] and v_x >= self.div_x_axis[t,j,x]:
            p = np.array([v_x - self.div_x_axis[t,j,x], v_y - self.div_y_axis[t,j,y]])
            q = np.array([self.div_x_axis[t,j,x+1] - self.div_x_axis[t,j,x], self.div_y_axis[t,j,y-1] - self.div_y_axis[t,j,y]])
            if np.cross(p,q) >= 0:
                return solve_linalg([x,x,x+1],[y,y-1,y-1])
            else:
                return solve_linalg([x,x+1,x+1],[y,y,y-1])

        if v_y <= self.div_y_axis[t,j,y] and v_x <= self.div_x_axis[t,j,x]:
            p = np.array([v_x - self.div_x_axis[t,j,x], v_y - self.div_y_axis[t,j,y-1]])
            q = np.array([self.div_x_axis[t,j,x-1] - self.div_x_axis[t,j,x], self.div_y_axis[t,j,y] - self.div_y_axis[t,j,y-1]])
            if np.cross(p,q) > 0:
                return solve_linalg([x,x,x-1],[y,y-1,y])
            else:
                return 0


    def lift_value(self,data):
        sum_data = self.sum_history(data)
        value = np.zeros((self.script.index,1))
        value[self.constant] = 1
        for t in range(self.T):
            for j in range(self.J):
                value[self.xi[t,j]] = data[t,j]
                for x in range(self.div_x_num):
                    for y in range(self.div_y_num):
                        value[self.xi[t,j,x,y]] = self.value(t,j,x,y,data[t,j],sum_data[t,j])
                        
        return value

    def relation(self):
        self.P = {}
        for t in range(self.T):
            for j in range(self.J):
                self.P[t,j] = []
                for x in range(self.div_x_num):
                    for y in range(self.div_y_num):
                        self.P[t,j].append(self.xi[t,j,x,y])
    
    def strategy(self,t,history,X):
        '''
        print self.J
        print history
        '''
        sum_history = self.sum_history(history)
        product = np.zeros((self.script.J,1))
        for j in range(self.script.J):
            if sum_history[t,j] <= self.history_low_bound[t,j]:
                product[j] = X[t,j,self.xi[t,j,self.div_x_num-1,0]].X
            elif sum_history[t,j] >= self.history_up_bound[t,j]:
                product[j] = X[t,j,self.xi[t,j,self.div_x_num-1,self.div_y_num-1]].X
            else:
                for k in range(1,self.div_y_num):
                    if self.div_y_axis[t,j,k] > sum_history[t,j]:
                        break
                    
                coef = (sum_history[t,j] - self.div_y_axis[t,j,k-1]) / float(self.div_y_axis[t,j,k]-self.div_y_axis[t,j,k-1])
                product[j] = (1-coef) * X[t,j,self.xi[t,j,self.div_x_num-1,k-1]].X + coef * X[t,j,self.xi[t,j,self.div_x_num-1,k]].X
        return product

    def update(self):
        self.train_history_bound()
        self.mesh()
        self.piecewise()
        self.relation()