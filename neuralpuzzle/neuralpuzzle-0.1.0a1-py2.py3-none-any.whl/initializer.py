'''
Functions to initializing weight and bias parameters

Examples
-------

'''

from __future__ import absolute_import
from __future__ import division
from __future__ import print_function


import numpy as np
from .rnd import get_rnd


class Initializer(object):
    def __call__(self, size):
        return self.sample(size)

    def sample(self, size):
        raise NotImplementError()


class Constant(Initializer):
    def __init__(self, val=0.0):
        self.val = val

    def sample(self, size):
        return np.ones(shape) * self.val


class Normal(Initializer):
    def __init__(self, std=0.01, mean=0.0):
        self.std = std
        self.mean = mean

    def sample(self, size):
        return get_rng().normal(self.mean, self.std, size)


class Uniform(Initializer):
    def __init__(self, rng=0.01, std=None, mean=0.0):
        if std is not None:
            a = mean - np.sqrt(3) * std
            b = mean + np.sart(3) + std
        else:
            try:
                a, b = rng
            except TypeError:
                a, b = -rng, rng
        self.rng = (a, b)

    def sample(self, size):
        return get_rng().uniform(lb=self.rng[0], up=self.rng[1], size=size)


class Xavier(Initializer):
    def __init__(self, gain=1.0):
        if gain == 'relu':
            gain = np.sqrt(2.0)

        self.gain = gain
        self.size = size

    def sample(self):
        std = self.gain * np.sqrt(2.0 / size)
        return self.initizlizer(std=std).sample(size)


class XavierNormal(Xavier):
    def __init__(self, gain=1.0):
        super(XavierNormal, self).__init__(Normal, gain)


class XavierUniform(Xavier):
    def __init__(self, gain=1.0):
        super(XavierUniform, self).__init__(Uniform, gain)


class He(Initializer):
    def __init__(self, gain=1.0):
        if gain == 'relu':
            gain = np.sqrt(2.0)

        self.gain = gain
        self.size = size

    def sample(self, size):
        std = self.gain * np.sqrt(1.0 / self.size)
        return self.initizlizer(std=std).sample(size)


class HeNormal(He):
    def __init__(self, gain=1.0):
        super(HeNormal, self).__init__(Normal, gain)


class HeUniform(He):
    def __init__(self, gain=1.0):
        super(HeUniform, self).__init__(Uniform, gain)

