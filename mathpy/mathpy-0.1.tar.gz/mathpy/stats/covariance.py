import numpy as np
import pandas as pd

from _lib import _create_array


class Covariance(object):

    def __init__(self, x):
        self.x, self.cols = _create_array(x)
        self.n = len(self.x)
        self.method = 'naive'
        self.xt = np.transpose(self.x)
        self.cov = np.empty([self.n, self.n])

    def naive(self):
        for i in range(self.n):
            for j in range(self.n):
                x = self.xt[:, i]
                y = self.xt[:, j]
                s2 = (np.sum(x * y) - ((np.sum(x)) * (np.sum(y))) / self.n) / (self.n - 1)
                self.cov[i, j] = s2

        return self.cov


def corr(x, method=None):
    x = _create_array(x)[0]
    n = x.shape[1]

    xt = np.transpose(x)

    cor = np.empty([n, n])

    for i in range(n):
        for j in range(n):
            x = xt[i]
            y = xt[j]

            xx = np.sum(np.power(x, 2))
            x2 = np.power(np.sum(x), 2)

            yy = np.sum(np.power(y, 2))
            y2 = np.power(np.sum(y), 2)

            xy = np.sum(x * y)
            sum_xy = np.sum(x) * np.sum(y)

            sxx = xx - x2 / n
            syy = yy - y2 / n
            sxy = xy - sum_xy / n

            cor[i, j] = sxy / np.sqrt(sxx * syy)

    cor = pd.DataFrame(cor)

    return cor