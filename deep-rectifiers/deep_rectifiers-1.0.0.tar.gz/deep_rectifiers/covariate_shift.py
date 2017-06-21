#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jun  2 00:54:52 2017

@author: aidanrocke
"""

import numpy as np

#lets check KL divergence for sigmoid and linear:
    
def linear():
	# create model
    model = Sequential()
    model.add(Dense(num_pixels, use_bias=True,input_dim=num_pixels, kernel_initializer='normal', activation='linear'))
    model.add(Dense(1000, use_bias=True,kernel_initializer='normal', activation='linear'))
    model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))
	# Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

LM = linear()

linear_history = LM.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, verbose=2)


from keras.models import Model
from scipy.stats import pearsonr as pear

layer = LM.layers[0]
intermediate_layer_model = Model(inputs=LM.input,
                                 outputs=layer.output)
int_1  = intermediate_layer_model.predict(X_train)

layer0 = LM.layers[1]
intermediate_layer_model = Model(inputs=LM.input,
                                 outputs=layer0.output)
int_2 = intermediate_layer_model.predict(X_train)

scores = np.zeros(100)

for i in range(100):
    Z1 = np.random.choice(int_2[i],784,replace=False)
    scores[i] = abs(np.min(np.corrcoef(Z1,int_1[i])))
    
entropies = np.zeros(100)

for i in range(100):
    Z1 = np.random.choice(int_2[i],784,replace=False)
    entropies[i] = mf(Z1,int_1[i])
        
#what happens when we use the sigmoid?
    
#sigmoid model:
def sigmoid():
	# create model
    model = Sequential()
    model.add(Dense(num_pixels, use_bias=True,input_dim=num_pixels, kernel_initializer='normal', activation='sigmoid'))
    model.add(Dense(1000, use_bias=True,kernel_initializer='normal', activation='sigmoid'))
    model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))
	# Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    return model


sig = sigmoid()

sig_history = sig.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, verbose=2)


from keras.models import Model

layer = sig.layers[0]
intermediate_layer_model = Model(inputs=sig.input,
                                 outputs=layer.output)
int_1  = intermediate_layer_model.predict(X_train)

layer0 = sig.layers[1]
intermediate_layer_model = Model(inputs= sig.input,
                                 outputs=layer0.output)
int_2 = intermediate_layer_model.predict(X_train)
    

entropies = np.zeros(100)

for i in range(100):
    Z1 = np.random.choice(int_2[i],784,replace=False)
    entropies[i] = mf(Z1,int_1[i])
    
entropies = np.zeros(100)

for i in range(100):
    Z1 = np.random.choice(int_2[i],784,replace=False)
    entropies[i] = entropy(Z1,int_1[i])

def real_exp():
	# create model
    model = Sequential()
    model.add(Dense(num_pixels, use_bias=True,input_dim=num_pixels, kernel_initializer='normal', activation=exp))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    model.add(Dense(1000, use_bias=True,kernel_initializer='normal', activation=exp))
    model.add(BatchNormalization())
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))
	# Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    
    return model

model = real_exp()
# Fit the model
history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, verbose=2)


layer = model.layers[0]
intermediate_layer_model = Model(inputs=model.input,
                                 outputs=layer.output)
int_1  = intermediate_layer_model.predict(X_train)

layer0 = model.layers[1]
intermediate_layer_model = Model(inputs= model.input,
                                 outputs=layer0.output)
int_2 = intermediate_layer_model.predict(X_train)

entropies = np.zeros(100)

for i in range(100):
    Z1 = np.random.choice(int_2[i],784,replace=False)
    entropies[i] = entropy(Z1,int_1[i])