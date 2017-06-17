from __future__ import print_function

import random
from math import *
import numpy as np
from scipy.integrate import ode, odeint
import pylab as plt
from .constants import *
from .modeode import *
#from _registry import *
from .utilities import *
from tqdm import tqdm


class Cooker(object):

    def __init__(self, history, geometry="CYLINDER", alpha=True, Nr=30,
                 integrator="lsodaOdeint"):

        self.history = history
        self.alpha = True

        # Prepare the geometry
        if geometry == "CYLINDER":
            self.cylinder = True
        
        # Prepare the integrator and its arguments
        self.integrator = integrator
        if self.integrator == "lsodaOdeint":
            integrator_args = lsoda_defaults
        if self.integrator == "lsoda":
            integrator_args = lsoda_defaults
        if self.integrator == "dopri5":
            integrator_args = dopri5_defaults
        if self.integrator == "vode":
            integrator_args = vode_defaults
        if self.integrator == "zvode":
            integrator_args = zvode_defaults
        if self.integrator == "dop853":
            integrator_args = dop853_defaults

        if self.integrator != "lsodaOdeint":
            self.modeode = cylinderModeOde
            self._get_modes_cylinder = self._get_modes_cylinderOde
            self._r = ode(self.modeode)
            self._r = self._r.set_integrator(self.integrator, **integrator_args)
        else:
            self.modeode = cylinderModeOdeint
            self._get_modes_cylinder = self._get_modes_cylinderOdeint
        
        # create interpolate function 
        self._interpolateTemp = self.history.getTemp
    
        self.delta = self._get_delta()
        self.tau = self.history.t
        self.theta = self.history.NDT
        self.tf = self.history.tf
        
        self.lbda = 1e6 * np.array([U238_DECAYCT, U235_DECAYCT, TH232_DECAYCT])
        
    def _get_delta(self):
        return self.history.dT / self.history.TMAX

    def _get_modes_cylinderOde(self, grain):

        self.C0 = C0 = np.zeros((grain.Nr, grain.Nz))
        C_sol = np.zeros((grain.Nr, grain.Nz, self.tau.size))
        C_sol[:,:,0] = C0

        for m in range(1,grain.Nr+1):
            for n in range(1,grain.Nz+1):
                self._r.set_initial_value(C0[m-1, n-1]).set_f_params(n, m, self, grain)
                step = 1
                while self._r.successful() and self._r.t < self.tf:
                    dt = self.tau[step] - self._r.t
                    intTime = self._r.t + dt
                    out = self._r.integrate(intTime)
                    if self._r.successful():
                        C_sol[m-1, n-1, step] = out 
                        step += 1

        return C_sol
    
    def _get_modes_cylinderOdeint(self, grain):

        self.C0 = C0 = np.zeros((grain.Nr, grain.Nz))
        C_sol = np.zeros((grain.Nr, grain.Nz, self.tau.size))
        C_sol[:,:,0] = C0

        for m in tqdm(range(1,grain.Nr+1), desc="Grain"):
            for n in range(1,grain.Nz+1):
                out = odeint(self.modeode, C0[m-1, n-1], self.tau,
                                     args=(n, m, self, grain),
                                     mxstep = 2000, **lsoda_defaults)
                C_sol[m-1, n-1, :] = out.flatten()

        return C_sol

    def _get_modes_sphere(self):
    
        self.C0 = C0 = np.zeros((self.Nr,))
        C_sol = np.zeros((self.Nr, self.tau.size))
        C_sol[:,0] = C0
        
        for n in range(1,Nr+1):
            self._r.set_initial_value(C0[n-1]).set_f_params(n, self)
            step = 1
            while self._r.successful() and self._r.t < self.tf:
                dt = self.tau[step] - self._r.t
                intTime = self._r.t + dt
                out = self._r.integrate(intTime)
                C_sol[n-1, step] = out 
                step += 1

        self._Csol = C_sol

    def _get_amount_cylinder(self, grain):
        return self._get_amount_cylinder_section(grain, 0, grain.NDlength)

    def _get_amount_cylinder_section(self, grain, z1, z2):
        """ Given mode weights contained in Cm and a cylinder of length l
            calculate the amount of C contained in a section of cylinder from
            z1 to z2.
        """
        l = grain.NDlength
        Cm = grain._Csol[:,:,-1]

        amount = 0.
        for m in range(1, grain.Nr+1):
            for n in range(1, grain.Nz+1):
                amount += 2.*Cm[m-1,n-1]*BesJ1(ALPHA[m-1])*l*(cos(pi*z1*n/l)-cos(pi*z2*n/l))/(n*ALPHA[m-1])
        
        return amount
    
    def _get_amount_sphere(self,r1,r2):
       
        if self._Csol is None:
            self._get_modes_sphere()
        
        Cm = self._Csol[:,:,-1]
        
        amount = 0.
        for n in range(1,self.Nr+1):
            amount += (amount + (Cm[n-1]/(n**2*pi**2))*(sin(n*pi*r2) - 
                       sin(n*pi*r1)-n*pi*r2*cos(n*pi*r2)+n*pi*r1*cos(n*pi*r1)))
        self.amount = amount
        return self.amount

    def getDiffusionMap(self):
        
        R = np.linspace(-1, 1, int(self.grain.radius))
        Z = np.linspace(0, self.l, int(self.grain.length))
        
        Conc_sol = np.zeros((R.size, Z.size))
        
        Nr, Nz = self.Nr, self.Nz
        C_sol = self._Csol

        l = self.l

        for I in range(R.size):
            for J in range(Z.size):
                for m in range(1, Nr+1):
                    for n in range(1, Nz+1):
                        Conc_sol[I, J] += (C_sol[m-1,n-1,-1]*BesJ0(ALPHA[m-1]*R[I])*
                                                     sin(n*pi*Z[J]/l))
        
        self.Conc_sol  = Conc_sol
        
        return self.Conc_sol



