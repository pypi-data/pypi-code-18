from tri_linear import *
import numpy as np
from gurobipy import *
from scipy.optimize import minimize
class opt_tri_linear(tri_linear):

#Method 1: Gradient Descent

#Method 2: Alternating Iterative

#Now I Use Gradient Descent

    def optimize_theta(self):
        self.invA = {}
        for l in range(self.script.L):
            self.invA[l] = []

        for (a,b) in self.script.A.items():
            for i in b:
                self.invA[i].append(a)
        
        self.theta_depend = {}
        for i in range(self.J):
            self.theta_depend[i] = set()
            
        for l in range(self.script.L):
            for b in self.invA[l]:
                self.theta_depend[b] = self.theta_depend[b].union(self.invA[l])
        
        self.theta = np.zeros((self.J,self.J))
        for j in range(self.J):
            self.theta[j,j] = 1
            #self.theta[j,self.theta_depend[j].pop()] = 0.5
        theta_0 = []
        for j in range(self.J):
            for k in self.theta_depend[j]:
                theta_0.append(self.theta[j,k])
        theta_0 = np.array(theta_0)
        
        np.set_printoptions(threshold=np.nan)
        res = self.optimize_x(theta_0[0],0,theta_0.copy())
        '''
        stage = 3
        for i in range(stage):
            for j in range(len(theta_0)):
                print "Optimize",i,j
                line = np.linspace(0,1,3)
                #line = [theta_0[j]]
                maxm = 0
                for in_theta in line:
                    res = self.optimize_x(in_theta,j,theta_0.copy())
                    if res > maxm:
                        maxm = res
                        p = in_theta
                    #res.append() opminimize(self.optimize_x, theta_0[j], args=(j,theta_0) , method = 'Nelder-Mead', options = {'maxiter':5})
                theta_0[j] = p
        '''
        count = 0
        for j in range(self.J):
            for k in self.theta_depend[j]:
                self.theta[j,k] = theta_0[count]
                count += 1
                
        #print self.theta

    def optimize_x(self,in_theta, j, theta_0):
        theta_0[j] = in_theta
        theta = np.zeros((self.J,self.J))
        
        count = 0
        for j in range(self.J):
            for k in self.theta_depend[j]:
                theta[j,k] = theta_0[count]
                count += 1                
        
        #print theta
        
        model = Model("Optimize X given theta")
        X = {}
        for t in range(self.T):
            for j in range(self.J):
                for x in range(self.div_x_num):
                    for y in range(self.div_y_num):
                        X[t,j,x,y] = model.addVar(lb = 0, ub = self.div_x_axis[t,j,x])

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
                            obj += X[t,j,x,y] * self.value(t,j,x,y,x_val,y_val) * self.script.V[j]
                            #print test_var, self.value(t,j,x,y,x_val,y_val) 
        obj = obj / float(len(self.train_data))
        model.setObjective(obj,GRB.MAXIMIZE)

        for data in self.train_data:
            
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
                                constriant += X[t,j,x,y] * self.value(t,j,x,y,x_val,y_val)
                                
                        #print t,j,x,y,x_val,y_val
                        #print y_val-self.div_y_axis[t,j,0],self.div_y_axis[t,j,self.div_y_num-1] - y_val
                model.addConstr(constriant <= self.script.C[l])

        model.update()
        model.optimize()
        '''
        for t in range(self.T):
            for j in range(self.J):
                for x in range(self.div_x_num):
                    for y in range(self.div_y_num):
        '''
        
        return model.getObjective().getValue()

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

    def strategy(self,t,history,X):
            '''
            print self.J
            print history
            '''
            sum_data = self.sum_history(history)
            product = np.zeros((self.script.J,1))
            for j in range(self.script.J):
                t_sum = 0
                if t >= 1:
                    for k in range(self.J):
                        t_sum = sum_data[t,k] * self.theta[j,k]
                        
                if t_sum <= self.history_low_bound[t,j]:
                    product[j] = X[t,j,self.xi[t,j,self.div_x_num-1,0]].X
                elif t_sum >= self.history_up_bound[t,j]:
                    product[j] = X[t,j,self.xi[t,j,self.div_x_num-1,self.div_y_num-1]].X
                else:
                    for k in range(1,self.div_y_num):
                        if self.div_y_axis[t,j,k] > t_sum:
                            break
                        
                    coef = (t_sum - self.div_y_axis[t,j,k-1]) / float(self.div_y_axis[t,j,k]-self.div_y_axis[t,j,k-1])
                    product[j] = (1-coef) * X[t,j,self.xi[t,j,self.div_x_num-1,k-1]].X + coef * X[t,j,self.xi[t,j,self.div_x_num-1,k]].X
            return product

    def update(self):
        self.train_history_bound()
        self.mesh()
        self.optimize_theta()
        self.piecewise()
        self.relation()