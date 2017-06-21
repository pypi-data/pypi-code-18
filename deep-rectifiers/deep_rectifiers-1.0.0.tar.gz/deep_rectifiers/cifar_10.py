#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 15:01:55 2017

@author: aidanrocke
"""
import keras
from keras.datasets import cifar10
import sys
import numpy as np

sys.path.insert(0,'/Users/aidanrocke/Desktop/scientific_deep_learning/deep_science')

from utils import create_model

batch_size = 32
num_classes = 10


(x_train, y_train), (x_test, y_test) = cifar10.load_data()

# normalize inputs from 0-255 to 0-1
x_train = x_train / 255
x_test = x_test / 255

x_train, x_test = np.mean(x_train,3), np.mean(x_test,3)

num_pixels = x_train.shape[1] * x_train.shape[2]
x_train = x_train.reshape(x_train.shape[0], num_pixels).astype('float32')
x_test = x_test.reshape(x_test.shape[0], num_pixels).astype('float32')

y_train = keras.utils.to_categorical(y_train, num_classes)
y_test = keras.utils.to_categorical(y_test, num_classes)

#create model:
model = create_model([1024,500,500,10],0,0, 0,'relu','softmax','categorical_crossentropy','adam')

history = model.fit(X_train, y_train, validation_data=(X_test, y_test), epochs=15, batch_size=5000, verbose=2)

import matplotlib.pyplot as plt

plt.imshow(np.round(x_train[0]),cmap='gray')