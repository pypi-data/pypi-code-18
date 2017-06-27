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

# what is imported by "from observer import *"
__all__ = ["Observer"]

class Observer(object):
    """Observer class defining the coordinate frame and projection of the observer."""

    PROJECTION = 'X'                                        #: Identifier of the projection used

    def __init__(self, zoom=((-1.0,1.0), (-1.0,1.0))):
        """Set up the Observer.

        :param zoom: The region *((xmin, xmax), (ymin, ymax))* in image coordinates where the observer is looking.
        """
        self.zoom = zoom            #: The part of the image that is zoomed ((xmin,xmax), (ymin,ymax)) in image coordinates

    def __str__(self):
        """Show human readable summary of the current setup.
        """
        res = 'Zoom: ({},{})x({},{})\n'.format(self.zoom[0][0], self.zoom[0][1], self.zoom[1][0], self.zoom[1][1])
        return res

    def zoomed(self):
        """Is this Observer zoomed in?
        """
        return self.zoom[0][0] != -1.0 or self.zoom[0][1] != 1.0 or self.zoom[1][0] != -1.0 or self.zoom[1][1] != 1.0

    def project(self, alpha, beta):
        """Project a given viewing direction (alpha,beta) onto a point (x,y) in the image plane.

        :param alpha,beta: the viewing angle.
        """
        raise NameError('Must be implemented by subclass!')

    def unproject(self, x, y):
        """Unproject a given point (x,y) in the image plane to an initial position
        and viewing angle (t,r,theta,phi,alpha,beta).

        :param x,y: The point in the image plane.
        """
        raise NameError('Must be implemented by subclass!')
