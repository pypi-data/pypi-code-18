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

# what is imported by "from stereographic import *"
__all__ = ["Stereographic"]

from .observer import Observer
from math import tan
import numpy as np

class Stereographic(Observer):
    """Class for taking a picture of the black hole with a stereographic projection (close to actual telescope or observer)."""

    PROJECTION = 'S'                                        #: Identifier of the projection used

    def __init__(self, r, theta, fov=np.pi/4, zoom=((-1.0,1.0), (-1.0,1.0))):
        """Set up the Observer.

        :param r,theta: The position of the Observer (t=0, phi=0 is implied).
        :param fov: The field of view of the Observer in the image plane.
        :param zoom: The region ((xmin, xmax), (ymin, ymax)) in image coordinates where the observer is looking.
        """
        super(Stereographic,self).__init__(zoom);
        self.fov = fov      #: The field of view of the Observer in the image plane.
        self.t = 0.0;       #: The time at which the Observer is located
        self.r = r;         #: The radius at which the Observer is located
        self.theta = theta; #: The theta angle at which the Observer is located
        self.phi = 0.0;     #: The phi angle at which the Observer is located (wlog chosen to be zero)

    def __str__(self):
        """Show human readable summary of the current setup.
        """
        res = 'Projection: Stereographic (StereographicObserver)\n'
        res = res + 'Field of view (deg): {}\n'.format(np.rad2deg(self.fov))
        res = res + 'Observer position [t,r,theta,phi]: [{},{},{},{}]\n'.format(self.t, self.r, np.rad2deg(self.theta), np.rad2deg(self.phi))
        res = res + super(Stereographic,self).__str__();
        return res

    def project(self, alpha, beta):
        """Project a given viewing direction (alpha,beta) onto a point (x,y) in the image plane.

        :param alpha,beta: the viewing angle.
        """
        return (np.tan(alpha/2.0)*np.cos(beta)/tan(self.fov/2.0), -np.tan(alpha/2.0)*np.sin(beta)/tan(self.fov/2.0))

    def unproject(self, x, y):
        """Unproject a given point (x,y) in the image plane to an initial position
        and viewing angle (t,r,theta,phi,alpha,beta).

        :param x,y: The point in the image plane.
        """
        alpha = 2.0*np.arctan(np.sqrt(x*x+y*y)*np.tan(self.fov/2.0))
        beta = np.arctan2(-y, x)%(2.0*np.pi)        # shift beta from [-pi,pi] to [0,2pi]
        return (self.t, self.r, self.theta, self.phi, alpha, beta)
