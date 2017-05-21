import algs
import numpy as np
class linear(algs):
	def __init__(self):
		algs.__init__(self):

	def piecewise(self):
		self.constant = self.script.constant
		self.xi = self.script.xi
		
		for t in range(self.T):
			for j in range(self.J):
				for t_pre in range(t):
					for j_pre in range(j):
						self.xi[t,j,t_pre,j_pre] = self.script.add_var()

	def lift_value(self,data):
		value = np.zeros((self.script.index,1))
		value[self.constant] = 1
		for t in range(self.T):
			for j in range(self.J):
				value[self.xi[t,j]] = data[t,j]
				for t_pre in range(t):
					for j_pre in range(j):
						value[self.xi[t,j,t_pre,j_pre]] = data[t,j]
		return value

	def get_relation(self):
		return self.P

	def relation(self):
		self.P = {}
		for t in range(self.T):
			for j in range(self.J):
				self.P[t,j] = []
				for t_pre in range(t):
					for j_pre in range(j):
						self.P[t,j].append(self.xi[t,j,t_pre,j_pre])

	def update(self):
		self.piecewise()
		self.relation()