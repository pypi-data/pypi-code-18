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

# what is imported by "from schwarzschild import *"
__all__ = ["Schwarzschild"]

import numpy as np
from .base import SphericalMetric

class Schwarzschild(SphericalMetric):
    """Schwarzschild black hole in spherical BL coordinates."""
    ID = 'S'        #: short identifier of this metric; used e.g. in file names
    CL_CODE = "Schwarzschild.cl"    #: OpenCL source file of this metric

    def __init__(self, RS):
        """Create new Schwarzschild blackhole.

        :param RS: The Schwarzschild radius of this black hole.
        """
        super(Schwarzschild, self).__init__()
        self.RS = RS
        self.EH = RS
        self.rCutoff = self.CUTOFF_FACTOR*self.EH

    def __str__(self):
        """Show human readable summary of the current setup.
        """
        res = 'Metric: Schwarzschild\n'
        res = res + 'Schwarzschild radius: {}\n'.format(self.RS)
        res = res + 'Event horizon:        {}\n'.format(self.EH)
        res = res + 'Cutoff radius:        {}\n'.format(self.rCutoff)
        res += super(Schwarzschild, self).__str__();
        return res

    def cl_allocate(self, context, device, commandQueue, real):
        """Add **CONST_RS** and **RCUTOFF** to the OpenCL compiler flags to pass these
        values to the OpenCL metric code.

        :param context: The PyOpenCL context of the OpenCL computation.
        :param device: The PyOpenCL device used for the OpenCL computation.
        :param commandQueue: The PyOpenCL command queue on the device.
        :param real: The type of "real" numbers (either ``np.float32`` or
            ``np.float64``).
        """
        super(Schwarzschild,self).cl_allocate(context, device, commandQueue, real)
        self.cl_flags += " -D CONST_RS={:.16e} -D RCUTOFF={:.16e}".format(self.EH, self.rCutoff)

    def update(self):
        """Compute the relevant components of the metric at the current point and store them in the attributes.

        :return: An error flag that is True if an error occured (most likely the ray fell into the black hole) or False otherwise.
        """
        # check if fallen in, this is returned later. We don't immediately return because this may be vectorized and called with many coordinates, some of which may fail some of which may not.
        result = self.x[1]<self.rCutoff
        rsr = self.RS/self.x[1]
        sinth = np.sin(self.x[2])

        # contravariant form
        self.tt = -1.0/(1.0-rsr)
        self.rr = (1.0-rsr)
        self.thth = 1.0/self.x[1]**2
        self.pp = 1.0/(self.x[1]*sinth)**2
        #self.tp = 0.0  # implicit

        # derivatives wrt r of the contravariant form
        self.dr_tt = rsr/((1.0-rsr)**2*self.x[1])
        self.dr_rr = rsr/self.x[1]
        self.dr_thth = -2.0/self.x[1]**3
        self.dr_pp = self.dr_thth/sinth**2
        #self.dr_tp = 0.0   # implicit

        # derivatives wrt theta of the contravariant form
        #self.dth_tt = 0.0  # implicit
        #self.dth_rr = 0.0  # implicit
        #self.dth_thth = 0.0    # implicit
        self.dth_pp = -2.0*np.cos(self.x[2])/(sinth**3*self.x[1]**2)
        #self.dth_tp = 0.0  # implicit

        return result
