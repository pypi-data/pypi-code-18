from tri_linear import *
import numpy as np
from gurobipy import *
from scipy.optimize import minimize
from inter import *
class opt_tri_linear(tri_linear):

#Method 1: Gradient Descent

#Method 2: Alternating Iterative

#Now I Use Gradient Descent

    def optimize_x(self,theta):             
        
        self.invA = {}
        for l in range(self.script.L):
            self.invA[l] = []

        for (a,b) in self.script.A.items():
            for i in b:
                self.invA[i].append(a)
                
        #print theta
        
        self.model = Model("Optimize X given theta")
        self.X = {}
        for t in range(self.T):
            for j in range(self.J):
                for x in range(self.div_x_num):
                    for y in range(self.div_y_num):
                        self.X[t,j,x,y] = self.model.addVar(lb = 0, ub = self.div_x_axis[t,j,x])

        obj = LinExpr()
        for data in self.train_data:
            sum_data = self.sum_history(data)
            for t in range(self.T):
                for j in range(self.J):
                    x_val = data[t,j]
                    y_val = 0
                    for k in range(self.J):
                        y_val += theta[j,k] * sum_data[t,k]
                        
                    for x in range(self.div_x_num):
                        for y in range(self.div_y_num):
                            obj += self.X[t,j,x,y] * self.value(t,j,x,y,x_val,y_val) * self.script.V[j]
                            #print test_var, self.value(t,j,x,y,x_val,y_val) 
        obj = obj / float(len(self.train_data))
        self.model.setObjective(obj,GRB.MAXIMIZE)

        '''
            for t in range(self.T):
                for j in range(self.J):
                    constriant = LinExpr()
                    x_val = data[t,j]
                    y_val = 0
                    for k in range(self.J):
                        y_val += theta[j,k] * sum_data[t,k]

                    for x in range(self.div_x_num):
                        for y in range(self.div_y_num):
                            constriant += self.X[t,j,x,y] * self.value(t,j,x,y,x_val,y_val)
                    model.addConstr(constriant >= 0)

            for t in range(self.T):
                for j in range(self.J):
                    constriant = LinExpr()
                    x_val = data[t,j]
                    y_val = 0
                    for k in range(self.J):
                        y_val += theta[j,k] * sum_data[t,j]

                    for x in range(self.div_x_num):
                        for y in range(self.div_y_num):
                            constriant += self.X[t,j,x,y] * self.value(t,j,x,y,x_val,y_val)
                    model.addConstr(constriant <= data[t,j])

                    '''
        for data in self.train_data:
            sum_data = self.sum_history(data)
            for l in range(self.script.L):
                constriant = LinExpr()
                for j in self.invA[l]:
                    for t in range(self.T):
                        x_val = data[t,j]
                        y_val = 0
                        for k in range(self.J):
                            y_val += theta[j,k] * sum_data[t,k]
                        for x in range(self.div_x_num):
                            for y in range(self.div_y_num):
                                constriant += self.X[t,j,x,y] * self.value(t,j,x,y,x_val,y_val)
                                
                        #print t,j,x,y,x_val,y_val
                        #print y_val-self.div_y_axis[t,j,0],self.div_y_axis[t,j,self.div_y_num-1] - y_val
                self.model.addConstr(constriant <= self.script.C[l])

        self.model.update()
        self.model.optimize()
        '''
        for t in range(self.T):
            for j in range(self.J):
                for x in range(self.div_x_num):
                    for y in range(self.div_y_num):
        '''
        
        return self.model.getObjective().getValue()

    def set_train_data(self,train_data):
        self.train_data = train_data

    def piecewise(self):
        self.constant = self.script.constant
        self.xi = self.script.xi
        self.sum_xi = {}
        for t in range(0,self.T):
            for j in range(self.J):
                self.sum_xi[t,j] = self.script.add_var(0,0)

        for t in range(1,self.T):
            for j in range(self.J):
                left = {self.sum_xi[t,j]:1}
                right = {}
                for u in range(t):
                    right[self.xi[u,j]] = 1
                self.script.add_lin_equ(left,right)

        for t in range(self.T):
            for j in range(self.J):
                self.y_var = self.script.add_var(0,0)

        for t in range(self.T):
            for j in range(self.J):
                left = {self.y_var:1}
                right = {}
                for k in range(self.J):
                    right[self.sum_xi[t,k]] = self.theta[j,k]
                self.script.add_lin_equ(left,right)

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

                left = {self.y_var[t,j]:1}
                right = {}
                for x in range(self.div_x_num):
                    for y in range(self.div_y_num):
                        right[self.xi[t,j,x,y]] = self.div_y_axis[t,j,y]

                self.script.add_lin_equ(left,right)
    
    def lift_value(self,data):
        sum_data = self.sum_history(data)
        value = np.zeros((self.script.index,1))
        value[self.constant] = 1
        for t in range(self.T):
            for j in range(self.J):
                value[self.xi[t,j]] = data[t,j]
                t_sum = 0
                if t >= 1:
                    for k in range(self.J):
                        t_sum = sum_data[t,k] * self.theta[j,k]
                for x in range(self.div_x_num):
                    for y in range(self.div_y_num):
                        value[self.xi[t,j,x,y]] = self.value(t,j,x,y,data[t,j],t_sum)
                        
        return value
    
    def set_inter(self,inter):
        self.inter = inter
    
    def once(self,sample):
        C = self.script.C.copy()
        V = self.script.V
        val = 0
        his = self.sum_history(sample)
        for t in range(self.script.T):
            product = self.strategy(t,sample, his)
            
            #product = product.reshape(self.script.J)
            
            for j in range(self.script.J):
                product[j] = self.inter(t,j,product[j])
                product[j] = min(product[j], sample[t,j])
                
                for l in self.script.A[j]:
                    product[j] = min(product[j],C[l])

                val += product[j] * V[j]
                for l in self.script.A[j]:
                    C[l] -= product[j]

        return val
            
    
    def strategy(self,t,data,sum_data):
            obj = np.zeros(self.J)
            for j in range(self.J):
                x_val = data[t,j]
                y_val = 0
                for k in range(self.J):
                    y_val += self.theta[j,k] * sum_data[t,k]

                for x in range(self.div_x_num):
                    for y in range(self.div_y_num):
                        obj[j] += self.X[t,j,x,y].X * self.value(t,j,x,y,x_val,y_val) 
                        #print test_var, self.value(t,j,x,y,x_val,y_val) 
            return obj
            '''
            sum_data = self.sum_history(history)
            product = np.zeros((self.script.J,1))
            for j in range(self.script.J):
                t_sum = 0
                if t >= 1:
                    for k in range(self.J):
                        t_sum = sum_data[t,k] * self.theta[j,k]
                        
                if t_sum <= self.history_low_bound[t,j]:
                    product[j] = X[t,j,self.div_x_num-1,0].X
                elif t_sum >= self.history_up_bound[t,j]:
                    product[j] = X[t,j,self.div_x_num-1,self.div_y_num-1].X
                else:
                    for k in range(1,self.div_y_num):
                        if self.div_y_axis[t,j,k] > t_sum:
                            break
                        
                    coef = (t_sum - self.div_y_axis[t,j,k-1]) / float(self.div_y_axis[t,j,k]-self.div_y_axis[t,j,k-1])
                    product[j] = (1-coef) * X[t,j,self.div_x_num-1,k-1].X + coef * X[t,j,self.div_x_num-1,k].X
            return product
            '''

    def update(self):
        self.train_history_bound()
        self.mesh()
        self.theta = np.identity(self.J)
        self.optimize_x(self.theta)