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

# what is imported by "from base import *"
__all__ = ["Metric", "SphericalMetric", "CartesianMetric"]

import numpy as np
from scipy.optimize import brentq

class Metric(object):
    """Stationary, axisymmetric 4D tensor (all contravariant)."""
    ID = ''                 #: short identifier of this metric; used e.g. in file names.
    CUTOFF_FACTOR = 1.005   #: You have to be within this factor of the event horizon to be considered fallen in.
    COORDINATES = "none"    #: What coordinate system this metric uses
    CL_CODE = ""            #: OpenCL source file. If empty, this metric does not support OpenCL computations (the default)
    cl_flags = ""           #: OpenCL compiler flags
    cl_args = []            #: Additional user defined OpenCL arguments
    cl_argstypes = []       #: Types of additional user defined OpenCL arguments

    def __init__(self):
        self.EH = 0.0
        self.rCutoff = self.CUTOFF_FACTOR*self.EH

    def __str__(self):
        """Show human readable summary of the current setup.
        """
        res = "Coordinates: {}\n".format(self.COORDINATES)
        return res

    def X2r(self, X):
        """Convert reduced radius **X** into BL radius **r**.

        :param X: The reduced radius **X** to convert.
        """
        return np.sqrt(self.EH*self.EH + X*X/(1.0-X)**2)

    def r2X(self, r):
        """Convert BL radius **r** into reduced radius **X**.

        :param r: The BL radius **r** to convert.
        """
        xx = np.sqrt(r*r - self.EH*self.EH)
        return xx/(xx + 1.0)

    def dr_r2X(self, r):
        """Derivative dX/dr of reduced radius **X** with rrespect to BL radius **r** .

        :param r: The BL radius **r** at which to evaluate the derivative.
        """
        xx = np.sqrt(r*r - self.EH*self.EH)
        return r/(xx * (xx + 1.0)**2)

    def cl_allocate(self, context, device, commandQueue, real):
        """Called after the OpenCL propagator has allocated the **device**,
        created a **context**, and set up a **commandQueue**. The metric here can
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
        pass

    def cl_free(self):
        """Free and OpenCL resources allocated earlier by the metric."""
        pass

    def getBlackholes(self):
        """Return a list of the center point (in cartesian display coordinates)
        and radius of all black holes in the metric.
        This information is used to draw the black holes in the interactive display.
        Currently, only spherical black holes are supported. By default, a single
        black hole centered at the origin of the size of the event horizon EH
        is returned."""
        if self.EH > 0.0:
            return [((0.0, 0.0, 0.0), self.EH)]
        else:
            return []

    def setPoint(self, x):
        """Set the current point and update the components of the metric.

        :param x: The new position :math:`[x_0,x_1,x_2,x_3]` where the metric is evaluated at.
        """
        self.x = x
        return self.update()

    def toDisplayCoordinates(self, x):
        """Convert metric coordinates to cartesian display coordinates."""
        raise NameError('Must be implemented by subclass!')

    def update(self):
        """Compute the relevant components of the metric at the current point and store them in the attributes.

        :return: An error flag that is True if an error occured (most likely the ray fell into the black hole) or False otherwise.
        """
        raise NameError('Must be implemented by subclass!')

    def nullCondition(self, x):
        """Compute the null condition (i.e. :math:`1/2 g_{ij} p^i p^j`).

        :param x: Full state where to compute the null condition.
        """
        raise NameError('Must be implemented by subclass!')


class CartesianMetric(Metric):
    """Stationary, axisymmetric 4D tensor (cartesian, all contravariant)."""
    COORDINATES = "Cartesian"       #: name of the coordinates this metric uses
    LABELS = ['t', 'x', 'y', 'z', 'pt', 'px', 'py', 'pz']       # labels for each component of the coordinates

    def __init__(self):
        """Initialize all components to zero. Note that tz is missing due
        to rotational symmetry!
        """
        super(CartesianMetric, self).__init__();
        self.tt = self.tx = self.ty = self.xx = self.xy = self.xz = self.yy = self.yz = self.zz = 0.0
        self.dx_tt = self.dx_tx = self.dx_ty = self.dx_xx = self.dx_xy = self.dx_xz = self.dx_yy = self.dx_yz = self.dx_zz = 0.0
        self.dy_tt = self.dy_tx = self.dy_ty = self.dy_xx = self.dy_xy = self.dy_xz = self.dy_yy = self.dy_yz = self.dy_zz = 0.0
        self.dz_tt = self.dz_tx = self.dz_ty = self.dz_xx = self.dz_xy = self.dz_xz = self.dz_yy = self.dz_yz = self.dz_zz = 0.0

    def toDisplayCoordinates(self, x):
        """Convert metric coordinates to cartesian display coordinates."""
        return [x[0], x[1], x[2], x[3]]

    def nullCondition(self, x):
        """Compute the null condition (i.e. :math:`1/2 g_{ij} p^i p^j`).

        :param x: Full state where to compute the null condition.
        """
        self.setPoint(x[0:4])
        return 0.5*self.tt*x[4]**2 + self.tx*x[4]*x[5] + self.ty*x[4]*x[6] + 0.5*self.xx*x[5]**2 + 0.5*self.yy*x[6]**2 + 0.5*self.zz*x[7]**2 + self.xy*x[5]*x[6] + self.xz*x[5]*x[7] + self.yz*x[6]*x[7]


class SphericalMetric(Metric):
    """Stationary, axisymmetric 4D tensor (spherical, all contravariant)."""
    COORDINATES = "spherical"       #: name of the coordinates this metric uses
    LABELS = ['t', 'r', 'θ', 'φ', 'pt', 'pr', 'pθ', 'pφ' ]      # labels for each component of the coordinates

    def __init__(self):
        """Initialize all metric components to zero. Due to symmetry
        not all components and derivatives are needed.
        """
        super(SphericalMetric, self).__init__();
        self.tt = self.tp = self.rr = self.thth = self.pp = 0.0
        self.dr_tt = self.dr_tp = self.dr_rr = self.dr_thth = self.dr_pp = 0.0
        self.dth_tt = self.dth_tp = self.dth_rr = self.dth_thth = self.dth_pp = 0.0

    def __str__(self):
        """Show human readable summary of the current setup.
        """
        res = super(SphericalMetric,self).__str__();

        # Try light rings (only working for spherical metrics)
        try:
            lrs = self.findLightrings()
            if len(lrs)>0:
                res += "Lightrings:\n#\tX\tr\tη\tstability\tfull initial condition\n"
            i = 1
            for lr, stab in lrs:
                res += "{:d}\t{:.4f}\t{:.4f}\t{:.4f}\t{}\t{}\n".format(i, self.r2X(lr[1]), lr[1], -lr[7]/lr[4], "stable" if stab>0 else "unstable", lr)
                i += 1
        except:
            pass

        return res

    def toDisplayCoordinates(self, x):
        """Convert metric coordinates to cartesian display coordinates."""
        temp = np.sin(x[2])*x[1]
        return [x[0], temp*np.cos(x[3]), temp*np.sin(x[3]), np.cos(x[2])*x[1]]

    def getRadius(self, R):
        """Get the radius in BL coordinates given a circumferential radius **R**.

        :param R: The circumferential radius **R** to convert.
        """
        from scipy.optimize import newton

        def f(r):
            self.setPoint([0.0, r, np.pi/2.0, 0.0])
            g_pp = self.tt/(self.tt*self.pp-self.tp**2)
            return np.sqrt(g_pp)-R

        def df(r):
            self.setPoint([0.0, r, np.pi/2.0, 0.0])
            det = self.tt*self.pp-self.tp**2
            dr_det = self.tt*self.dr_pp+self.dr_tt*self.pp-2.0*self.tp*self.dr_tp
            g_pp = self.tt/det
            dr_g_pp = (self.dr_tt*det-dr_det*self.tt)/det**2
            return 0.5*dr_g_pp/np.sqrt(g_pp)

        sol = newton(f, R, df)
        return sol

    def determinant(self):
        """Determinant of the metric."""
        return self.rr*self.thth*(self.tt*self.pp-self.tp**2)

    def toLower(self):
        """Return the inverse metric (lower indices) as :math:`[g_{tt}, g_{rr}, g_{\\theta\\theta}, g_{\\varphi\\varphi}, g_{t\\varphi}]`."""
        det = self.tt*self.pp-self.tp**2
        g_tt = self.pp/det
        g_rr = 1.0/self.rr
        g_thth = 1.0/self.thth
        g_pp = self.tt/det
        g_tp = -self.tp/det
        return [g_tt, g_rr, g_thth, g_pp, g_tp]

    def nullCondition(self, x):
        """Compute the null condition (i.e. :math:`1/2 g_{ij} p^i p^j`).

        :param x: Full state where to compute the null condition.
        """
        self.setPoint(x[0:4])
        return 0.5*(x[4]**2*self.tt + x[5]**2*self.rr + x[6]**2*self.thth + x[7]**2*self.pp) + x[4]*x[7]*self.tp

    def getL(self, pth=0.0, pt=-1.0):
        """Get L such that potential is zero at current point with given pth and pt.

        :param pth: The value for the theta momentum pth
        :return: two possible values (L1, L2), such that :math:`\\dot{t}(L1)>\\dot{t}(L2)`
        """
        temp = np.sqrt(self.tp*self.tp*pt*pt-self.pp*(self.thth*pth*pth+self.tt*pt*pt))
        L1 = (-pt*self.tp+temp)/self.pp
        L2 = (-pt*self.tp-temp)/self.pp
        if self.tp*pt*L1>self.tp*pt*L2:
            return (L1, L2)
        else:
            return (L2, L1)

    def getNullIC(self, r, th=np.pi/2, pth=0.0, L=None, pt=-1.0, normalize=True):
        """Compute a null initial condition (position & momentum)
        E(=- **pt** ) is as specified (default -1.0), pr is computed such that everything is null.
        If **L** = None it is computed such that **pr** == 0 and :math:`\\dot{t}` is largest.

        :param r: Observer radius (BL)
        :param th: Observer theta
        :param L: Constant of motion pphi
        :param pth: Theta momentum ptheta
        :param pt: Time momentum pt
        :param normalize: Return a normalized resulting vector?
        """
        res = [0.0, r, th, 0.0,  pt, 0.0, pth, L]
        self.setPoint(res)
        if L is None:
            L = self.getL(pth, pt)[0]
            res[7] = L
        res[5] = np.sqrt(-(self.tt*pt*pt+2.0*self.tp*L*pt+self.pp*L*L+self.thth*pth*pth)/self.rr)
        if normalize:
            fact = 1.0/np.sqrt(1.0+res[5]*res[5]+res[6]*res[6]+res[7]*res[7])
            res[4] = res[4]*fact
            res[5] = res[5]*fact
            res[6] = res[6]*fact
            res[7] = res[7]*fact
        return res

    def potential(self, L=0, pt=-1.0, pth=0):
        """Obtain the potential function at the current point evaluated for **L**,
        **pt** and **pth** as given. This corresponds to the potential W defined by:

        .. math::
            W = g^{ab}*p_a*p_b - g^{rr}*p_r*p_r

        and for **pth** == 0 this becomes the usual potential

        .. math::
            V = g^{ab}*p_a*p_b - g^{rr}*p_r*p_r - g^{\\theta\\theta}*p_{\\theta}*p_{\\theta}

        :param L: The value for the constant of motion pphi = **L**
        :param pt: The value for the constant of motion **pt** = -E
        :param pth: The value for the theta momentum **pth**
        """
        return self.tt*pt*pt+2.0*self.tp*L*pt+self.pp*L*L+self.thth*pth*pth

    def dr_potential(self, L=0, pt=-1.0, pth=0):
        """Derivative of the potential with respect to **r**. See :meth:`potential`.

        :param L: The value for the constant of motion pphi = **L**
        :param pt: The value for the constant of motion **pt** = -E
        :param pth: The value for the theta momentum **pth**
        """
        return self.dr_tt*pt*pt+2.0*self.dr_tp*L*pt+self.dr_pp*L*L+self.dr_thth*pth*pth

    def dth_potential(self, L=0, pt=-1.0, pth=0):
        """Derivative of the potential with respect to theta. See :meth:`potential`.

        :param L: The value for the constant of motion pphi = **L**
        :param pt: The value for the constant of motion **pt** = -E
        :param pth: The value for the theta momentum **pth**
        """
        return self.dth_tt*pt*pt+2.0*self.dth_tp*L*pt+self.dth_pp*L*L+self.dth_thth*pth*pth

    def h(self):
        """Obtain the h+- function at the current point.

        :return: A tuple with the values of h+ and h- at the current point.
        """
        sqrtD = np.sqrt(self.tp*self.tp-self.tt*self.pp)
        hp = (self.tp - sqrtD)/self.pp      # plus and minus are flipped because we use the contravariant metric!
        hm = (self.tp + sqrtD)/self.pp
        return (hp, hm)

    def dr_h(self):
        """Obtain the r derivative of the h+- function at the current point.

        :return: A tuple with the values of d/dr h+ and d/dr h- at the current point.
        """
        sqrtD = np.sqrt(self.tp*self.tp-self.tt*self.pp)
        dr_D = 2.0*self.tp*self.dr_tp-self.tt*self.dr_pp-self.dr_tt*self.pp
        dr_hp = (self.dr_tp - 0.5*dr_D/sqrtD)/self.pp - self.dr_pp*(self.tp - sqrtD)/(self.pp*self.pp)
        dr_hm = (self.dr_tp + 0.5*dr_D/sqrtD)/self.pp - self.dr_pp*(self.tp + sqrtD)/(self.pp*self.pp)
        return (dr_hp, dr_hm)

    def dth_h(self):
        """Obtain the theta derivative of the h+- function at the current point.

        :return: A tuple with the values of d/dtheta h+ and d/dtheta h- at the current point.
        """
        sqrtD = np.sqrt(self.tp*self.tp-self.tt*self.pp)
        dth_D = 2.0*self.tp*self.dth_tp-self.tt*self.dth_pp-self.dth_tt*self.pp
        dth_hp = (self.dth_tp - 0.5*dth_D/sqrtD)/self.pp - self.dth_pp*(self.tp - sqrtD)/(self.pp*self.pp)
        dth_hm = (self.dth_tp + 0.5*dth_D/sqrtD)/self.pp - self.dth_pp*(self.tp + sqrtD)/(self.pp*self.pp)
        return (dth_hp, dth_hm)

    def hinv(self):
        """Obtain 1/h+- at the current point. This is used instead of h to find roots of

        :return: A tuple with the values of 1/h+ and 1/h- at the current point.
        """
        sqrtD = np.sqrt(self.tp*self.tp-self.tt*self.pp)
        hp = self.pp/(self.tp - sqrtD)
        hm = self.pp/(self.tp + sqrtD)
        return (hp, hm)

    def dr_hinv(self):
        """Obtain d/dr 1/h+- at the current point.

        :return: A tuple with the values of d/dr 1/h+ and d/dr 1/h- at the current point.
        """
        sqrtD = np.sqrt(self.tp*self.tp-self.tt*self.pp)
        dr_D = 2.0*self.tp*self.dr_tp-self.tt*self.dr_pp-self.dr_tt*self.pp
        dr_hp = self.dr_pp/(self.tp - sqrtD) - self.pp*(self.dr_tp - 0.5*dr_D/sqrtD)/(self.tp - sqrtD)**2
        dr_hm = self.dr_pp/(self.tp + sqrtD) - self.pp*(self.dr_tp + 0.5*dr_D/sqrtD)/(self.tp + sqrtD)**2
        return (dr_hp, dr_hm)

    def dth_hinv(self):
        """Obtain d/dr 1/h+- at the current point.

        :return: A tuple with the values of d/dr 1/h+ and d/dr 1/h- at the current point.
        """
        sqrtD = np.sqrt(self.tp*self.tp-self.tt*self.pp)
        dth_D = 2.0*self.tp*self.dth_tp-self.tt*self.dth_pp-self.dth_tt*self.pp
        dth_hp = self.dth_pp/(self.tp - sqrtD) - self.pp*(self.dth_tp - 0.5*dth_D/sqrtD)/(self.tp - sqrtD)**2
        dth_hm = self.dth_pp/(self.tp + sqrtD) - self.pp*(self.dth_tp + 0.5*dth_D/sqrtD)/(self.tp + sqrtD)**2
        return (dth_hp, dth_hm)

    def findLightrings(self):
        """Find all light rings, that is all circular orbits in the equatorial plane.
        This is characterized by potential(r)=0 and dr_potential(r)=0.
        This condition is equivalent to eta=h+-(r) and dr_h+-(r)=0.
        As h is not always a continuous function, we use 1/h=hinv which is always smooth to perform the computations.

        :returns: A list of tuples of complete initial conditions of the
            circular closed orbit in the equatorial plane, and either +1 if the
            orbit is stable and -1 if the orbit is unstable.
        """
        def func(r, i):
            # function returning d/dr 1/h+ or d/dr 1/h-
            self.setPoint([0, r, np.pi/2, 0])
            return self.dr_hinv()[i]

        # sample 1/h+- along r. Using a uniform grid in x so that it is denser near the black hole
        x = np.linspace(self.r2X(max(1e-6, 1.001*self.rCutoff)), 0.99, 1000)
        r = self.X2r(x)
        th = np.full_like(r, np.pi/2)
        self.setPoint([0, r, th, 0])

        res = []
        for i, dr_hinv in enumerate(self.dr_hinv()):
            # find the intervals where there was a sign change
            idx = np.nonzero(dr_hinv[0:-1]*dr_hinv[1:] <= 0.0)[0]
            for j in idx:
                # now perform a search for the root in each interval
                try:
                    r0 = brentq(func, r[j], r[j+1], args=(i))
                except:
                    continue
                # assemble the initial condition and determine stability
                self.setPoint([0, r0, np.pi/2, 0])
                sign = np.sign(dr_hinv[j+1]-dr_hinv[j])     # sign of the derivative of dr_hinv (- sign of dr2_h)
                stab = -((-1)**i)*sign                      # the sign of V'' changes with h+-
                pt = -1.0
                if -self.pp > 0.0 and i == 0:     # XXX: this is currently making assumptions on D<0
                    pt = 1.0                                #: only h+ in the ergo region has negative energy (g_ttg^pp)
                h = self.h()
                L = -h[i]*pt
                res.append(([0.0, r0, np.pi/2, 0.0,  pt, 0.0, 0.0, L], stab))

        return res
