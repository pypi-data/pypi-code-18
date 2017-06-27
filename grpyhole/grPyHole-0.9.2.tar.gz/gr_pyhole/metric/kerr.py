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

# what is imported by "from kerr import *"
__all__ = ["Kerr"]

import numpy as np
from .base import SphericalMetric

class Kerr(SphericalMetric):
    """Kerr black hole in spherical BL coordinates."""
    ID = 'K'    #: short identifier of this metric; used e.g. in file names. Modified in __init__!
    CL_CODE = "Kerr.cl"    #: OpenCL source file of this metric

    def __init__(self, RS, A):
        """Create new Kerr blackhole.

        :param RS: The Schwarzschild radius of this black hole.
        :param A: The alpha parameter.
        """
        super(Kerr,self).__init__()
        self.RS = RS
        self.A = A
        self.ID = 'K{:02}'.format(int(A*10))
        self.EH = 0.5*RS+np.sqrt(0.25*RS**2-A**2)
        self.rCutoff = self.CUTOFF_FACTOR*self.EH

    def __str__(self):
        """Show human readable summary of the current setup.
        """
        res = 'Metric: Kerr\n'
        res = res + 'Schwarzschild radius: {}\n'.format(self.RS)
        res = res + 'Alpha:                {}\n'.format(self.A)
        res = res + 'Event horizon:        {}\n'.format(self.EH)
        res = res + 'Cutoff radius:        {}\n\n'.format(self.rCutoff)
        res += super(Kerr,self).__str__();
        return res

    def cl_allocate(self, context, device, commandQueue, real):
        """Add **CONST_RS**, **CONST_A**, and **RCUTOFF** to the OpenCL compiler flags to pass these
        values to the OpenCL metric code.

        :param context: The PyOpenCL context of the OpenCL computation.
        :param device: The PyOpenCL device used for the OpenCL computation.
        :param commandQueue: The PyOpenCL command queue on the device.
        :param real: The type of "real" numbers (either ``np.float32`` or
            ``np.float64``).
        """
        super(Kerr,self).cl_allocate(context, device, commandQueue, real)
        self.cl_flags += " -D CONST_RS={:.16e} -D CONST_A={:.16e} -D RCUTOFF={:.16e}".format(self.RS, self.A, self.rCutoff)

    def update(self):
        """Compute the relevant components of the metric at the current point and store them in the attributes.

        :return: An error flag that is True if an error occured (most likely the ray fell into the black hole) or False otherwise.
        """
        r = self.x[1]
        # check if fallen in, this is returned later. We don't immediately return because this may be vectorized and called with many coordinates, some of which may fail some of which may not.
        result = r<self.rCutoff
        s = np.sin(self.x[2])
        c = np.cos(self.x[2])
        s2 = s**2
        c2 = c**2
        r2 = r**2
        rho2 = r2 + self.A**2*c2
        rho4 = rho2*rho2
        Delta = r2 - self.RS*r + self.A**2

        # contravariant form
        self.tt = -(r2 + self.A**2 + self.RS*r*self.A**2*s2/rho2 )/Delta
        self.rr = Delta/rho2
        self.thth = 1.0/rho2
        self.pp = (Delta-self.A**2*s2)/(rho2*Delta*s2)
        self.tp = -self.RS*r*self.A/(rho2*Delta)

        # derivatives wrt r of the contravariant form
        Delta_r = 2.0*r-self.RS
        rho2_r = 2.0*r
        rho2_th = -2.0*self.A**2*c*s
        self.dr_tt = -(self.tt*Delta_r+2.0*r+(rho2-rho2_r*r)*self.RS*self.A**2*s2/rho4)/Delta
        self.dr_rr = (Delta_r-rho2_r*self.rr)/rho2
        self.dr_thth = -rho2_r/rho4
        self.dr_pp = (Delta_r-self.pp*(rho2_r*Delta+rho2*Delta_r)*s2)/(rho2*Delta*s2)
        self.dr_tp = -(self.RS*self.A+self.tp*(rho2_r*Delta+rho2*Delta_r))/(rho2*Delta)

        # derivatives wrt theta of the contravariant form
        self.dth_tt = -self.RS*self.A*r*2.0*s*c*(r2+self.A**2)/(Delta*rho4)
        self.dth_rr = -Delta*rho2_th/rho4
        self.dth_thth = -rho2_th/rho4
        self.dth_pp = (-2.0*self.A**2*c - Delta*self.pp*(rho2_th*s+2.0*rho2*c))/(rho2*Delta*s)
        self.dth_tp = self.RS*r*self.A*rho2_th/(Delta*rho4)

        return result
