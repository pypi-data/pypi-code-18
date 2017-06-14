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

import logging
import numpy as np

import TransportMaps as TM

__all__ = ['Map',
           'LinearMap']

nax = np.newaxis

class Map(TM.TMO):
    r""" Abstract map :math:`T:\mathbb{R}^{d_x}\rightarrow\mathbb{R}^{d_y}`

    Args:
      dim_in (int): input dimension :math:`d_x`
      dim_out (int): output dimension :math:`d_y`
    """
    def __init__(self, dim_in, dim_out):
        super(Map, self).__init__()
        self.dim_in = dim_in
        self.dim_out = dim_out
        self.dim = None
        if self.dim_in == self.dim_out:
            self.dim = self.dim_in

    def __call__(self, x):
        r"""
        Calls :func:`evaluate`.
        """
        return self.evaluate( x )

    def evaluate(self, x, precomp=None, idxs_slice=slice(None)):
        r""" [Abstract] Evaluate the map :math:`T` at the points :math:`{\bf x} \in \mathbb{R}^{m \times d_x}`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d_x`]): evaluation points
          precomp (:class:`dict<dict>`): dictionary of precomputed values
          idxs_slice (slice): if precomputed values are present, this parameter
            indicates at which of the points to evaluate. The number of indices
            represented by ``idxs_slice`` must match ``x.shape[0]``.

        Returns:
           (:class:`ndarray<numpy.ndarray>` [:math:`m,d_y`]) -- transformed points

        Raises:
          NotImplementedError: to be implemented in sub-classes
        """
        raise NotImplementedError("To be implemented in sub-classes")

    def grad_x(self, x, precomp=None, idxs_slice=slice(None)):
        r""" [Abstract] Evaluate the gradient :math:`\nabla_{\bf x}T` at the points :math:`{\bf x} \in \mathbb{R}^{m \times d_x}`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d_x`]): evaluation points
          precomp (:class:`dict<dict>`): dictionary of precomputed values
          idxs_slice (slice): if precomputed values are present, this parameter
            indicates at which of the points to evaluate. The number of indices
            represented by ``idxs_slice`` must match ``x.shape[0]``.

        Returns:
           (:class:`ndarray<numpy.ndarray>` [:math:`m,d_y,d_y`]) -- transformed points

        Raises:
          NotImplementedError: to be implemented in sub-classes
        """
        raise NotImplementedError("To be implemented in sub-classes")

    def hess_x(self, x, precomp=None, idxs_slice=slice(None)):
        r""" [Abstract] Evaluate the Hessian :math:`\nabla^2_{\bf x}T` at the points :math:`{\bf x} \in \mathbb{R}^{m \times d_x}`.

        Args:
          x (:class:`ndarray<numpy.ndarray>` [:math:`m,d_x`]): evaluation points
          precomp (:class:`dict<dict>`): dictionary of precomputed values
          idxs_slice (slice): if precomputed values are present, this parameter
            indicates at which of the points to evaluate. The number of indices
            represented by ``idxs_slice`` must match ``x.shape[0]``.

        Returns:
           (:class:`ndarray<numpy.ndarray>` [:math:`m,d_y,d_y,d_y`]) -- transformed points

        Raises:
          NotImplementedError: to be implemented in sub-classes
        """
        raise NotImplementedError("To be implemented in sub-classes")

class LinearMap(Map):
    r""" Map :math:`T({\bf x}) = {\bf c} + {\bf T} {\bf x}`

    Args:
      c (:class:`ndarray<numpy.ndarray>` [:math:`d_y`]): constant part
      T (:class:`ndarray<numpy.ndarray>` [:math:`d_y,d_x`]): linear part (matrix)
    """
    def __init__(self, c, T):
        if c.shape[0] != T.shape[0]:
            raise ValueError("The dimensions of the constant and the " + \
                             "linear part must match")
        super(LinearMap, self).__init__(T.shape[1], T.shape[0])
        self.c = c
        self.T = T

    def evaluate(self, x, *args, **kwargs):
        return self.c + self.T.dot(x.T).T

    def grad_x(self, x, *args, **kwargs):
        return self.T[nax,:,:]

    def hess_x(self, x, *args, **kwargs):
        return np.zeros((1, self.dim_out, self.dim_in, self.dim_in))