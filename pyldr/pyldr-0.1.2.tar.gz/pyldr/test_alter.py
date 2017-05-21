
from SIM import *
from SIM_Resolve_First import *
from piecewise_linear import *
from tri_linear import *
from alter_solve import *
from script import *


case = SIM_Resolve_First()
#algs = piecewise_linear()
#algs = tri_linear()
algs = opt_tri_linear()
sim = SIM(case,algs)

data = []
for i in range(10):
    data.append(sim.simulator.sim())
algs.set_train_data(data)

sim.generate_data()
sim.script = script(sim.simulator.A,sim.D,sim.simulator.v,sim.simulator.c,sim.algs)
sim.algs.update()

algs.once(sim.sim())