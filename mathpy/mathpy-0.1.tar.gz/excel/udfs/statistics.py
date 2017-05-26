# encoding=utf8

"""

STATISTICS

"""


from mathpy.stats import sim_corr, variance

import numpy as np
import xlwings as xw


"""
Variance
"""


@xw.func
@xw.arg('x', np.array, doc='Matrix or vector input.')
@xw.ret(expand='table')
def VARIANCE(x):
    """
    Computes the variance of the given matrix (column-wise) or vector

    Parameters
    ----------
    x : Continuous range of cells representing the vector or matrix

    Returns
    -------
    array-like
        Range containing variances of matrix (column-wise) or vector

    See Also
    --------
    var : function
        Function used to compute variance
    Variance : class
        Backend class of the var function containing several different algorithmic
        implementations for computing variance

    """
    return variance.var(x)


"""
Simulating Correlation Matrices
"""


@xw.func
@xw.arg('k', doc='number of k groups to simulate')
@xw.arg('nk', np.array, doc='sample size of groups')
@xw.arg('rho', np.array, doc='standard deviation of group')
@xw.arg('m')
@xw.arg('power')
@xw.arg('method', doc='define structure of simulated correlation matrix. Options are "constant", "toeplitz", or '
                      '"hub". Default is "constant".')
@xw.ret(expand='table')
def SIMULATECORRMATRIX(k, nk, rho, m, power, method):
    """
    Simulates an n x n correlation matrix using a constant, Toeplitz, or hub matrix structure (default constant)

    """
    cor = sim_corr.simulate_corr_matrix(k=k, nk=nk, rho=rho, M=m, power=power, method=method)

    return cor
