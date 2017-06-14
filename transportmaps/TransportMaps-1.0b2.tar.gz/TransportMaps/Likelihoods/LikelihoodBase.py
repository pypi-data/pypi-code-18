#
# This file is part of TransportMaps.
#
# TransportMaps is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# TransportMaps is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with TransportMaps.  If not, see <http://www.gnu.org/licenses/>.
#
# Transport Maps Library
# Copyright (C) 2015-2017 Massachusetts Institute of Technology
# Uncertainty Quantification group
# Department of Aeronautics and Astronautics
#
# Authors: Transport Map Team
# Website: transportmaps.mit.edu
# Support: transportmaps.mit.edu/qa/
#

import numpy as np

from TransportMaps.Functionals.FunctionBase import *
from TransportMaps.Maps.MapBase import LinearMap
from TransportMaps.Distributions.FrozenDistributions import GaussianDistribution

__all__ = ['LogLikelihood',
           'AdditiveLogLikelihood',
           'AdditiveLinearGaussianLogLikelihood',
           'IndependentLogLikelihood']

class LogLikelihood(Function):
    r""" Abstract class for log-likelihood :math:`\log \pi({\bf y} \vert {\bf x})`

    Note that :math:`\log\pi:\mathbb{R}^d \rightarrow \mathbb{R}`
    is considered a function of :math:`{\bf x}`, while the
    data :math:`{\bf y}` is fixed.
    
    Args:
      y (:class:`ndarray<numpy.ndarray>`): data
      dim (int): input dimension $d$
    """
    def __init__(self, y, dim):
        super(LogLikelihood, self).__init__(dim)
        self.y = y

    def evaluate(self, x, *args, **kwargs):
        r""" [Abstract] Evaluate :math:`\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m`]) -- function evaluations
        """
        raise NotImplementedError("To be implemented in sub-classes")

    def grad_x(self, x, *args, **kwargs):
        r""" [Abstract] Evaluate :math:`\nabla_{\bf x}\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]) -- gradient evaluations
        """
        raise NotImplementedError("To be implemented in sub-classes")

    def hess_x(self, x, *args, **kwargs):
        r""" [Abstract] Evaluate :math:`\nabla^2_{\bf x}\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]) -- Hessian evaluations
        """
        raise NotImplementedError("To be implemented in sub-classes")

class AdditiveLogLikelihood(LogLikelihood):
    r""" Log-likelihood :math:`\log \pi({\bf y} \vert {\bf x})=\log\pi({\bf y} - T({\bf x}))`

    Args:
      y (:class:`ndarray<numpy.ndarray>` :math:`[d_y]`): data
      pi (:class:`Distribution<TransportMaps.Distributions.Distribution>`):
        distribution :math:`\nu_\pi`
      T (:class:`Map<TransportMaps.Maps.Map>`): map :math:`T:\mathbb{R}^d\rightarrow\mathbb{R}^{d_y}`
    """
    def __init__(self, y, pi, T):
        if len(y) != pi.dim:
            raise ValueError("The dimension of the data must match the " + \
                             "dimension of the distribution pi")
        if len(y) != T.dim_out:
            raise ValueError("The dimension of the data must match the " + \
                             "dimension of the output of T")
        super(AdditiveLogLikelihood, self).__init__(y, T.dim_in)
        self.pi = pi
        self.T = T

    def evaluate(self, x, *args, **kwargs):
        r""" Evaluate :math:`\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m`]) -- function evaluations

        .. todo:: caching is not implemented
        """
        frw = self.T.evaluate(x, *args, **kwargs)
        return self.pi.log_pdf( self.y - frw )

    def grad_x(self, x, *args, **kwargs):
        r""" Evaluate :math:`\nabla_{\bf x}\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]) -- gradient evaluations

        .. todo:: caching is not implemented
        """
        frw = self.T.evaluate(x, *args, **kwargs)
        gx_frw = self.T.grad_x(x, *args, **kwargs)
        gx_lpdf = self.pi.grad_x_log_pdf( self.y - frw )
        out = - np.einsum('...i,...ij->...j',gx_lpdf, gx_frw)
        return out

    def hess_x(self, x, *args, **kwargs):
        r""" Evaluate :math:`\nabla^2_{\bf x}\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,d,d`]) -- Hessian evaluations

        .. todo:: caching is not implemented
        """
        frw = self.T.evaluate(x, *args, **kwargs) # m x d_y
        gx_frw = self.T.grad_x(x, *args, **kwargs) # m x d_y x d_x
        hx_frw = self.T.hess_x(x, *args, **kwargs) # m x d_y x d_x x d_x
        gx_lpdf = self.pi.grad_x_log_pdf( self.y - frw ) # m x d_y
        hx_lpdf = self.pi.hess_x_log_pdf( self.y - frw ) # m x d_y x d_y
        out = np.einsum('...ij,...ik->...jk', hx_lpdf, gx_frw) # m x d_y x d_x
        out = np.einsum('...ij,...ik->...jk', out, gx_frw) # m x d_x x d_x
        out -= np.einsum('...i,...ijk->...jk', gx_lpdf, hx_frw) # m x d_x x d_x
        return out

class AdditiveLinearGaussianLogLikelihood(AdditiveLogLikelihood):
    r""" Define the log-likelihood for the additive linear Gaussian model

    The model is

    .. math::

       {\bf y} = {\bf c} + {\bf T}{\bf x} + \varepsilon \;, \quad
       \varepsilon \sim \mathcal{N}(\mu, \Sigma)

    where :math:`T \in \mathbb{R}^{d_y \times d_x}`, :math:`\mu \in \mathbb{R}^{d_y}`
    and :math:`\Sigma \in \mathbb{R}^{d_y \times d_y}` is symmetric positve
    definite

    Args:
      y (:class:`ndarray<numpy.ndarray>` [:math:`d_y`]): data
      c (:class:`ndarray<numpy.ndarray>` [:math:`d_y`]): system constant
      T (:class:`ndarray<numpy.ndarray>` [:math:`d_y,d_x`]): system matrix
      mu (:class:`ndarray<numpy.ndarray>` [:math:`d_y`]): noise mean
      sigma (:class:`ndarray<numpy.ndarray>` [:math:`d_y,d_y`]):
        noise covariance
    """
    def __init__(self, y, c, T, mu, sigma):
        pi = GaussianDistribution(mu, sigma)
        linmap = LinearMap(c, T)
        super(AdditiveLinearGaussianLogLikelihood, self).__init__(y, pi, linmap)
        
class IndependentLogLikelihood(Function):
    r""" Handling likelihoods in the form :math:`\pi({\bf y}\vert{\bf x}) = \prod_{i=1}^{n}\pi_i({\bf y}_i\vert{\bf x}_i)`

    Args:
      factors (:class:`list` of :class:`tuple`): each tuple contains a
        log-likelihood (:class:`LogLikelihood`) and the sub-set of variables
        of :math:`{\bf x}` on which it acts.

    Example
    -------
    Let :math:`\pi(y_0,y_2\vert x_0,x_1,x_2)= \pi_0(y_0\vert x_0) \pi_2(y_2,x_2)`.

    >>> factors = [(ll0, [0]),
    >>>            (ll2, [2])]
    >>> ll = IndependentLogLikelihood(factors)
    
    """
    def __init__(self, factors):
        self.factors = []
        self.input_dim = set()
        for i, (ll, xidxs) in enumerate(factors):
            # Check right number of inputs
            if ll is not None and len(set(list(xidxs))) != ll.dim:
                raise TypeError("The dimension of the %d " % i + \
                                "log-likelihood is not consistent with " + \
                                "the number of variables.")
            self.factors.append( (ll, xidxs) )
            self.input_dim |= set(xidxs)
        dim = 0 if len(self.input_dim) == 0 else max(self.input_dim)+1
        super(IndependentLogLikelihood, self).__init__(dim)

    def append(self, factor):
        r""" Add a new factor to the likelihood

        Args:
          factors (:class:`tuple`): tuple containing a
            log-likelihood (:class:`LogLikelihood`) and the sub-set of variables
            of :math:`{\bf x}` on which it acts.

        Example
        -------
        Let :math:`\pi(y_0,y_2\vert x_0,x_1,x_2)= \pi_0(y_0\vert x_0) \pi_2(y_2,x_2)` and
        let's add the factor :math:`\pi_1(y_1\vert x_1)`, obtaining:

        .. math::

           \pi(y_0,y_1,y_2\vert x_0,x_1,x_2)= \pi_0(y_0\vert x_0) \pi_1(y_1\vert x_1) \pi_2(y_2,x_2)

        >>> factor = (ll1, [1])
        >>> ll.append(factor)
        
        """
        ll, xidxs = factor
        if ll is not None and len(set(xidxs)) != ll.dim:
            raise TypeError("The dimension of the " + \
                            "log-likelihood is not consistent with " + \
                            "the number of variables.")
        self.factors.append( (ll, xidxs) )
        self.input_dim |= set(xidxs)
        self.dim = max(self.input_dim)+1

    def evaluate(self, x, *args, **kwargs):
        r""" Evaluate :math:`\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m`]) -- function evaluations
        """
        if x.shape[1] != self.dim:
            raise ValueError("The dimension of the input does not match the dimension " + \
                             "of the log-likelihood")
        out = np.zeros(x.shape[0])
        for ll, xidxs in self.factors:
            if ll is not None:
                out += ll.evaluate(x[:,xidxs], *args, **kwargs)
        return out

    def grad_x(self, x, *args, **kwargs):
        r""" Evaluate :math:`\nabla_{\bf x}\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]) -- gradient evaluations
        """
        if x.shape[1] != self.dim:
            raise ValueError("The dimension of the input does not match the dimension " + \
                             "of the log-likelihood")
        out = np.zeros(x.shape)
        for ll, xidxs in self.factors:
            if ll is not None:
                out[:,xidxs] += ll.grad_x(x[:,xidxs], *args, **kwargs)
        return out

    def hess_x(self, x, *args, **kwargs):
        r""" Evaluate :math:`\nabla^2_{\bf x}\log\pi({\bf y} \vert {\bf x})`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]): evaluation points

        Returns:
          (:class:`ndarray<numpy.ndarray>` [:math:`m,d`]) -- Hessian evaluations
        """
        if x.shape[1] != self.dim:
            raise ValueError("The dimension of the input does not match the dimension " + \
                             "of the log-likelihood")
        m = x.shape[0]
        out = np.zeros( (m, self.dim, self.dim) )
        for ll, xidxs in self.factors:
            if ll is not None:
                out[np.ix_(range(m),xidxs,xidxs)] += \
                    ll.hess_x(x[:,xidxs], *args, **kwargs)
        return out