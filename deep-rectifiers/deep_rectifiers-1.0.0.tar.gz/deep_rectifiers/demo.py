#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Apr 18 22:50:53 2017

@author: aidanrocke
"""

import sys
import numpy as np
import pandas as pd


sys.path.insert(0,'/Users/aidanrocke/Desktop/scientific_deep_learning/deep_science')


from utils import create_model

#create several models:
model_1 = create_model([10,12,1],1,1,'relu','sigmoid','binary_crossentropy')
    
model_2 = create_model([100,102,1],1,1,'relu','sigmoid','binary_crossentropy')

model_3 = create_model([1000,1002,1],1,1,'relu','sigmoid','binary_crossentropy')

#create several data sets:
X_train1, Y_train1, X_test1, Y_test1 = datasets(0,100,10000,10,0.5)

X_train1b, Y_train1b, X_test1b, Y_test1b = datasets(0,10,10000,10,0.5)


X_train2, Y_train2, X_test2, Y_test2 = datasets(0,100,10000,100,0.5)
X_train2b, Y_train2b, X_test2b, Y_test2b = datasets(0,10,10000,100,0.5)


X_train3, Y_train3, X_test3, Y_test3 = datasets(0,100,10000,1000,0.5)
X_train3b, Y_train3b, X_test3b, Y_test3b = datasets(0,10,10000,1000,0.5)


# fit models to data:
    
#dataset 1:
history = model_1.fit(X_train1, Y_train1, nb_epoch=20, batch_size=1000, verbose=1)

eval_1 = model_1.evaluate(X_test1,Y_test1)
# [0.056188725310564042, 0.99795]
#dataset 2:
history = model_2.fit(X_train2, Y_train2, nb_epoch=20, batch_size=1000, verbose=1)

eval_2 = model_2.evaluate(X_test2,Y_test2)

#[0.00042243222850374878, 1.0]

#dataset 3:
history = model_3.fit(X_train3, Y_train3, nb_epoch=20, batch_size=1000, verbose=1)

eval_3 = model_3.evaluate(X_test3,Y_test3)

#now let's see how well they generalise to harder problems:
eval_1b = model_1.evaluate(X_test1b,Y_test1b)
#[0.56407629785537716, 0.5]

eval_2b = model_2.evaluate(X_test2b,Y_test2b)
#[1.0880742697238923, 0.5]

eval_3b = model_3.evaluate(X_test3b,Y_test3b)
#[7.9711923576354984, 0.5]









from keras import backend as K

def get_activations(model, layer, X_batch):
    get_activations = K.function([model.layers[0].input, K.learning_phase()], [model.layers[layer].output,])
    activations = get_activations([X_batch,0])
    return activations

    


history = model.fit(X_train1, Y_train1, nb_epoch=20, batch_size=1000, verbose=1)

CV_results = cross_validate(model, X_train1, Y_train1, 10,10,1000)

#get activations at the layer prior to sigmoid:
activations_2 = get_activations(model, 2, X_train1)
activations_3 = get_activations(model, 3, X_train1)


n = max(np.shape(activations_2[0]))

values = np.zeros(n)

for i in range(n):
    values[i] = np.sum(activations_2[0][i])
    
import matplotlib.pyplot as plt

plt.scatter(values,Y_train1)




