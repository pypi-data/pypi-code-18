#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Wed May 17 19:27:37 2017

@author: lin
"""


from SIM import *
from SIM_Resolve_First import *
from piecewise_linear import *
from tri_linear import *
from opt_tri_linear import *
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

case = SIM_Resolve_First()
#algs = piecewise_linear()
#algs = tri_linear()
algs = opt_tri_linear()
sim = SIM(case,algs)

data = []
for i in range(30):
    data.append(sim.simulator.sim())
algs.set_train_data(data)

sim.generate_data()
sim.script = script(sim.simulator.A,sim.D,sim.simulator.v,sim.simulator.c,sim.algs)
algs.train_history_bound()
algs.mesh()

t = 3
j = 3
x = 0
y = 4
xx = np.linspace(algs.low_bound[t,j],algs.up_bound[t,j],20)
yy = np.linspace(algs.history_low_bound[t,j], algs.history_up_bound[t,j],20)
X, Y = np.meshgrid(xx,yy)
mem = np.zeros((20,20))
for a in range(20):
    for b in range(20):
        mem[a,b] = algs.value(t,j,x,y,xx[a],yy[b])

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.plot_wireframe(X, Y, mem)
print mem
plt.show()
#sim.algs.update()