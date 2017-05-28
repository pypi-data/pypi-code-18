from collections import OrderedDict
from .layers import *
import numpy as np
import pickle


class DeepConvNet(object):
    def __init__(self, **kwargs):
        self.kwargs = kwargs
        self.input_dim = self.kwargs["input_dim"]
        self.layer_list = self.kwargs["layer_list"]
        self.hidden_list_size = len(self.layer_list[1:-1])
        self.pre_list = self.layer_list[:-1]
        self.activation = self.kwargs["activation"]
        self.filer_size = self.kwargs["filer_size"]
        self.padding = self.kwargs["padding"]
        self.stride = self.kwargs["stride"]
        self.output_size = self.layer_list[-1]
        self.params = {}

        self.__init_weights()

        self.layers = OrderedDict()
        for idx in range(1, len(self.layer_list)):
            if idx < range(1, len(self.layer_list))[-2]:
                self.layers['Convolution' + str[idx]] = Convolution(self.params['W' + str(idx)], self.params['b' + str[idx]], self.stride, self.padding)
                self.layers['Activation_function' + str(idx)] = activation_layer[activation[0]]()
                self.layers['Pooling' + str[idx]] = Pooling(pool_h=2, pool_w=2, stride=2)
            elif idx == 7:
                self.layers['Affine' + str(idx)] = Affine(self.params[idx], self.params[idex])
                self.layers['Activation_function' + str(idx)] = activation_layer[activation[0]]()
                self.layers['Dropout' + str(idx)] = Dropout(0.5)
            else:
                self.layers['Affine' + str(idx)] = Affine(self.params[idx], self.params[idex])
                self.layers['Dropout' + str(idx)] = Dropout(0.5)

        self.last_layer = SoftmaxWithLoss()

    def __init_weights(self):
        for idx in range(1, len(self.layer_list)):
            std = np.sqrt(2.0 / self.layer_list[idx-1])
            if idx < range(1, len(self.layer_list))[-2]:
                self.params['W'+str(idx)] = std * np.random.rand(self.layer_list[idx], self.layer_list[idx-1], self.filter_size, self.filter_size)
                self.params['b'+str(idx)] = np.zeros(self.layer_list[idx])
            else:
                self.params['W'+str(idx)] = std * np.random.rand(self.layer_list[idx], self.layer_list[idx+1])
                self.params['b'+str(idx)] = np.zeros(self.layer_list[idx+1])

    def predict(self, x, train_flg=False):
        for key, layer in self.layers.items():
            if "Dropout" in key:
                x = layer.forward(x, train_flg)
            else:
                x = layer.forward(x)
        return x

    def loss(self, x, t):
        y = self.predict(x, train_flg=True)
        return self.last_layer.forward(y, t)

    def accuracy(self, x, t, batch_size=100):
        if t.ndim != 1 : t = np.argmax(t, axis=1)

        acc = 0.0

        for i in range(int(x.shape[0] / batch_size)):
            tx = x[i*batch_size:(i+1)*batch_size]
            tt = t[i*batch_size:(i+1)*batch_size]
            y = self.predict(tx, train_flg=False)
            y = np.argmax(y, axis=1)
            acc += np.sum(y == tt)

        return acc / x.shape[0]

    def gradient(self, x, t):
        self.loss(x, t)

        dout = 1
        dout = self.last_layer.backward(dout)

        tmp_layers = self.layers.copy()
        tmp_layers.reverse()
        for layer in tmp_layers:
            dout = layer.backward(dout)

        grads = {}
        for idx in range(1, len(self.layer_list[-1])):
            grads['W' + str(idx)] = self.layers['Convolution' + str[idx]].dW
            grads['b' + str(idx)] = self.layers['Convolution' + str[idx]].db

        return grads

    def save_params(self, file_name="params.pkl"):
        params = {}
        for key, val in self.params.items():
            params[key] = val
        with open(file_name, 'wb') as f:
            pickle.dump(params, f)

    def load_params(self, file_name="params.pkl"):
        with open(file_name, 'rb') as f:
            params = pickle.load(f)
        for key, val in params.items():
            self.params[key] = val

        for idx in range(1, len(self.layer_list[-1])):
            self.layers['Convolution' + str[idx]].dW = self.params['W'+ str(idx)]
            self.layers['Convolution' + str[idx]].db = self.params['b'+ str(idx)]

