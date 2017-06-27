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

# What is to be imported by "from propagator import *"
__all__ = ["Propagator"]

class Propagator(object):
    """Propagator for a light ray or a whole set of light rays.
    Encapsulates all the required physics.
    This is an abstract class that is subclassed by each type of propagator."""
    LMAX = 1000.0                       #: Maximum integration variable lambda before stopping integration and declaring failure
    TOLERANCE = 1e-6                    #: Integrator tolerance
    VERBOSE = True                      #: Print extra output while integrating

    def __init__(self, o, g, Rsky=0.0):
        """Create a new Propagator.

        :param o: The observer associated with this propagator.
        :param g: The metric associated with this propagator.
        :param Rsky: The celestial sphere radius or 0.0 for infinite radius
        """
        self.g = g
        self.o = o
        self.Rsky = Rsky

    def __str__(self):
        """Show human readable summary of the current setup.
        """
        res  = 'Celestial sphere radius: {}\n'.format(self.Rsky)
        res += 'Tolerance: {}\n'.format(self.TOLERANCE)
        res += 'Maximum lambda: {}\n\n'.format(self.LMAX)
        res += str(self.g)
        res += "\n"
        res += str(self.o)
        return res

    def generateImageData(self, size=(100,100), NP=1, i=0):
        """Generate directions table and set it in the camera / return it.
        If called with NP=1 it performs the whole computation in a single process
        and stores them directly in the camera.
        If called with NP>1, only partial results are computed and returned,
        while nothing is stored in the camera.


        :param size: The size of the directions table (= resolution of the resulting image).
        :param NP: The total number of slices (or processors) for parallel computation.
        :param i: The number of the slice of the directions table (for the i-th processor) to return.
        """
        raise NameError('Must be implemented by subclass!')

    def propagate(self, ic, store=False, dt=10.0):
        """Propagation of a ray and final angle calculation. This performs a
        backward propagation in time, but the initial condition is given in
        forward time (i.e. the velocity is the actual forward-time velocity).

        :param ic: Initial condition as position and viewing angle (t,r,theta,phi,alpha,beta) (see :meth:`getICMomenta`) or directly as (t,r,theta,phi,pt,pr,ptheta,pphi)
        :param store: If true, return the trajectory every integration interval
        :param dt: Absolute length of one integration interval (within integration is performed with automatic step size control)
        :return: ((theta,phi), trajectory).
            Resulting angles are normalized to [0,2pi) for phi and [0,pi) for theta.

            - In case of collissions with the black hole, theta-2pi, phi-2pi is returned
            - In case of errors (-100.0,3.0) is returned.
            - In case of trapped rays (-100.0,2.0) is returned.

            Trajectory contains the points along the trajectory (in rows), in all cases there is at least the initial and final point.
            The trajectory data is always: integration variable lambda, the full state (4 position + 4 momenta), the winding number, the total winding number, the null condition violation (if available, else -1.0), and any other integrator dependent data
        """
        raise NameError('Must be implemented by subclass!')
