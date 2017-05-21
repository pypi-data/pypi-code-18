#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Mon May 15 20:30:41 2017

@author: lin
"""

from SIM import *
from SIM_Resolve_First import *
from piecewise_linear import *
from tri_linear import *
from opt_tri_linear import *

case = SIM_Resolve_First()
#algs = piecewise_linear()
#algs = tri_linear()
algs = opt_tri_linear()
sim = SIM(case,algs)

data = []
for i in range(1000):
    data.append(sim.simulator.sim())
algs.set_train_data(data)

sim.update()
#sim.train_mab()
print sim.avg(1000)