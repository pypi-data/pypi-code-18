from __future__ import division
from __future__ import print_function

import warnings

import numpy as np


def learn(X, H, W, nu_param, lambda_param=0., H_init=None):
    N = X.shape[0]
    D = X.shape[1]
    K = W.shape[1]
    if W.shape[0] != N:
        raise ValueError("W's row dimension does not match with X's rows")
    if H.shape[0] != K or H.shape[1] != D:
        raise ValueError("H's dimensions don't match for given X and W")
    if lambda_param < 0:
        raise ValueError("Lambda parameter can't be negative")
    use_hinit = False
    if lambda_param == 0. and H_init is not None:
        warnings.warn("Warning: H_init won't be in effect as lambda parameter is set to 0")
    elif lambda_param > 0 and H_init is None:
        warnings.warn("Warning: Lamda parameter won't be in effect as H_init is None")
    elif lambda_param > 0 and H_init is not None:
        use_hinit = True
        assert (H_init.shape == H.shape), "H_init must have same dimenstions as H"

    G = (W.T).dot(W)

    for k in range(K):
        hk = np.zeros(D)
        g = np.copy(G[:, k]).reshape((-1, 1))
        g[k][0] = 0.
        vk = W[:, k].reshape((-1, 1))
        numerator = ((X.T).dot(vk) - (H.T).dot(g))
        denominator = G[k, k]
        if use_hinit:
            init_term = (H_init[k, :].reshape((-1, 1)))*lambda_param
            assert (init_term.shape == numerator.shape), "Init term and numerator shape do not agree"
            numerator = numerator/N + init_term
            denominator = denominator/N + lambda_param
        epsilon = 0.00001
        qk = numerator/(denominator+epsilon)
        assert (qk.shape == (D, 1))
        qk = qk.reshape((-1,))
        Iset = np.argsort(qk)[::-1]
        Istarset = set()
        for I in Iset[0:nu_param]:
            if qk[I] > 0:
                Istarset.add(I)
            else:
                break
        for Istar in Istarset:
            hk[Istar] = qk[Istar]/np.linalg.norm(qk, ord=2)
        H[k, :] = hk
    return H
