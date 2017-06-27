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

# what is imported by "from hr import *"
__all__ = ["HR", "CHR"]

import numpy as np
from scipy.interpolate import RectBivariateSpline
from .base import SphericalMetric, CartesianMetric

class Functions(object):
    """Functions and properties fully defining an HR metric."""
    NX = 101        #: number of points to sample in X for OpenCL
    Ntheta = 101    #: number of points to sample in theta for OpenCL
    EH = 0.0        #: Event horizon for these functions

    def __str__(self):
        """Return Human readable representation.
        """
        return ""

    def sample(self, dtype=np.float32):
        """Sample this metric's generator functions over a grid made from
        ``self.Ntheta`` by ``self.NX`` points.
        The result is stored in the class members Y, dX_Y, dth_Y
        where Y contains the function values,
        dX_Y the X derivatives and dth_Y the theta derivatives. Each array is
        of the form Y[j_theta,j_X,i] where j_theta and j_X select the point in x
        and theta in increasing order and i indicates the functions F0, F1, F2,
        and W.

        :param dtype: The type of the values in the resulting arrays.
        """

        # check for cached version of the grid and don't need to recompute
        if hasattr(self,'Y') and self.Y.shape == (self.Ntheta, self.NX, 4):
            return (self.Y, self.dX_Y, self.dth_Y)

        X_grid = np.linspace(0.0, 1.0, self.NX)
        theta_grid = np.linspace(0.0, np.pi, self.Ntheta)
        self.Y = np.empty((self.Ntheta, self.NX, 4), dtype=dtype)
        self.dX_Y = np.empty((self.Ntheta, self.NX, 4), dtype=dtype)
        self.dth_Y = np.empty((self.Ntheta, self.NX, 4), dtype=dtype)

        # Order is (X, theta) in OpenCL device code, which requires (theta, X) in Python.
        THETA, X = np.meshgrid(theta_grid, X_grid, indexing='ij')

        self.Y[:,:,0] = self.F0( X, THETA, dX=0, dtheta=0 )
        self.Y[:,:,1] = self.F1( X, THETA, dX=0, dtheta=0 )
        self.Y[:,:,2] = self.F2( X, THETA, dX=0, dtheta=0 )
        self.Y[:,:,3] = self.W(  X, THETA, dX=0, dtheta=0 )

        self.dX_Y[:,:,0] = self.F0( X, THETA, dX=1, dtheta=0 )
        self.dX_Y[:,:,1] = self.F1( X, THETA, dX=1, dtheta=0 )
        self.dX_Y[:,:,2] = self.F2( X, THETA, dX=1, dtheta=0 )
        self.dX_Y[:,:,3] = self.W(  X, THETA, dX=1, dtheta=0 )

        self.dth_Y[:,:,0] = self.F0( X, THETA, dX=0, dtheta=1 )
        self.dth_Y[:,:,1] = self.F1( X, THETA, dX=0, dtheta=1 )
        self.dth_Y[:,:,2] = self.F2( X, THETA, dX=0, dtheta=1 )
        self.dth_Y[:,:,3] = self.W(  X, THETA, dX=0, dtheta=1 )

    def F0(self, X, theta, dX=0, dtheta=0):
        """Evaluate F0.

        :param X: X coordinate where to evaluate F0 (see :meth:`r2X`).
        :param theta: Theta coordinate where to evaluate F0.
        :param dx: order of the X derivative (0 or 1).
        :param dy: order of the theta derivative (0 or 1).
        """
        raise NameError('Must be implemented by subclass!')

    def F1(self, X, theta, dX=0, dtheta=0):
        """Evaluate F1.

        :param X: X coordinate where to evaluate F0 (see :meth:`r2X`).
        :param theta: Theta coordinate where to evaluate F0.
        :param dx: order of the X derivative (0 or 1).
        :param dy: order of the theta derivative (0 or 1).
        """
        raise NameError('Must be implemented by subclass!')

    def F2(self, X, theta, dX=0, dtheta=0):
        """Evaluate F2.

        :param X: X coordinate where to evaluate F0 (see :meth:`r2X`).
        :param theta: Theta coordinate where to evaluate F0.
        :param dx: order of the X derivative (0 or 1).
        :param dy: order of the theta derivative (0 or 1).
        """
        raise NameError('Must be implemented by subclass!')

    def W(self, X, theta, dX=0, dtheta=0):
        """Evaluate W.

        :param X: X coordinate where to evaluate F0 (see :meth:`r2X`).
        :param theta: Theta coordinate where to evaluate F0.
        :param dx: order of the X derivative (0 or 1).
        :param dy: order of the theta derivative (0 or 1).
        """
        raise NameError('Must be implemented by subclass!')


class Flat(Functions):
    """Flat HR metric functions."""

    def F0(self, X, theta, dX=0, dtheta=0):
        """Evaluate F0.

        :param X: X coordinate where to evaluate F0 (see :meth:`r2X`).
        :param theta: Theta coordinate where to evaluate F0.
        :param dx: order of the X derivative (0 or 1).
        :param dy: order of the theta derivative (0 or 1).
        """
        return 0.0

    def F1(self, X, theta, dX=0, dtheta=0):
        """Evaluate F1.

        :param X: X coordinate where to evaluate F0 (see :meth:`r2X`).
        :param theta: Theta coordinate where to evaluate F0.
        :param dx: order of the X derivative (0 or 1).
        :param dy: order of the theta derivative (0 or 1).
        """
        return 0.0

    def F2(self, X, theta, dX=0, dtheta=0):
        """Evaluate F2.

        :param X: X coordinate where to evaluate F0 (see :meth:`r2X`).
        :param theta: Theta coordinate where to evaluate F0.
        :param dx: order of the X derivative (0 or 1).
        :param dy: order of the theta derivative (0 or 1).
        """
        return 0.0

    def W(self, X, theta, dX=0, dtheta=0):
        """Evaluate W.

        :param X: X coordinate where to evaluate F0 (see :meth:`r2X`).
        :param theta: Theta coordinate where to evaluate F0.
        :param dx: order of the X derivative (0 or 1).
        :param dy: order of the theta derivative (0 or 1).
        """
        return 0.0


class Schwarzschild(Functions):
    """Schwarzschild HR metric functions."""

    def __init__(self, EH):
        """Create new HR functions representing a Schwarzschild BH with given event horizon.

        :param EH: The Schwarzschild radius (event horizon) of this black hole.
        """
        self.EH = EH

    def F0(self, X, theta, dX=0, dtheta=0):
        """Evaluate F0.

        :param X: X coordinate where to evaluate F0 (see :meth:`r2X`).
        :param theta: Theta coordinate where to evaluate F0.
        :param dx: order of the X derivative (0 or 1).
        :param dy: order of the theta derivative (0 or 1).
        """
        return 0.0

    def F1(self, X, theta, dX=0, dtheta=0):
        """Evaluate F1.

        :param X: X coordinate where to evaluate F0 (see :meth:`r2X`).
        :param theta: Theta coordinate where to evaluate F0.
        :param dx: order of the X derivative (0 or 1).
        :param dy: order of the theta derivative (0 or 1).
        """
        return 0.0

    def F2(self, X, theta, dX=0, dtheta=0):
        """Evaluate F2.

        :param X: X coordinate where to evaluate F0 (see :meth:`r2X`).
        :param theta: Theta coordinate where to evaluate F0.
        :param dx: order of the X derivative (0 or 1).
        :param dy: order of the theta derivative (0 or 1).
        """
        return 0.0

    def W(self, X, theta, dX=0, dtheta=0):
        """Evaluate W.

        :param X: X coordinate where to evaluate F0 (see :meth:`r2X`).
        :param theta: Theta coordinate where to evaluate F0.
        :param dx: order of the X derivative (0 or 1).
        :param dy: order of the theta derivative (0 or 1).
        """
        return 0.0


class Interpolated(Functions):
    """HR functions interpolated from regular grid."""
    SPLINE_ORDER = 2        #: Order of the splines used to interpolate the metric functions (must be at least 2).

    def __init__(self, filename, raster_scale=15):
        """Create new numerically interpolated blackhole.

        :param filename: The NumPy style data file containing the information on the metric.
        :param raster_scale: A factor to increase the sampling relative to the grid in the data file.
        """
        self.filename = filename
        with np.load(filename) as data:
            # these are parameters of the simulation, and should be read from our data files along with the actual metric
            # only EH is manatory, as it is used in the metric computation
            # m_ADM is not manadtory but used in outside code
            self.EH         = data['EH'][()]
            if 'OmegaH' in data.files:
                self.OmegaH = data['OmegaH'][()]
            if 'm' in data.files:
                self.m      = data['m'][()]
            if 'w' in data.files:
                self.w      = data['w'][()]
            if 'm_ADM' in data.files:
                self.m_ADM  = data['m_ADM'][()]
            if 'L_ADM' in data.files:
                self.L_ADM  = data['L_ADM'][()]
            if 'm_BH' in data.files:
                self.m_BH   = data['m_BH'][()]
            if 'L_BH' in data.files:
                self.L_BH   = data['L_BH'][()]
            if 'm_SF' in data.files:
                self.m_SF   = data['m_SF'][()]
            if 'L_SF' in data.files:
                self.L_SF   = data['L_SF'][()]
            # this is the actual metric parameters on a regular (X,theta) grid
            self._Xdata  = data['X']
            self._THdata = data['TH']
            self._F0data = data['F0']
            self._F1data = data['F1']
            self._F2data = data['F2']
            self._Wdata  = data['W']
            # spline interpolation objects
            self._F0 = RectBivariateSpline(self._Xdata, self._THdata, self._F0data, kx=self.SPLINE_ORDER, ky=self.SPLINE_ORDER);
            self._F1 = RectBivariateSpline(self._Xdata, self._THdata, self._F1data, kx=self.SPLINE_ORDER, ky=self.SPLINE_ORDER);
            self._F2 = RectBivariateSpline(self._Xdata, self._THdata, self._F2data, kx=self.SPLINE_ORDER, ky=self.SPLINE_ORDER);
            self._W  = RectBivariateSpline(self._Xdata, self._THdata, self._Wdata,  kx=self.SPLINE_ORDER, ky=self.SPLINE_ORDER);

        self.NX = raster_scale*len(self._Xdata)
        # make sure Ntheta is odd so there is a node at pi/2
        self.Ntheta = raster_scale*(((len(self._THdata)+1)//2)*2)+1

    def __str__(self):
        """Show human readable summary of the current setup.
        """
        res =       'Data file:     {}\n'.format(self.filename)
        res = res + 'Spline order:  {}\n'.format(self.SPLINE_ORDER)
        res = res + 'OmegaH: {}\n'.format(self.OmegaH)
        res = res + 'm:      {}\n'.format(self.m)
        res = res + 'w:      {}\n'.format(self.w)
        res = res + 'm_ADM:  {}\n'.format(self.m_ADM)
        res = res + 'L_ADM:  {}\n'.format(self.L_ADM)
        res = res + 'm_BH:   {}\n'.format(self.m_BH)
        res = res + 'L_BH:   {}\n'.format(self.L_BH)
        res = res + 'm_SF:   {}\n'.format(self.m_SF)
        res = res + 'L_SF:   {}\n\n'.format(self.L_SF)
        return res

    def F0(self, X, theta, dX=0, dtheta=0):
        """Evaluate F0.

        :param X: X coordinate where to evaluate F0 (see :meth:`r2X`).
        :param theta: Theta coordinate where to evaluate F0.
        :param dx: order of the X derivative (0 or 1).
        :param dy: order of the theta derivative (0 or 1).
        """
        return self._F0(X, theta, dx=dX, dy=dtheta, grid=False)

    def F1(self, X, theta, dX=0, dtheta=0):
        """Evaluate F1.

        :param X: X coordinate where to evaluate F0 (see :meth:`r2X`).
        :param theta: Theta coordinate where to evaluate F0.
        :param dx: order of the X derivative (0 or 1).
        :param dy: order of the theta derivative (0 or 1).
        """
        return self._F1(X, theta, dx=dX, dy=dtheta, grid=False)

    def F2(self, X, theta, dX=0, dtheta=0):
        """Evaluate F2.

        :param X: X coordinate where to evaluate F0 (see :meth:`r2X`).
        :param theta: Theta coordinate where to evaluate F0.
        :param dx: order of the X derivative (0 or 1).
        :param dy: order of the theta derivative (0 or 1).
        """
        return self._F2(X, theta, dx=dX, dy=dtheta, grid=False)

    def W(self, X, theta, dX=0, dtheta=0):
        """Evaluate W.

        :param X: X coordinate where to evaluate F0 (see :meth:`r2X`).
        :param theta: Theta coordinate where to evaluate F0.
        :param dx: order of the X derivative (0 or 1).
        :param dy: order of the theta derivative (0 or 1).
        """
        return self._W(X, theta, dx=dX, dy=dtheta, grid=False)



class _HRCommon:
    """Routines common to all HR metrics. Used as a mix-in to the HR and CHR classes."""
    FIX_SAMPLER = 1                     #: In OpenCL code, if 1 use our own linear interpolation to work around broken OpenCL implementations

    def getRadius(self, R):
        """Get the radius in BL coordinates given a circumferential radius **R**.
        This routine overwrites the one in SphericalMetric and also adds this
        functionality to the Cartesian HR metrics as it is implemented directly
        in terms of the generator functions.

        :param R: The circumferential radius **R** to convert.
        """
        from scipy.optimize import newton
        theta = np.pi/2
        f = lambda r: np.exp(self.f.F2(self.r2X(r), theta))*r-R
        df = lambda r: (self.dr_r2X(r)*self.f.F2(self.r2X(r), theta, dX=1, dtheta=0)*r + 1.0)*np.exp(self.f.F2(self.r2X(r), theta))
        sol = newton(f, R, df)
        return sol

    def cl_allocate(self, context, device, commandQueue, real):
        """Called after the OpenCL propagator has allocated the **device**,
        created a **context**, and set up a command queue. The metric here can
        perform additional setup tasks on the **device** before running
        propagations. This includes setting the various ``cl_*`` class members
        to appropriate values.

        There are two main ways to pass data to an OpenCL metric:

        * by compiler flag (``-D MYVAR=1.23``) which then can be used in the
          OpenCL code as ``MYVAR``
        * by user defined argument. These are passed as additional arguments
          to the :meth:`updateMetric` function. Their values and types must be
          declared in the ``cl_args`` and ``cl_argstypes`` member variables, typically
          during the call to :meth:`cl_allocate`.

        :param context: The PyOpenCL context of the OpenCL computation.
        :param device: The PyOpenCL device used for the OpenCL computation.
        :param commandQueue: The PyOpenCL command queue on the device.
        :param real: The type of "real" numbers (either ``np.float32`` or
            ``np.float64``). Can be used as ``real(5.6)`` to convert Python numbers to
            the correct numerical memory layout expected by the OpenCL kernel
            for its arguments.
        """
        import pyopencl as cl       # only needed for these OpenCL specific routines so not included globally

        # Create images for OpenCL image sampler.
        self.f.sample(dtype=np.float32)
        self.img = cl.image_from_array(context, self.f.Y, num_channels=4)
        self.dX_img = cl.image_from_array(context, self.f.dX_Y, num_channels=4)
        self.dth_img = cl.image_from_array(context, self.f.dth_Y, num_channels=4)

        self.cl_args = [self.img, self.dX_img, self.dth_img]
        self.cl_argstypes = [None, None, None]
        self.cl_flags += " -D FIX_SAMPLER={:d} -D NX={:d} -D NTHETA={:d} -D EH={:.16e} -D RCUTOFF={:.16e}".format(self.FIX_SAMPLER, self.f.NX, self.f.Ntheta, self.EH, self.rCutoff)

    def cl_free(self):
        """Free and OpenCL resources allocated earlier."""
        self.img.release()
        self.dX_img.release()
        self.dth_img.release()


class HR(_HRCommon, SphericalMetric):
    ID = 'HR'    #: short identifier of this metric; used e.g. in file names
    CL_CODE = "HR.cl"                   #: Our OpenCL source file

    """Metric in exponential form in both spherical and Cartesian coordinates."""
    def __init__(self, f):
        """Create new exponential form blackhole.

        :param f: An HR function object.
        """
        super(HR, self).__init__()
        self.EH = f.EH
        self.rCutoff = self.CUTOFF_FACTOR*self.EH
        self.f = f

    def __str__(self):
        """Show human readable summary of the current setup.
        """
        res = 'Metric: Herdeiro-Radu (HRMetric)\n'
        res = res + 'Event horizon:        {}\n'.format(self.EH)
        res = res + 'Cutoff radius:        {}\n\n'.format(self.rCutoff)
        res = res + str(self.f)
        res += super(HR,self).__str__();
        return res

    def update(self):
        """Compute the relevant components of the metric at the current point and store them in the attributes.

        :return: An error flag that is True if an error occured (most likely the ray fell into the black hole) or False otherwise.
        """
        r = self.x[1]
        theta = self.x[2]
        # correct various coordinates. Done differently for scalars and vectors.
        if isinstance(r, np.ndarray):
            # correct for non-canonical coordinates. May be necessary for specific cases in flat metric.
            # Note there is no phi dependence, hence phi is not adjusted
            cond = r<0.0
            r[cond] = -r[cond]
            theta[cond] = np.pi-theta[cond]
            # check if fallen in, this is returned later.
            result = r<self.rCutoff
            # normalize theta. Note there is no phi dependence, hence phi is not adjusted
            theta = theta%(2.0*np.pi)
            cond = theta>=np.pi
            theta[cond] = 2.0*np.pi - theta[cond]
            # Hack to prevent divisions by zero: if we are too close to the coordinate singularity enforce minimum size for theta
            cond = theta<1e-12
            theta[cond] = 1e-12
        else:
            # correct for non-canonical coordinates. May be necessary for specific cases in flat metric.
            # Note there is no phi dependence, hence phi is not adjusted
            if r<0.0:
                r = -r
                theta = np.pi-theta
            # check if fallen in
            if r<self.rCutoff: return True
            result = False
            # normalize theta. Note there is no phi dependence, hence phi is not adjusted
            theta = theta%(2.0*np.pi)
            if theta>=np.pi:
                theta = 2.0*np.pi - theta
            # Hack to prevent divisions by zero: if we are too close to the coordinate singularity enforce minimum size for theta
            if theta<1e-12: theta = 1e-12

        # interpolate and take derivatives
        XX = self.r2X(r)       # this is the first index to use for the extrapolation table along with theta
        dr = self.dr_r2X(r)
        F0 = self.f.F0(XX, theta)
        F1 = self.f.F1(XX, theta)
        F2 = self.f.F2(XX, theta)
        W  = self.f.W( XX, theta)

        dr_F0 = dr*self.f.F0(XX, theta, dX=1, dtheta=0)
        dr_F1 = dr*self.f.F1(XX, theta, dX=1, dtheta=0)
        dr_F2 = dr*self.f.F2(XX, theta, dX=1, dtheta=0)
        dr_W  = dr*self.f.W( XX, theta, dX=1, dtheta=0)

        dth_F0 = self.f.F0(XX, theta, dX=0, dtheta=1)
        dth_F1 = self.f.F1(XX, theta, dX=0, dtheta=1)
        dth_F2 = self.f.F2(XX, theta, dX=0, dtheta=1)
        dth_W  = self.f.W( XX, theta, dX=0, dtheta=1)

        # calculate actual contravariant metric
        N = 1.0 - self.EH/r
        Ninv = 1.0/N
        W2 = W*W
        r2 = r*r
        dr_N = self.EH/r2
        eF0 = np.exp(-2.0*F0)
        eF1 = np.exp(-2.0*F1)
        eF2 = np.exp(-2.0*F2)

        # some common terms for reuse
        t1 = eF0*Ninv
        t2 = eF2/(r2*np.sin(theta)**2)
        t3 = eF1/r2

        self.tt = -t1
        self.rr = N*eF1
        self.thth = t3
        self.pp = t2 - W2*t1
        self.tp = -W*t1

        self.dr_tt = (2.0*dr_F0 + dr_N*Ninv)*t1
        self.dr_rr = (dr_N - 2.0*dr_F1*N)*eF1
        self.dr_thth = 2.0*(-1.0/r - dr_F1)*t3
        self.dr_pp = -2.0*((dr_F2 + 1.0/r)*t2 - (dr_F0*W - dr_W)*W*t1) + dr_N*W2*t1*Ninv
        self.dr_tp = ((2.0*dr_F0  + dr_N*Ninv)*W - dr_W)*t1

        self.dth_tt = 2.0*dth_F0*t1
        self.dth_rr = -2.0*dth_F1*N*eF1
        self.dth_thth = -2.0*dth_F1*t3
        self.dth_pp = -2.0*((dth_F2 + 1.0/np.tan(theta))*t2 + (dth_W - dth_F0*W)*W*t1)
        self.dth_tp = (2.0*dth_F0*W - dth_W)*t1

        return result


class CHR(_HRCommon, CartesianMetric):
    ID = 'CHR'      #: short identifier of this metric; used e.g. in file names
    EPS_RP = 1e-6   #: Cutoff for using the analytical limit near the z axis in Cartesian coordinates.
    CL_CODE = "CHR.cl"                  #: Our OpenCL source file

    """Metric in exponential form in both spherical and Cartesian coordinates."""
    def __init__(self, f):
        """Create new exponential form blackhole.

        :param EH: The event horizon.
        :param f: An HR function object.
        """
        super(CHR, self).__init__()
        self.EH =f. EH
        self.rCutoff = self.CUTOFF_FACTOR*self.EH
        self.f = f

    def __str__(self):
        """Show human readable summary of the current setup.
        """
        res = 'Metric: Cartesian Herdeiro-Radu (CHRMetric)\n'
        res = res + 'Event horizon:        {}\n'.format(self.EH)
        res = res + 'Cutoff radius:        {}\n\n'.format(self.rCutoff)
        res = res + str(self.f)
        res += super(CHR,self).__str__();
        return res

    def cl_allocate(self, context, device, commandQueue, real):
        """Called after the OpenCL propagator has allocated the **device**,
        created a **context**, and set up a command queue. The metric here can
        perform additional setup tasks on the **device** before running
        propagations. This includes setting the various ``cl_*`` class members
        to appropriate values.

        There are two main ways to pass data to an OpenCL metric:

        * by compiler flag (``-D MYVAR=1.23``) which then can be used in the
          OpenCL code as ``MYVAR``
        * by user defined argument. These are passed as additional arguments
          to the :meth:`updateMetric` function. Their values and types must be
          declared in the ``cl_args`` and ``cl_argstypes`` member variables, typically
          during the call to :meth:`cl_allocate`.

        :param context: The PyOpenCL context of the OpenCL computation.
        :param device: The PyOpenCL device used for the OpenCL computation.
        :param commandQueue: The PyOpenCL command queue on the device.
        :param real: The type of "real" numbers (either ``np.float32`` or
            ``np.float64``). Can be used as ``real(5.6)`` to convert Python numbers to
            the correct numerical memory layout expected by the OpenCL kernel
            for its arguments.
        """
        super(CHR,self).cl_allocate(context, device, commandQueue, real)
        self.cl_flags += " -D EPS_RP={:.16e} ".format(self.EPS_RP)

    def update(self):
        """Compute the relevant components of the metric at the current point and store them in the attributes.

        :return: An error flag that is True if an error occured (most likely the ray fell into the black hole) or False otherwise.
        """
        x = self.x[1]
        y = self.x[2]
        z = self.x[3]
        x2 = x*x
        y2 = y*y
        z2 = z*z
        r2 = x2+y2+z2
        r = np.sqrt(r2)
        # check if fallen in, this is returned later. We don't immediately return because this may be vectorized and called with many coordinates, some of which may fail some of which may not.
        result = r<self.rCutoff
        rp2 = x2+y2
        rp4 = rp2*rp2
        rp = np.sqrt(rp2)
        theta = np.arccos(z/r)
        XX = self.r2X(r)       # this is the first index to use for the extrapolation table along with theta
        dr = self.dr_r2X(r)

        # interpolate and take derivatives wrt (r, theta)
        F0 = self.f.F0(XX, theta)
        F1 = self.f.F1(XX, theta)
        F2 = self.f.F2(XX, theta)
        W  = self.f.W( XX, theta)

        dr_F0 = dr*self.f.F0(XX, theta, dX=1, dtheta=0)
        dr_F1 = dr*self.f.F1(XX, theta, dX=1, dtheta=0)
        dr_F2 = dr*self.f.F2(XX, theta, dX=1, dtheta=0)
        dr_W  = dr*self.f.W( XX, theta, dX=1, dtheta=0)

        dth_F0 = self.f.F0(XX, theta, dX=0, dtheta=1)
        dth_F1 = self.f.F1(XX, theta, dX=0, dtheta=1)
        dth_F2 = self.f.F2(XX, theta, dX=0, dtheta=1)
        dth_W  = self.f.W( XX, theta, dX=0, dtheta=1)

        # partials for coordinate change in derivative
        drdx = x/r
        drdy = y/r
        drdz = z/r
        if isinstance(x, np.ndarray):
            dthdx = z*x/(r2*rp)
            dthdy = z*y/(r2*rp)
            rp2inv = 1.0/rp2
            rp4inv = 1.0/rp4
            cond = rp<self.EPS_RP
            dthdx[cond] = 0.0
            dthdy[cond] = 0.0
            rp2inv[cond] = 0.0
            rp4inv[cond] = 0.0
        else:
            if rp<self.EPS_RP:
                dthdx = 0.0
                dthdy = 0.0
                rp2inv = 0.0        # we adjust explicitly in the equations below where the limit of terms involving rp2inv or rp4inv is non-zero
                rp4inv = 0.0
            else:
                dthdx = z*x/(r2*rp)
                dthdy = z*y/(r2*rp)
                rp2inv = 1.0/rp2
                rp4inv = 1.0/rp4
        dthdz = -rp/r2

        # change derivatives wrt (x, y, z)
        dx_F0 = drdx*dr_F0 + dthdx*dth_F0
        dy_F0 = drdy*dr_F0 + dthdy*dth_F0
        dz_F0 = drdz*dr_F0 + dthdz*dth_F0
        dx_F1 = drdx*dr_F1 + dthdx*dth_F1
        dy_F1 = drdy*dr_F1 + dthdy*dth_F1
        dz_F1 = drdz*dr_F1 + dthdz*dth_F1
        dx_F2 = drdx*dr_F2 + dthdx*dth_F2
        dy_F2 = drdy*dr_F2 + dthdy*dth_F2
        dz_F2 = drdz*dr_F2 + dthdz*dth_F2
        dx_W  = drdx*dr_W  + dthdx*dth_W
        dy_W  = drdy*dr_W  + dthdy*dth_W
        dz_W  = drdz*dr_W  + dthdz*dth_W

        # more useful constants
        N = 1.0 - self.EH/r
        N2 = N*N
        W2 = W*W
        dr_N = self.EH/r2
        dx_N = drdx*dr_N
        dy_N = drdy*dr_N
        dz_N = drdz*dr_N
        eF0 = np.exp( 2.0*F0 )
        eF1 = np.exp( 2.0*F1 )
        eF2 = np.exp( 2.0*F2 )

        # calculate actual contravariant metric
        self.tt = -1.0/(eF0*N)
        self.tx = (y*W)/(eF0*N)
        self.ty = -(x*W)/(eF0*N)
        self.xx = (x2/eF1 + y2/eF2)*rp2inv + (x2*(-1.0 + N))/(eF1*r2) - (y2*W2)/(eF0*N)
        self.yy = (x2/eF2 + y2/eF1)*rp2inv + (y2*(-1.0 + N))/(eF1*r2) - (x2*W2)/(eF0*N)
        self.xy = ((1.0/eF1 - 1.0/eF2)*x*y)*rp2inv + (x*y*(-1.0 + N))/(eF1*r2) + (x*y*W2)/(eF0*N)
        # adjust for missing limit involving rp2inv in expressions above
        if isinstance(x, np.ndarray):
                self.xx[cond] += 1.0/eF1[cond]
                self.yy[cond] += 1.0/eF1[cond]
        elif rp<self.EPS_RP:
                self.xx += 1.0/eF1
                self.yy += 1.0/eF1
        self.zz = 1.0/eF1 + (z2*(-1.0 + N))/(eF1*r2)
        self.xz = (x*z*(-1.0 + N))/(eF1*r2)
        self.yz = (y*z*(-1.0 + N))/(eF1*r2)

        self.dx_tt = (2.0*dx_F0)/(eF0*N) + dx_N/(eF0*N2)
        self.dx_tx = (-2.0*y*W*dx_F0)/(eF0*N) - (y*W*dx_N)/(eF0*N2) + (y*dx_W)/(eF0*N)
        self.dx_ty = -(W/(eF0*N)) + (2.0*x*W*dx_F0)/(eF0*N) + (x*W*dx_N)/(eF0*N2) - (x*dx_W)/(eF0*N)
        self.dx_xx = (x2*(-1.0 + N))/(eF1*r2)*(-2.0*drdx/r) + (-2.0*x*(x2/eF1 + y2/eF2))*rp4inv + (2.0*x*(-1.0 + N))/(eF1*r2) + (2.0*y2*W2*dx_F0)/(eF0*N) - (2.0*x2*(-1.0 + N)*dx_F1)/(eF1*r2) + ((2.0*x)/eF1 - (2.0*x2*dx_F1)/eF1 - (2.0*y2*dx_F2)/eF2)*rp2inv + (x2*dx_N)/(eF1*r2) + (y2*W2*dx_N)/(eF0*N2) - (2.0*y2*W*dx_W)/(eF0*N)
        self.dx_yy = (y2*(-1.0 + N))/(eF1*r2)*(-2.0*drdx/r) + (-2.0*x*(x2/eF2 + y2/eF1))*rp4inv - (2.0*x*W2)/(eF0*N) + (2.0*x2*W2*dx_F0)/(eF0*N) - (2.0*y2*(-1.0 + N)*dx_F1)/(eF1*r2) + ((2.0*x)/eF2 - (2.0*y2*dx_F1)/eF1 - (2.0*x2*dx_F2)/eF2)*rp2inv + (y2*dx_N)/(eF1*r2) + (x2*W2*dx_N)/(eF0*N2) - (2.0*x2*W*dx_W)/(eF0*N)
        self.dx_xy = (x*y*(-1.0 + N))/(eF1*r2)*(-2.0*drdx/r) + (-2.0*(1.0/eF1 - 1.0/eF2)*x2*y)*rp4inv + ((1.0/eF1 - 1.0/eF2)*y)*rp2inv + (y*(-1.0 + N))/(eF1*r2) + (y*W2)/(eF0*N) - (2.0*x*y*W2*dx_F0)/(eF0*N) - (2.0*x*y*(-1.0 + N)*dx_F1)/(eF1*r2) + (x*y*((-2.0*dx_F1)/eF1 + (2.0*dx_F2)/eF2))*rp2inv + (x*y*dx_N)/(eF1*r2) - (x*y*W2*dx_N)/(eF0*N2) + (2.0*x*y*W*dx_W)/(eF0*N)
        self.dx_zz = (z2*(-1.0 + N))/(eF1*r2)*(-2.0*drdx/r) + (-2.0*dx_F1)/eF1 - (2.0*z2*(-1.0 + N)*dx_F1)/(eF1*r2) + (z2*dx_N)/(eF1*r2)
        self.dx_xz = (x*z*(-1.0 + N))/(eF1*r2)*(-2.0*drdx/r) + (z*(-1.0 + N))/(eF1*r2) - (2.0*x*z*(-1.0 + N)*dx_F1)/(eF1*r2) + (x*z*dx_N)/(eF1*r2)
        self.dx_yz = (y*z*(-1.0 + N))/(eF1*r2)*(-2.0*drdx/r) + (-2.0*y*z*(-1.0 + N)*dx_F1)/(eF1*r2) + (y*z*dx_N)/(eF1*r2)

        self.dy_tt = (2.0*dy_F0)/(eF0*N) + dy_N/(eF0*N2)
        self.dy_tx = W/(eF0*N) - (2.0*y*W*dy_F0)/(eF0*N) - (y*W*dy_N)/(eF0*N2) + (y*dy_W)/(eF0*N)
        self.dy_ty = (2.0*x*W*dy_F0)/(eF0*N) + (x*W*dy_N)/(eF0*N2) - (x*dy_W)/(eF0*N)
        self.dy_xx = (x2*(-1.0 + N))/(eF1*r2)*(-2.0*drdy/r) + (-2.0*y*(x2/eF1 + y2/eF2))*rp4inv - (2.0*y*W2)/(eF0*N) + (2.0*y2*W2*dy_F0)/(eF0*N) - (2.0*x2*(-1.0 + N)*dy_F1)/(eF1*r2) + ((2.0*y)/eF2 - (2.0*x2*dy_F1)/eF1 - (2.0*y2*dy_F2)/eF2)*rp2inv + (x2*dy_N)/(eF1*r2) + (y2*W2*dy_N)/(eF0*N2) - (2.0*y2*W*dy_W)/(eF0*N)
        self.dy_yy = (y2*(-1.0 + N))/(eF1*r2)*(-2.0*drdy/r) + (-2.0*y*(x2/eF2 + y2/eF1))*rp4inv + (2.0*y*(-1.0 + N))/(eF1*r2) + (2.0*x2*W2*dy_F0)/(eF0*N) - (2.0*y2*(-1.0 + N)*dy_F1)/(eF1*r2) + ((2.0*y)/eF1 - (2.0*y2*dy_F1)/eF1 - (2.0*x2*dy_F2)/eF2)*rp2inv + (y2*dy_N)/(eF1*r2) + (x2*W2*dy_N)/(eF0*N2) - (2.0*x2*W*dy_W)/(eF0*N)
        self.dy_xy = (x*y*(-1.0 + N))/(eF1*r2)*(-2.0*drdy/r) + (-2.0*(1.0/eF1 - 1.0/eF2)*x*y2)*rp4inv + ((1.0/eF1 - 1.0/eF2)*x)*rp2inv + (x*(-1.0 + N))/(eF1*r2) + (x*W2)/(eF0*N) - (2.0*x*y*W2*dy_F0)/(eF0*N) - (2.0*x*y*(-1.0 + N)*dy_F1)/(eF1*r2) + (x*y*((-2.0*dy_F1)/eF1 + (2.0*dy_F2)/eF2))*rp2inv + (x*y*dy_N)/(eF1*r2) - (x*y*W2*dy_N)/(eF0*N2) + (2.0*x*y*W*dy_W)/(eF0*N)
        self.dy_zz = (z2*(-1.0 + N))/(eF1*r2)*(-2.0*drdy/r) + (-2.0*dy_F1)/eF1 - (2.0*z2*(-1.0 + N)*dy_F1)/(eF1*r2) + (z2*dy_N)/(eF1*r2)
        self.dy_xz = (x*z*(-1.0 + N))/(eF1*r2)*(-2.0*drdy/r) + (-2.0*x*z*(-1.0 + N)*dy_F1)/(eF1*r2) + (x*z*dy_N)/(eF1*r2)
        self.dy_yz = (y*z*(-1.0 + N))/(eF1*r2)*(-2.0*drdy/r) + (z*(-1.0 + N))/(eF1*r2) - (2.0*y*z*(-1.0 + N)*dy_F1)/(eF1*r2) + (y*z*dy_N)/(eF1*r2)

        self.dz_tt = (2.0*dz_F0)/(eF0*N) + dz_N/(eF0*N2)
        self.dz_tx = (-2.0*y*W*dz_F0)/(eF0*N) - (y*W*dz_N)/(eF0*N2) + (y*dz_W)/(eF0*N)
        self.dz_ty = (2.0*x*W*dz_F0)/(eF0*N) + (x*W*dz_N)/(eF0*N2) - (x*dz_W)/(eF0*N)
        self.dz_xx = (x2*(-1.0 + N))/(eF1*r2)*(-2.0*drdz/r) + (2.0*y2*W2*dz_F0)/(eF0*N) - (2.0*x2*(-1.0 + N)*dz_F1)/(eF1*r2) + ((-2.0*x2*dz_F1)/eF1 - (2.0*y2*dz_F2)/eF2)*rp2inv + (x2*dz_N)/(eF1*r2) + (y2*W2*dz_N)/(eF0*N2) - (2.0*y2*W*dz_W)/(eF0*N)
        self.dz_yy = (y2*(-1.0 + N))/(eF1*r2)*(-2.0*drdz/r) + (2.0*x2*W2*dz_F0)/(eF0*N) - (2.0*y2*(-1.0 + N)*dz_F1)/(eF1*r2) + ((-2.0*y2*dz_F1)/eF1 - (2.0*x2*dz_F2)/eF2)*rp2inv + (y2*dz_N)/(eF1*r2) + (x2*W2*dz_N)/(eF0*N2) - (2.0*x2*W*dz_W)/(eF0*N)
        self.dz_xy = (x*y*(-1.0 + N))/(eF1*r2)*(-2.0*drdz/r) + (-2.0*x*y*W2*dz_F0)/(eF0*N) - (2.0*x*y*(-1.0 + N)*dz_F1)/(eF1*r2) + (x*y*((-2.0*dz_F1)/eF1 + (2.0*dz_F2)/eF2))*rp2inv + (x*y*dz_N)/(eF1*r2) - (x*y*W2*dz_N)/(eF0*N2) + (2.0*x*y*W*dz_W)/(eF0*N)
        # adjust for missing limit involving rp2inv in expressions above
        if isinstance(x, np.ndarray):
            self.dz_xx += -2.0*dz_F1[cond]/eF1[cond]
            self.dz_yy += -2.0*dz_F1[cond]/eF1[cond]
        elif rp<self.EPS_RP:
            self.dz_xx += -2.0*dz_F1/eF1
            self.dz_yy += -2.0*dz_F1/eF1
        self.dz_zz = (z2*(-1.0 + N))/(eF1*r2)*(-2.0*drdz/r) + (2.0*z*(-1.0 + N))/(eF1*r2) - (2.0*dz_F1)/eF1 - (2.0*z2*(-1.0 + N)*dz_F1)/(eF1*r2) + (z2*dz_N)/(eF1*r2)
        self.dz_xz = (x*z*(-1.0 + N))/(eF1*r2)*(-2.0*drdz/r) + (x*(-1.0 + N))/(eF1*r2) - (2.0*x*z*(-1.0 + N)*dz_F1)/(eF1*r2) + (x*z*dz_N)/(eF1*r2)
        self.dz_yz = (y*z*(-1.0 + N))/(eF1*r2)*(-2.0*drdz/r) + (y*(-1.0 + N))/(eF1*r2) - (2.0*y*z*(-1.0 + N)*dz_F1)/(eF1*r2) + (y*z*dz_N)/(eF1*r2)

        return result
