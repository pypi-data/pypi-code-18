from collections import OrderedDict
from .layers import *
import numpy as np

class MultipleLayerNetwork:
    def __init__(self, layer_list, activation=['relu'], weight_init_std='he', weight_decay_lambda=0, use_batchnorm=False):
        self.layer_list = layer_list
        self.input_size = layer_list[0]
        self.output_size = layer_list[-1]
        self.hidden_size_list = layer_list[1:-1]
        self.hidden_layer_num = len(layer_list[1:-1])
        self.weight_init_std = weight_init_std
        self.weight_decay_lambda = weight_decay_lambda
        self.use_batchnorm = use_batchnorm
        self.params = {}


        activation_layer = {
            'sigmoid': Sigmoid,
            "bipolar": bipolar_sigmoid,
            'tanh': tanh,
            'relu': Relu
        }

        self.gain = weight_init_std
        self.__init_weights(self.gain)

        self.layers = OrderedDict()
        for idx in range(1, self.hidden_layer_num+1):
            self.layers['Affine' + str(idx)] = Affine(self.params['W' + str(idx)], self.params['b' + str(idx)])
            if self.use_batchnorm:
                self.params['gamma' + str(idx)] = np.ones(hidden_size_list[idx-1])
                self.params['beta' + str(idx)] = np.zeros(hidden_size_list[idx-1])
                self.layers['BatchNorm' + str(idx)] = BatchNormalization(self.params['gamma' + str(idx)], self.params['beta' + str(idx)])

            if len(activation) == 1:
                self.layers['Activation_function' + str(idx)] = activation_layer[activation[0]]()
            else:
                self.layers['Activation_function' + str(idx)] = activation_layer[activation[idx]]

        idx = self.hidden_layer_num + 1
        self.layers['Affine' + str(idx)] = Affine(self.params['W' + str(idx)], self.params['b' + str(idx)])

        self.last_layer = SoftmaxWithLoss()


    def __init_weights(self, gain=1.0):
        for idx in range(1, len(self.layer_list)):
            if self.gain == 'he':
                std = np.sqrt(2.0 / self.layer_list[idx-1])
            elif self.gain == 'xavier':
                std = np.sqrt(1.0 / self.layer_list[idx-1])
            self.params['W' + str(idx)] = std * np.random.rand(self.layer_list[idx-1], self.layer_list[idx])
            self.params['b' + str(idx)] = np.zeros(self.layer_list[idx])

    def predict(self, x, train_flg=False):
        for key, layer in self.layers.items():
            if "Dropout" in key or "BatchNorm" in key:
                x = layer.forward(x, train_flg)
            else:
                x = layer.forward(x)
        return x

    def loss(self, x, t, train_flg=False):
        y = self.predict(x, train_flg)

        weight_decay = 0
        for idx in range(1, self.hidden_layer_num + 2):
            W = self.params['W' + str(idx)]
            weight_decay += 0.5 * self.weight_decay_lambda * np.sum(W**2)

        return self.last_layer.forward(y, t) + weight_decay

    def accuracy(self, X, T):
        Y = self.predict(X, train_flg=False)
        Y = np.argmax(Y, axis=1)
        if T.ndim != 1 : T = np.argmax(T, axis=1)

        accuracy = np.sum(Y == T) / float(X.shape[0])
        return accuracy

    def numerical_gradient(self, X, T):
        loss_W = lambda W: self.loss(X, T, train_flg=True)

        grads = {}
        for idx in range(1, self.hidden_layer_num+2):
            grads['W' + str(idx)] = numerical_gradient(loss_W, self.params['W' + str(idx)])
            grads['b' + str(idx)] = numerical_gradient(loss_W, self.params['b' + str(idx)])

            if self.use_batchnorm and idx != self.hidden_layer_num+1:
                grads['gamma' + str(idx)] = numerical_gradient(loss_W, self.params['gamma' + str(idx)])
                grads['beta' + str(idx)] = numerical_gradient(loss_W, self.params['beta' + str(idx)])

        return grads

    def gradient(self, x, t):
        self.loss(x, t, train_flg=True)

        dout = 1
        dout = self.last_layer.backward(dout)

        layers = list(self.layers.values())
        layers.reverse()
        for layer in layers:
            dout = layer.backward(dout)

        grads = {}
        for idx in range(1, self.hidden_layer_num+2):
            grads['W' + str(idx)] = self.layers['Affine' + str(idx)].dW + self.weight_decay_lambda * self.params['W' + str(idx)]
            grads['b' + str(idx)] = self.layers['Affine' + str(idx)].db

            if self.use_batchnorm and idx != self.hidden_layer_num+1:
                grads['gamma' + str(idx)] = self.layers['BatchNorm' + str(idx)].dgamma
                grads['beta' + str(idx)] = self.layers['BatchNorm' + str(idx)].dbeta

        return grads
