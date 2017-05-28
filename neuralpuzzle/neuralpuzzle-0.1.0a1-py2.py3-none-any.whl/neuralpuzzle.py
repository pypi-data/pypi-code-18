# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
import os.path
import pickle
import numpy as np
from .optimizer import *
from .gen_network import *
from .gen_cnn import *
from .train_network import *

class NeuralPuzzle(object):
    def __init__(self, data, layer_list, activation, weights, weight_decay=0, use_batchnorm=False, epochs=20, mini_batch_size=100, optimizer="SGD", optimizer_param={'lr':0.01}, verbose=True, cnn=False, filter_size=3, padding=[1], stride=1):
        self.data = data
        self.layer_list = layer_list
        self.activation = activation
        self.weights = weights
        self.weight_decay = weight_decay
        self.use_batchnorm = use_batchnorm
        self.epochs = epochs
        self.batch_size = mini_batch_size
        self.optimizer = optimizer
        self.optimizer_param = optimizer_param
        self.verbose = verbose
        self.cnn = cnn
        self.filter_size = filter_size
        self.padding = padding
        self.stride = stride


        if self.cnn:
            (self.train_input, self.train_output), (self.test_input, self.test_output) = self.load(self.data, flatten=False)
            self.input_dim = (1, 28, 28)
            self.network = DeepConvNet(slef.input_dim, self.layer_list, self.activation, self.filter_size, self.padding, self.stride)
        else:
            (self.train_input, self.train_output), (self.test_input, self.test_output) = self.load(self.data)
            self.network = MultipleLayerNetwork(self.layer_list, self.activation, self.weights, self.weight_decay, self.use_batchnorm)

        self.trainer = Trainer(self.network, self.train_input, self.train_output, self.test_input, self.test_output, self.epochs, self.batch_size, self.optimizer, self.optimizer_param, self.verbose)

        self.trainer.train()


    def load(self, normalize=True, flatten=True, one_hot_label=False):
        with open(self.data, 'rb') as f:
            dataset = pickle.load(f)

        if normalize:
            for key in ('train_img', 'test_img'):
                dataset[key] = dataset[key].astype(np.float32)
                dataset[key] /= 255.0

        if one_hot_label:
            dataset['train_label'] = _change_one_hot_label(dataset['train_label'])
            dataset['test_label'] = _change_one_hot_label(dataset['test_label'])

        if not flatten:
             for key in ('train_img', 'test_img'):
                dataset[key] = dataset[key].reshape(-1, 1, 28, 28)

        return (dataset['train_img'], dataset['train_label']), (dataset['test_img'], dataset['test_label'])
