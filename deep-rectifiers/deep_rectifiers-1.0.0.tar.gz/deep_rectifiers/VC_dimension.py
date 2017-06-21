# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils
from sklearn import linear_model 

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

# load data
(X_train, y_train), (X_test, y_test) = mnist.load_data()

y = y_train
y_t = y_test

# flatten 28*28 images to a 784 vector for each image
num_pixels = X_train.shape[1] * X_train.shape[2]
X_train = X_train.reshape(X_train.shape[0], num_pixels).astype('float32')
X_test = X_test.reshape(X_test.shape[0], num_pixels).astype('float32')

# normalize inputs from 0-255 to 0-1
X_train = X_train / 255
X_test = X_test / 255

# one hot encode outputs
y_train = np_utils.to_categorical(y_train)
y_test = np_utils.to_categorical(y_test)
num_classes = y_test.shape[1]

#get logistic model:
logistic = linear_model.LogisticRegression()

logistic.fit(X_train[1:1000],y[1:1000])

logistic.score(X_train[1:1000],y[1:1000])
#99.7%

logistic.score(X_test[1:1000],y_t[1:1000])
#84%

#what if we increase the variable size representation:
Z = np.random.random((10000,784))

train_X = np.zeros((1000,10000))

for i in range(1000):
    train_X[i] = np.matmul(Z,X_train[i])
    
#do the same for the test data:
test_X = np.zeros((1000,10000))

for i in range(1000):
    test_X[i] = np.matmul(Z,X_test[i])
    
logistic.fit(train_X,y[0:1000])

logistic.score(train_X,y[0:1000])

logistic.score(test_X,y_t[0:1000])





