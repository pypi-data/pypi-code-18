#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri May 19 23:26:05 2017

@author: aidanrocke
"""

import numpy as np
from scipy import linalg as LA


def LDA(data, labels, dim_rescale):
    '''
    Linear Discriminant Analysis
    pass in:
        (i) a raw data array--features encoded in the cols;
            one data instance per row;
        (ii) EV, explanatory variable, is included in D as last column;
        (iii) the LDA flag is set to False so PCA is the default techique;
            if both LDA & EV are set to True then LDA is performed
            instead of PCA
    returns:
        (i) eigenvalues (1D array);
        (ii) eigenvectors (2D array)
        (iii) covariance matrix
    some numerical assertions:
    >>> # sum of the eigenvalues is equal to trace of R
    >>> x = R.trace()
    >>> x1 = eva.sum()
    >>> np.allclose(x, x1)
    True
    >>> # determinant of R is product of eigenvalues
    >>> q = LA.det(R)
    >>> q1 = np.prod(eva)
    >>> np.allclose(q, q1)
    True
    '''
    assert data.shape[0] == labels.shape[0]
    # mean center the data array
    data -= data.mean(axis=0)
    nrow, ndim = data.shape
    # pre-allocate sw, sb arrays (both same shape as covariance matrix)
    # s_wc: array encoding 'within class' scatter
    # s_bc: array encoding 'between class' scatter
    s_wc = np.zeros((ndim, ndim))
    s_bc = np.zeros((ndim, ndim))
    R = np.cov(data.T)
    classes = np.unique(labels)
    for c in range(len(classes)):
        # create an index only for data rows whose class label = classes[c]
        idx = np.squeeze(np.where(labels == classes[c]))
        d = np.squeeze(data[idx,:])
        class_cov = np.cov(d.T)
        s_wc += float(idx.shape[0]) / nrow * class_cov
    s_bc = R - s_wc
    # now solve for w then compute the mapped data
    evals, evecs = LA.eig(s_wc, s_bc)
    np.ascontiguousarray(evals)
    np.ascontiguousarray(evecs)
    # sort the eigenvectors based on eigenvalues sort order
    idx = np.argsort(evals)
    idx = idx[::-1]
    evecs = evecs[:,idx]
    # take just number of eigenvectors = dim_rescale
    evecs_dr = evecs[:,:dim_rescale]
    # multiply data array & remaining set of eigenvectors
    rescaled_data = np.dot(data, evecs_dr)
    return rescaled_data, evecs_dr

def feature_importance(trained_model,validate_X,validate_Y):
    
    yhat = np.round(model.predict(validate_X))
    
    # get boolean array of correctly mapped indices:
    boolean = np.array(yhat == validate_Y)
    
    X = validate_X[boolean[:,0]]
    Y = validate_Y[boolean[:,0]]
    
    N, M = np.shape(validate_X)
    
    importance = np.zeros(M)
    
    for i in range(M):
        
        mu = np.mean(X[:,i])
        sigma = np.std(X[:,i])
        
        Xhat = X
        
        Xhat[:,i] = np.random.normal(mu,sigma)
        
        importance[i] = 1 - np.mean(np.round(model.predict(Xhat)) == Y)
        
    return importance


"""
#let's see what the difference is between the ordinary approach 
ind = np.argpartition(importance, -15)[-15:]

X = validate_X[:,ind]

model = create_model([15,500,500,1],0.8,1,'elu','sigmoid','binary_crossentropy')


from xgboost import XGBClassifier
from xgboost import plot_importance
from matplotlib import pyplot

model = XGBClassifier()
model.fit(train_X, train_Y)

# fit model no training data
model = XGBClassifier()
model.fit(train_X, train_Y)
# plot feature importance
plot_importance(model)
pyplot.show()
"""
    
    
    
    