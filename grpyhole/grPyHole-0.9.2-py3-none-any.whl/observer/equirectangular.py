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

# what is imported by "from equirectangular import *"
__all__ = ["Equirectangular"]

from .stereographic import Stereographic
import numpy as np

class Equirectangular(Stereographic):
    """Class for taking a picture of the black hole with equirectangular (Aveiro) projection."""

    PROJECTION = 'E'                                        #: Identifier of the projection used

    def __init__(self, r, theta, fov=np.pi/4, zoom=((-1.0,1.0), (-1.0,1.0))):
        """Set up the Observer.

        :param r,theta: The position of the Observer.
        :param fov: The field of view of the Observer in the image plane. For this Observer (only!) this can also be a tuple of two angles, one along the x-axis of the image, and one along the y-axis. Note that in that case some functions related to the black hole shape are not available.
        """
        if np.isscalar(fov):
            fov = [fov, fov]
        super(Equirectangular,self).__init__(r, theta, fov, zoom);

    def __str__(self):
        """Show human readable summary of the current setup.
        """
        res = 'Projection: Equirectangular (EquirectangularObserver)\n'
        res = res + 'Field of view along x, y (deg): {}\n'.format(np.rad2deg(self.fov))
        res = res + 'Observer position [t,r,theta,phi]: [{},{},{},{}]\n'.format(self.t, self.r, np.rad2deg(self.theta), np.rad2deg(self.phi))
        res = res + super(Stereographic,self).__str__();    # note how we skip our direct parent to avoid garbled output!
        return res

    def unproject(self, x, y):
        """Unproject a given point (x,y) in the image plane to an initial position
        and viewing angle (t,r,theta,phi,alpha,beta).

        :param x,y: The point in the image plane.
        """
        betap = x*self.fov[0]
        alphap = y*self.fov[1]
        alpha = np.arccos(np.cos(alphap)*np.cos(betap))
        beta = np.arctan2(-np.tan(alphap),np.sin(betap))
        return (self.t, self.r, self.theta, self.phi, alpha, beta)

    def project(self, alpha, beta):
        """Project a given viewing direction (alpha,beta) onto a point (x,y) in the image plane.

        :param alpha,beta: the viewing angle.
        """
        alphap = np.arcsin(-np.sin(alpha)*np.sin(beta))
        betap = np.arctan2(np.sin(alpha)*np.cos(beta), np.cos(alpha))
        return (betap/self.fov[0], alphap/self.fov[1])
