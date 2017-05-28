# -*- coding:utf-8 -*-
from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import numpy as np


def identity(node_input):
    return node_input


def step_function(node_input):
    '''
    Binary Step Function with Threshod 0

        f(x) := 1 if x > 0 or x = 0
        f(x) := 0 if x < 0

    It activates the neuron if the activation is above a certain value (0)
    '''
    out_puts = np.zeros(node_input)
    out_puts[node_input>=0] = 1
    return out_puts


def sigmoid(node_input):
    '''
    Logistic Sigmoid Function (Binary Sigmoid Funciton)

        f(x) := 1/(1+exp(-x))

    It is one of the most used activation function in neural network.
    It returns values restricted to the open interval (0, 1)
    '''
    return 1 / (1 + np.exp(-node_input))


def bipolar_sigmoid(node_input):
    return (1 - np.exp(-node_input)) / (1 + np.exp(-node_input))


def tanh(node_input):
    '''
    Hyperbolic Tangent Activation Fuction:
        f(x) := tanh(x)

    It is also a very common used activation function.
    It compressed the input into range (-1, 1)
    '''
    return np.tanh(node_input)


def relu(node_input):
    '''
    Rectified Linear Unit (ReLU):
        f(x) := max(0, x)

    It was introduced in 2000 by Teh & Hinton.
    ReLU is a linear, none-saturating function.
    Performs better than other activation fucntins fro hidden layers

    '''
    return np.maximum(0, node_input)


def softmax(node_output):
    '''Softmacx Activation Function:
    .. math::
        f(x)_i = exp(xi) / sum(exp(xk)) where i = 1, ..., k

    It usually found in the output layer of the neural network.
    And mostly used on a classification neural network
    '''
    e = np.exp(node_output - np.max(node_output))
    if e.ndim ==1:
        return e / np.sum(e, axis=0)
    else: return e/ np.array([np.sum(e, axis=1)]).T


def mean_squared_error(outputs, true_val):
    return 0.5 * np.sum((outputs - true_val)**2)


def cross_entropy(outputs, true_val):
    if outputs.ndim == 1:
        true_val = true_val.reshape(1, true_val.size)
        outputs = outputs.reshape(1, outputs.size)

    if true_val.size == outputs.size:
        true_val = true_val.argmax(axis=1)

    batch_size = outputs.shape[0]
    return -np.sum(np.log(outputs[np.arange(batch_size), true_val])) / batch_size


def softmax_with_loss(inputs, true_val):
    outputs = softmax(inputs)
    return cross_entropy(outputs, true_val)


def  numerical_gradient(func, inputs):
    h = 1e-4
    grad = np.zeros_like(x)

    it = np.nditer(inputs, flags=['multi_index'], op_flags=['readwrite'])
    while not it.finished:
        idx = it.multi_index
        tmp_val = x[idx]
        x[idx] = float(tmp_val) + h
        delta1 = func(x)

        x[idx] = tmp_val -h
        delta2 =- func(x)
        grad[idx] = (dalta1 - datla2) / (2*h)

        x[idx] = tmp_val
        it.iternext()

    return grad
