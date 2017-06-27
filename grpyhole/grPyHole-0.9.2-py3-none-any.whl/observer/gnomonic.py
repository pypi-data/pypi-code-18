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

# what is imported by "from gnomonic import *"
__all__ = ["Gnomonic"]

from .stereographic import Stereographic
from math import tan
import numpy as np

class Gnomonic(Stereographic):
    """Class for taking a picture of the black hole with Gnomonic projection."""

    PROJECTION = 'G'                                        #: Identifier of the projection used

    def __str__(self):
        """Show human readable summary of the current setup.
        """
        res = 'Projection: Gnomonic (GnomonicObserver)\n'
        res = res + 'Field of view (deg): {}\n'.format(np.rad2deg(self.fov))
        res = res + 'Observer position [t,r,theta,phi]: [{},{},{},{}]\n'.format(self.t, self.r, np.rad2deg(self.theta), np.rad2deg(self.phi))
        res = res + super(Stereographic,self).__str__();    # note how we skip our direct parent to avoid garbled output!
        return res

    def project(self, alpha, beta):
        """Project a given viewing direction (alpha,beta) onto a point (x,y) in the image plane.

        :param alpha,beta: the viewing angle.
        """
        return (np.tan(alpha)*np.cos(beta)/tan(self.fov), -np.tan(alpha)*np.sin(beta)/tan(self.fov))

    def unproject(self, x, y):
        """Unproject a given point (x,y) in the image plane to an initial position
        and viewing angle (t,r,theta,phi,alpha,beta).

        :param x,y: The point in the image plane.
        """
        alpha = np.arctan(np.sqrt(x*x+y*y)*np.tan(self.fov))
        beta = np.arctan2(-y, x)%(2.0*np.pi)        # shift beta from [-pi,pi] to [0,2pi]
        return (self.t, self.r, self.theta, self.phi, alpha, beta)

