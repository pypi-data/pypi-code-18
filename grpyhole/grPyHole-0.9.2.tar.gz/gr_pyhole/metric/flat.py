# -*- coding: utf-8 -*-

#   Copyright 2015 - 2017 Alexander Wittig, Jai Grover
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.

# what is imported by "from flat import *"
__all__ = ["Flat", "CFlat"]

import numpy as np
from .base import SphericalMetric, CartesianMetric

class Flat(SphericalMetric):
    """Flat metric in spherical coordinates."""
    ID = 'F'        #: short identifier of this metric; used e.g. in file names.
    CL_CODE = "Flat.cl"                     #: Our OpenCL source file

    def __init__(self):
        super(Flat, self).__init__();

    def __str__(self):
        """Show human readable summary of the current setup.
        """
        res = 'Metric: Flat\n\n'
        res += super(Flat, self).__str__();
        return res

    def update(self):
        """Compute the relevant components of the metric at the current point and store them in the attributes.

        :return: An error flag that is True if an error occured (most likely the ray fell into the black hole) or False otherwise.
        """
        s = np.sin(self.x[2])
        c = np.cos(self.x[2])

        # contravariant form
        self.tt = -1.0
        self.rr = 1.0
        self.thth = 1.0/self.x[1]**2
        self.pp = 1.0/(self.x[1]*s)**2
        #self.tp = 0.0  # implicit

        # derivatives wrt r of the contravariant form
        #self.dr_tt = 0.0   # implicit
        #self.dr_rr = 0.0   # implicit
        self.dr_thth = -2.0/self.x[1]**3
        self.dr_pp = -2.0/(self.x[1]**3*s**2)
        #self.dr_tp = 0.0   # implicit

        # derivatives wrt theta of the contravariant form
        #self.dth_tt = 0.0   # implicit
        #self.dth_rr = 0.0   # implicit
        #self.dth_thth = 0.0 # implicit
        self.dth_pp = -2.0*c/(self.x[1]**2*s**3)
        #self.dth_tp = 0.0   # implicit

        if isinstance(self.x[0], np.ndarray):
            return np.full(self.x[0].shape, False, dtype=bool)
        else:
            return False


class CFlat(CartesianMetric):
    """Flat metric in cartesian coordinates."""
    ID = 'CF'        #: short identifier of this metric; used e.g. in file names.
    CL_CODE = "CFlat.cl"                     #: Our OpenCL source file

    def __init__(self):
        super(CFlat, self).__init__();

    def __str__(self):
        """Show human readable summary of the current setup.
        """
        res = 'Metric: Flat\n\n'
        res += super(CFlat, self).__str__();
        return res

    def update(self):
        """Compute the relevant components of the metric at the current point and store them in the attributes.

        :return: An error flag that is True if an error occured (most likely the ray fell into the black hole) or False otherwise.
        """
        # contravariant form
        self.tt = -1.0
#        self.tx = 0.0  # implicit
#        self.ty = 0.0  # implicit
        self.xx = 1.0
        self.yy = 1.0
        self.zz = 1.0
#        self.xy = 0.0  # implicit
#        self.xz = 0.0  # implicit
#        self.yz = 0.0  # implicit

#        self.dx_tt = 0.0   # implicit
#        self.dx_tx = 0.0   # implicit
#        self.dx_ty = 0.0   # implicit
#        self.dx_xx = 0.0   # implicit
#        self.dx_yy = 0.0   # implicit
#        self.dx_zz = 0.0   # implicit
#        self.dx_xy = 0.0   # implicit
#        self.dx_xz = 0.0   # implicit
#        self.dx_yz = 0.0   # implicit

#        self.dy_tt = 0.0   # implicit
#        self.dy_tx = 0.0   # implicit
#        self.dy_ty = 0.0   # implicit
#        self.dy_xx = 0.0   # implicit
#        self.dy_yy = 0.0   # implicit
#        self.dy_zz = 0.0   # implicit
#        self.dy_xy = 0.0   # implicit
#        self.dy_xz = 0.0   # implicit
#        self.dy_yz = 0.0   # implicit

#        self.dz_tt = 0.0   # implicit
#        self.dz_tx = 0.0   # implicit
#        self.dz_ty = 0.0   # implicit
#        self.dz_xx = 0.0   # implicit
#        self.dz_yy = 0.0   # implicit
#        self.dz_zz = 0.0   # implicit
#        self.dz_xy = 0.0   # implicit
#        self.dz_xz = 0.0   # implicit
#        self.dz_yz = 0.0   # implicit

        if isinstance(self.x[0], np.ndarray):
            # make sure the result is a vector of bools, not a single one
            return np.full(self.x[0].shape, False, dtype=bool)
        else:
            return False
