# encoding=utf8


"""
Module containing functions related to computing variance and covariance
matrices with several different algorithm implementations.

"""


import numpy as np
import pandas as pd

from mathpy._lib import _create_array
from mathpy.linalgebra.norm import norm


def var(x, method=None):
    r"""
    Front-end interface function for computing the variance of a sample
    or population.

    Parameters
    ----------
    x : array_like
        Accepts a numpy array, nested list, dictionary, or
        pandas DataFrame. The private function _create_array
        is called to create a copy of x as a numpy array.

    Returns
    -------
    v : float or numpy array or numpy structured array or pandas DataFrame
        If the input is one-dimensional, the variance is returned as
        a float. For a two-dimensional input, the variance is calculated
        column-wise and returned as a numpy array or pandas DataFrame.

    Examples
    --------
    >>> f = pd.DataFrame({0: [1,-1,2,2], 1: [-1,2,1,-1], 2: [2,1,3,2], 3: [2,-1,2,1]})
    >>> var(f)
    np.array([2, 2.25, 0.666667, 2])
    >>> var(f[1])
    np.array([2])

    """
    x = Variance(x)
    if method is None:
        v = getattr(x, x.method, None)
    else:
        if hasattr(x, method):
            v = getattr(x, method, x.method)
        else:
            return 'no method with name ' + str(method)

    return v()


class Variance(object):
    r"""
    Class containing various algorithm method implementations for computing the
    variance of a sample. Please see the individual methods for more details on
    the specific algorithms.

    Parameters
    ----------
    x : array_like
        Accepts a list, nested list, dictionary, pandas DataFrame or
        pandas Series. The private function _create_array is called
        to create a copy of x as a numpy array.

    Attributes
    ----------
    type : string
        Class type of object that initializes the class.
    dim : int
        The dimension of the array
    method : string
        The default method for calculating the variance.
    n : int
        Number of rows of the array

    Methods
    -------
    textbook_one_pass()
        So-called due the equation's prevalence in statistical textbooks (Chan, Golub, & Leveque, 1983).
    standard_two_pass()
        Known as two-pass as it passes through the data twice, once to compute the mean and
        again to compute the variance :math:`S`.
    corrected_two_pass()
        An alternative form of the standard two pass algorithm suggested by Professor Å. Björck.

    """
    def __init__(self, x):
        self.type = x.__class__.__name__
        self.x, self.cols = _create_array(x)
        self.n = self.x.shape[0]
        self.dim = self.x.ndim
        self.method = 'corrected_two_pass'

    def corrected_two_pass(self):
        r"""
        Computes variance using the corrected two pass algorithm as suggested by
        Professor Å. Björck in (Chan, Golub, & Leveque, 1983). The corrected two pass
        approach is generally more stable numerically compared to other methods and is
        the default algorithm used in the var function.

        Returns
        -------
        varr : numpy ndarray
            Depending on the dimension of the input, returns a 1D or 2D array of the
            column-wise computed variances.

        Notes
        -----
        The corrected two pass algorithm takes advantage of increased gains in accuracy by
        shifting all the data by the computed mean before computing :math:`S`. Even primitive
        approximations of :math:`\bar{x}` can yield large improvements in accuracy. The
        corrected two pass algorithm is defined as:

        .. math::

            S = \sum^N_{i=1} (x_i - \bar{x})^2 - \frac{1}{N} \left( \sum^N_{i=1} (x_i - \bar{x}) \right)^2

        The first term is the standard two pass algorithm while the second acts as an approximation
        to the error term of the first term that avoids the problem of catastrophic cancellation.

        References
        ----------
        Chan, T., Golub, G., & Leveque, R. (1983). Algorithms for Computing the Sample Variance:
            Analysis and Recommendations. The American Statistician, 37(3), 242-247.
            http://dx.doi.org/10.1080/00031305.1983.10483115

        """
        if self.dim == 1:
            varr = np.array((np.sum(np.power(self.x - np.mean(self.x), 2)) - (1 / self.n) *
                             np.power(np.sum(self.x - np.mean(self.x)), 2)) / float(self.n - 1))
        elif self.dim == 2:
            varr = np.empty(self.x.shape[1])
            j = 0
            for i in self.x.T:
                v = (np.sum(np.power(i - np.mean(i), 2)) - (1 / self.n) *
                     np.power(np.sum(i - np.mean(i)), 2)) / float(self.n - 1)
                varr[j] = v
                j += 1
            if self.type is 'DataFrame':
                varr = pd.DataFrame(varr, index=self.cols)
        else:
            raise ValueError('array must be 1D or 2D')

        return varr

    def textbook_one_pass(self):
        r"""
        Textbook one-pass algorithm for calculating variance as defined in
        (Chan, Golub, & Leveque, 1983). Currently defined for 1D and 2D arrays.

        Returns
        -------
        varr : numpy ndarray
            Depending on the dimension of the input, returns a 1D or 2D array of the
            column-wise computed variances.

        Notes
        -----
        The textbook one pass algorithm for calculating variance is so named due to its
        prevalence in statistical textbooks and it passes through the data once
        (hence 'one-pass').

        The textbook one pass algorithm is defined as:

        .. math::

            S = \sum^N_{i=1} x_i^2 - \frac{1}{N}\left( \sum^N_{i=1} x_i \right)^2

        References
        ----------
        Chan, T., Golub, G., & Leveque, R. (1983). Algorithms for Computing the Sample Variance:
            Analysis and Recommendations. The American Statistician, 37(3), 242-247.
            http://dx.doi.org/10.1080/00031305.1983.10483115

        """
        if self.dim == 1:
            varr = np.array(float(np.sum(np.power(self.x, 2.)) - (1. / self.n) *
                                  np.power(np.sum(self.x), 2.)) / float(self.n - 1))
        elif self.dim == 2:
            varr = np.empty(self.x.shape[1])
            j = 0
            for i in self.x.T:
                v = float(np.sum(np.power(i, 2.)) - (1. / self.n) * np.power(np.sum(i), 2.)) / float(self.n - 1)
                varr[j] = v
                j += 1
            if self.type is 'DataFrame':
                varr = pd.DataFrame(varr, index=self.cols)
        else:
            raise ValueError('array must be 1D or 2D')

        return varr

    def standard_two_pass(self):
        r"""
        Standard two-pass algorithm defined in (Chan, Golub, & Leveque, 1983) for
        computing variance of a 1D or 2D array.

        Returns
        -------
        varr : numpy ndarray
            Depending on the dimension of the input, returns a 1D or 2D array of the
            column-wise computed variances.

        Notes
        -----
        The standard two pass algorithm for computing variance as defined in
        (Chan, Golub, & Leveque, 1983) is so named due to the algorithm passing
        through the data twice, once to compute the mean :math:`\bar{x}` and again
        for the variance :math:`S`. The standard two pass algorithm is defined as:

        .. math::

            S = \sum^N_{i=1} (x_i - \bar{x})^2 \qquad \bar{x} = \frac{1}{N} \sum^N_{i=1} x_i

        Due to the algorithm's two pass nature, it may not be the most optimal approach
        when the data is too large to store in memory or dynamically as data is collected.
        The algorithm is mathematically equivalent to the textbook one-pass algorithm.

        References
        ----------
        Chan, T., Golub, G., & Leveque, R. (1983). Algorithms for Computing the Sample Variance:
            Analysis and Recommendations. The American Statistician, 37(3), 242-247.
            http://dx.doi.org/10.1080/00031305.1983.10483115

        """
        if self.dim == 1:
            varr = np.array(np.sum(np.power(self.x - np.mean(self.x), 2)) / float(self.n - 1))
        elif self.dim == 2:
            varr = np.empty(self.x.shape[1])
            j = 0
            for i in self.x.T:
                v = np.sum(np.power(i - np.mean(i), 2)) / float(self.n - 1)
                varr[j] = v
                j += 1
            if self.type is 'DataFrame':
                varr = pd.DataFrame(varr, index=self.cols)
        else:
            raise ValueError('array must be 1D or 2D')

        return varr

    def youngs_cramer(self):
        r"""
        Implementation of the Youngs-Cramer updating algorithm for computing the variance
        :math:`S` as presented in (Chan, Golub, & LeVeque, 1982).

        Returns
        -------
        varr : numpy ndarray
            Depending on the dimension of the input, returns a 1D or 2D array of the
            column-wise computed variances.

        Notes
        -----
        Updating algorithms for computing variance have been proposed by numerous authors as
        they are robust to catastrophic cancellation and don't require several passes through
        the data, hence reducing the amount of memory required. The Youngs and Cramer updating
        algorithm is generally as performant as the two-pass algorithm. The algorithm proposed by
        Youngs and Cramer follows from their investigation of the most performant updating
        algorithms for computing variance and is as follows:

        .. math::

            t_j = t_{j-1} + x_j
            S_n = S_{n-1} + \frac{1}{n(n - 1)} (nx_j - t_j)^2

        References
        ----------
        Chan, T., Golub, G., & Leveque, R. (1983). Algorithms for Computing the Sample Variance:
            Analysis and Recommendations. The American Statistician, 37(3), 242-247.
            http://dx.doi.org/10.1080/00031305.1983.10483115

        Chan, T., Golub, G., & LeVeque, R. (1982). Updating Formulae and a Pairwise Algorithm for
            Computing Sample Variances. COMPSTAT 1982 5Th Symposium Held At Toulouse 1982, 30-41.
            http://dx.doi.org/10.1007/978-3-642-51461-6_3

        """
        if self.dim == 1:
            s = 0
            n = 1
            t = self.x[0]

            for j in np.arange(1, self.n):
                n += 1
                t = t + self.x[j]
                s = s + (1 / float((n * (n - 1))) * np.power(n * self.x[j] - t, 2))

            varr = np.array(s / float(self.n - 1))

        elif self.dim == 2:
            varr = np.empty(self.x.shape[1])
            k = 0

            for i in self.x.T:
                s = 0
                n = 1
                t = i[0]

                for j in np.arange(1, self.n):
                    n += 1
                    t = t + i[j]
                    s = s + (1 / float((n * (n - 1)))) * np.power(n * i[j] - t, 2)

                s = s / float(self.n - 1)
                varr[k] = s
                k += 1

        else:
            raise ValueError('array must be 1D or 2D')

        return varr

    # def pairwise(self):
    #     s = 0
    #     t = self.x[0]
    #
    #     for m in np.arange(1, self.n):
    #         t = t + self.x[m]


def std_dev(x):
    r"""
    Calculates the standard deviation by simply taking the square
    root of the variance.

    Parameters
    ----------
    x : array_like
        Accepts a numpy array, nested list, dictionary, or
        pandas DataFrame. The private function _create_array
        is called to create a copy of x as a numpy array.

    Returns
    -------
    sd : numpy array or float
        The computed standard deviation.

    """
    v = var(x)
    sd = np.sqrt(v)

    return sd


def var_cond(x):
    r"""
    Calculates the condition number, denoted as :math:`\kappa` which
    measures the sensitivity of the variance :math:`S` of a sample
    vector :math:`x` as defined by Chan and Lewis (as cited in Chan,
    Golub, & Leveque, 1983). Given a machine accuracy value of
    :math:`u`, the value :math:`\kappa u` can be used as a measure to
    judge the accuracy of the different variance computation algorithms.

    Parameters
    ----------
    x : array_like
        Accepts a numpy array, nested list, dictionary, or
        pandas DataFrame. The private function _create_array
        is called to create a copy of x as a numpy array.

    Returns
    -------
    varr : numpy ndarray
        Depending on the dimension of the input, returns a 1D or 2D array of the
        column-wise computed variances.

    Notes
    -----
    The 2-norm is defined as usual:

    .. math::

        ||x||_2 = \sum^N_{i=1} x^2_i

    Then the condition number :math:`\kappa` is defined as:

    .. math::

        \kappa = \frac{||x||_2}{\sqrt{S}} = \sqrt{1 + \bar{x}^2 N / S}

    References
    ----------
    Chan, T., Golub, G., & Leveque, R. (1983). Algorithms for Computing the Sample Variance:
        Analysis and Recommendations. The American Statistician, 37(3), 242-247.
        http://dx.doi.org/10.1080/00031305.1983.10483115

    """
    x = _create_array(x)[0]
    if x.ndim == 1:
        kap_cond = norm(x) / np.sqrt(var(x))
    elif x.ndim == 2:
        kap_cond = np.empty(x.shape[1])
        j = 0
        for i in x.T:
            k = norm(i) / np.sqrt(var(i))
            kap_cond[j] = k
            j += 1

    else:
        raise ValueError('array must be 1D or 2D')

    return kap_cond
