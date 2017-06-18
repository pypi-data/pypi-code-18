
# coding: utf-8

# # Examples

# ## Data

# In[41]:


# get_ipython().magic('matplotlib inline')
import numpy as np
from linearmodels.datasets import munnell
data = munnell.load()

regions = {
    'GF':['AL', 'FL', 'LA', 'MS'],
    'MW':['IL', 'IN', 'KY', 'MI', 'MN', 'OH', 'WI'],
    'MA':['DE', 'MD', 'NJ', 'NY', 'PA', 'VA'],
    'MT' :['CO', 'ID', 'MT', 'ND', 'SD', 'WY'],
    'NE' :['CT', 'ME', 'MA', 'NH', 'RI', 'VT'],
    'SO' :['GA', 'NC', 'SC', 'TN', 'WV', 'AR'],
    'SW' : ['AZ', 'NV', 'NM', 'TX', 'UT'],
    'CN': ['AK', 'IA','KS', 'MO','NE','OK'],
    'WC': ['CA','OR','WA']
}

def map_region(state):
    for key in regions:
        if state in regions[key]:
            return key


data['REGION'] = data.ST_ABB.map(map_region)
data['TOTAL_EMP'] = data.groupby(['REGION','YR'])['EMP'].transform('sum')
data['EMP_SHARE'] = data.EMP / data.TOTAL_EMP
data['WEIGHED_UNEMP'] = data.EMP_SHARE * data.UNEMP


# In[42]:


grouped = data.groupby(['REGION','YR'])
agg_data = grouped[['GSP','PC','HWY','WATER','UTIL','EMP','WEIGHED_UNEMP']].sum()
for col in ['GSP','PC','HWY','WATER','UTIL','EMP']:
    agg_data['ln'+col] = np.log(agg_data[col])
agg_data['UNEMP'] = agg_data.WEIGHED_UNEMP
agg_data['Intercept'] = 1.0


# ## Basic Usage

# In[43]:


from collections import OrderedDict
mod_data = OrderedDict()
for region in ['GF','SW','WC','MT','NE','MA','SO','MW','CN']:
    region_data = agg_data.loc[region]
    dependent = region_data.lnGSP
    exog = region_data[['Intercept', 'lnPC', 'lnHWY', 'lnWATER', 'lnUTIL', 'lnEMP', 'UNEMP']]
    mod_data[region] = {'dependent': dependent, 'exog': exog}


# In[44]:


import pandas as pd
from linearmodels.system import SUR
mod = SUR(mod_data)
res = mod.fit(cov_type='unadjusted', method='gls', debiased=True, iter_limit=10)
cov = res.sigma
std = np.sqrt(np.diag(res.sigma)[:,None])
regions =  [k for k in mod_data.keys()]
corr = pd.DataFrame(cov / (std @ std.T), columns=regions, index=regions)

import seaborn as sns
import matplotlib.pyplot as plt
sns.heatmap(corr, vmax=.8, square=True)
plt.show()

corr.style.format('{:0.3f}')


# In[45]:


from IPython.display import Image, display_png
display_png(Image('correct-greene-table-10-2.png'))


# In[46]:


print(res)


# In[47]:


print(res.equations['GF'])


# In[48]:


params = []
for label in res.equation_labels:
    params.append(res.equations[label].params)
params = pd.concat(params,1)
params.columns = res.equation_labels
params.T.style.format('{:0.3f}')


# In[49]:


display_png(Image('correct-greene-table-10-1.png'))


# In[50]:


res_ols = mod.fit(method='ols', debiased=True, cov_type='unadjusted')
params = []
r2 = []
for label in res.equation_labels:
    params.append(res_ols.equations[label].params)
    r2.append(res_ols.equations[label].rsquared)
params = pd.concat(params,1)
params.columns = res.equation_labels
params = params.T
params['R2'] = r2
params.style.format('{:0.3f}')


# In[51]:


params = pd.concat([res_ols.params.iloc[1::7], res_ols.std_errors.iloc[1::7], 
 res.params.iloc[1::7], res.std_errors.iloc[1::7]],1)
params.columns=['OLS', 'OLS se', 'GLS', 'GLS se']
params.index = regions
params


# In[52]:


display_png(Image('correct-greene-table-10-3.png'))


# In[53]:


res_het = mod.fit(cov_type='robust', debiased=True)
print(res_het)


# ## Estimation Options

# ### Restricted Residual Covariance

# ### Iterative GLS

# In[54]:


mod.fit(cov_type='unadjusted',debiased=True,iterate=True)


# ### Alternative Covariance Estimators

# In[55]:


mod.fit(cov_type='robust',debiased=True)
mod.fit(cov_type='robust',)


# ## Pre-specified Residual Covariance Estimators

# In[56]:


avg_corr = (corr - np.eye(9)).mean().mean() * (81/72)
rho = np.ones((9,9)) * avg_corr  + (1-avg_corr) * np.eye(9)
sigma_pre = rho * (std @ std.T)
mod_pre_sigma = SUR(mod_data, sigma=sigma_pre)
res_pre = mod_pre_sigma.fit(cov_type='unadjusted', debiased=True)
print(res_pre.equations['GF'])


# ## Cross-Equation Restrictions

# In[57]:


mod.param_names[:14]


# In[58]:


r = pd.DataFrame(columns=mod.param_names, index=['rest{0}'.format(i) for i in range(1,9)], dtype=np.float64)
r.loc[:,:] = 0.0
r.iloc[:,6] = -1.0
r.iloc[:,13::7] = np.eye(8)
print(r.iloc[:,6::7])


# In[67]:


r2 = np.zeros((8*6, r.shape[1]))
loc = 0
for i in range(6):
    for j in range(8):
        r2[loc,i+1] = -1
        r2[loc,7*(j+1) + i+1] = 1
        loc += 1
r2=pd.DataFrame(r2, columns=mod.param_names)
mod.reset_constraints()
mod.add_constraints(r2)
mod.fit()


# In[ ]:


mod.add_constraints(r)
rest_res = mod.fit(cov_type='unadjusted', debiased=True)
print(rest_res.params.iloc[6::7])


# ## Multivariate OLS

# In[ ]:


import statsmodels.api as sm
from linearmodels.datasets import french
data = french.load()
factors = sm.add_constant(data[['MktRF']])
mv_ols = SUR.multivariate_ls(data[['S1V1','S1V3','S1V5','S5V1','S5V3','S5V5']], factors)
mv_ols_res = mv_ols.fit(cov_type='unadjusted')
print(mv_ols_res)


# ## Using GLS with common regressors

# In[ ]:


print(mv_ols.fit(cov_type='unadjusted', method='gls'))

