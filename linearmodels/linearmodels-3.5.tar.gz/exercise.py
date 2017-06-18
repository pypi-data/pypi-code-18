from linearmodels.system.model import SUR
from linearmodels.tests.system._utility import generate_data, simple_sur
import pandas as pd
p = []
s = []
for i in range(1):
    data = generate_data(n=100, k=8, p=3, seed=i)
    mod = SUR(data)
    r = pd.DataFrame(columns=mod.param_names,index=['0','1'])
    r.iloc[:,:] = 0
    r.iloc[0,::7] = 1
    r.iloc[1, ::5] = 1
    mod.add_constraints(r)
    res = mod.fit(cov_type='robust', debiased=True, method='gls', iterate=True)

    p.append(res.params)
    s.append(res.std_errors)

print(res)
print(res.equations[res.equation_labels[0]])
#print(p)


