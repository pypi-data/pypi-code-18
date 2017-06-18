
# coding: utf-8

# # Using formulas to specify models
# 
# Formulas can be used to specify models using mostly standard [patsy](https://patsy.readthedocs.io/) syntax. Since system estimation is more complicated than the specification of a single model, there are two methods available to specify a system:
# 
# * Dictionary of formulas
# * Single formula separated using {}
# 
# These examples use data on fringe benefits from F. Vella (1993), "A Simple Estimator for Simultaneous Models with Censored
# Endogenous Regressors" which appears in Wooldridge (2002).  The model consists of two equations, one for hourly wage and the other for hourly benefits.  The initial model uses the same regressors in both equaitons. 

# In[29]:


import numpy as np
import pandas as pd
from linearmodels.datasets import fringe
data = fringe.load()


# ## Dictionary 
# 
# The dictionary syntax is virtually identical to standard patsy syntax where each eqaution is specified in a kay-value pair where the key is the equation label and the value is the formula. It is recommended to use an OrderedDict which will preserve equation order in results. Keys **must** be strings.

# In[25]:


from collections import OrderedDict
formula = OrderedDict()
formula['benefits'] = 'hrbens ~ educ + exper + expersq + union + south + nrtheast + nrthcen + male'
formula['earnings'] = 'hrearn ~ educ + exper + expersq + nrtheast + married + male'


# In[27]:


from linearmodels.system import SUR
mod = SUR.from_formula(formula, data)
print(mod.fit(cov_type='unadjusted'))


# ## Curly Braces {}
# 
# The same formula can be expressed in a single string by surrounding each equation with braces `{}`.

# In[19]:


formula = '''
{hrbens ~ educ + exper + expersq + union + south + nrtheast + nrthcen + male}
{hrearn ~ educ + exper + expersq + nrtheast + married + male}
'''
mod = SUR.from_formula(formula, data)
braces_res = mod.fit(cov_type='unadjusted')
print(braces_res)


# ## Labeled Formulas

# In[24]:


formula = '''
{benefits: hrbens ~ educ + exper + expersq + union + south + nrtheast + nrthcen + male}
{earnings: hrearn ~ educ + exper + expersq + nrtheast + married + male}
'''
labeles_mod = SUR.from_formula(formula, data)
labeled_res = mod.fit(cov_type='unadjusted')

print('Unlabeled')
print(braces_res.equation_labels)
print('Labeled')
print(labeled_res.equation_labels)


# ## Other Options

# ### Estimation Weights
# 
# SUR supports weights which are assumed to be proportional to the inverse variance of the data so that 
# 
# $$ V(y_i \times w_i) = \sigma^2 \,\,\forall i.$$
# 
# Weights can be passed using a `DataFrame` where each column.  
# 
# Here the results are printed to ensure that the estimates are different from those in the standard GLS model.

# In[33]:


random_weights = np.random.chisquare(5, size=(616,2))
random_weights = pd.DataFrame(random_weights, columns=['benefits', 'earnings'])
weighted_mod = SUR.from_formula(formula, data, weights=random_weights)
print(weighted_mod.fit())


# ### Pre-specified Residual Covariance
# Like a standard SUR, it is possible to pass a pre-specified residual covariance for use in the GLS step.  This is done using the keyword argument `sigma` in the `from_formula` method, and is otherwise identical to passing one to the standard SUR.
