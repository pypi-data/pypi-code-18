a#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue May 30 14:18:07 2017

@author: aidanrocke
"""


import numpy as np
from keras.datasets import mnist
from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout
from keras.utils import np_utils

# fix random seed for reproducibility
seed = 7
np.random.seed(seed)

# load data
(X_train, y_train), (X_test, y_test) = mnist.load_data()

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

from keras import backend as K

def exp(x):
    return K.exp(x)



from keras.layers.normalization import BatchNormalization

#define small exp model:
# define baseline model
def small_exp():
	# create model
	model = Sequential()
	model.add(Dense(num_pixels, input_dim=num_pixels, kernel_initializer='normal', activation=exp))
	model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))
	# Compile model
	model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
	return model

model = small_exp()
# Fit the model
model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, verbose=2)

# Final evaluation of the model
small_scores = model.evaluate(X_test, y_test, verbose=0)


# define exponential model
def naive_exp():
	# create model
    model = Sequential()
    model.add(Dense(num_pixels, use_bias=True,input_dim=num_pixels, kernel_initializer='normal', activation=exp))
    model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))
	# Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# define linear model
# build the models:
def exponential():
	# create model
    model = Sequential()
    model.add(Dense(num_pixels, use_bias=True,input_dim=num_pixels, kernel_initializer='normal', activation=exp))
    model.add(Dense(1000, use_bias=True,kernel_initializer='normal', activation=exp))
    model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))
	# Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

# define linear model
def linear():
	# create model
    model = Sequential()
    model.add(Dense(num_pixels, use_bias=True,input_dim=num_pixels, kernel_initializer='normal', activation='linear'))
    model.add(Dense(num_classes, kernel_initializer='normal', activation='softmax'))
	# Compile model
    model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
    return model

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

# build the model
LM = linear()
naive_exp = exponential()

#get intermediate values:
layer = exponential.layers[0]
intermediate_layer_model = Model(inputs=exponential.input,
                                 outputs=model.get_layer(layer_name).output)
intermediate_output = intermediate_layer_model.predict(X_train[0])

exp_scores = naive_exp.evaluate(X_test, y_test, verbose=0)

# Fit the model
linear_history = LM.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, verbose=2)


# build the model
LM = linear()
exponential = exponential()
# Fit the model
exp_history = exponential.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, verbose=2)

# Final evaluation of the model
linear_scores = LM.evaluate(X_test, y_test, verbose=0)

linear = linear_history.history['acc']

# compare with sigmoid:
sigmoid_history = sigmoid.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=10, batch_size=200, verbose=2)

sigmoid_scores = sigmoid.evaluate(X_test, y_test, verbose=0)

#create plot:
    
plt.figure(figsize=(10,10))

plt.title('exponential network with two hidden layers')

plt.plot(exp_history.history['acc'], label='accuracy')


plt.savefig('/Users/aidanrocke/Desktop/pauli-space.github.io/_images/exp_history2.png')

def jacobian(y, x):
  y_flat = tf.reshape(y, (-1,))
  jacobian_flat = tf.stack(
      [tf.gradients(y_i, x)[0] for y_i in tf.unstack(y_flat)])
  return tf.reshape(jacobian_flat, y.shape.concatenate(x.shape))

import theano as T

jacobian = T.gradient.jacobian(LM.predict(),x)

#getting gradients:
    
outputTensor = LM.output #Or model.layers[index].output

listOfVariableTensors = model.trainable_weights

gradients = K.gradients(outputTensor, listOfVariableTensors)

trainingExample = np.random.random((1,784))
sess = tf.InteractiveSession()
sess.run(tf.initialize_all_variables())
evaluated_gradients = sess.run(gradients,feed_dict={model.input:X})


#an alternative approach:


    cost = model.model.total_loss
    grads = K.gradients(cost, trainable_params)

    return cost, grads

