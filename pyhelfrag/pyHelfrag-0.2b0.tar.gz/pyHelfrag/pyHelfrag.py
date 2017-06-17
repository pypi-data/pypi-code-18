from __future__ import print_function

import random
from math import *
import numpy as np
from scipy.integrate import ode
import pylab as plt
from constants import *
from modeode import *
from _registry import *
from utilities import *
import pandas as pd
from scipy.constants import Avogadro

from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
from plotly.graph_objs import Scatter, Figure, Layout, XAxis, YAxis
import plotly.tools as tls
from rdaam import _rdaam_diffusivities, _get_sum_density

if __IPYTHON__:
    init_notebook_mode(connected=True)


class GrainList(list):

    def __init__(self):

        self._data = None
        self._cooker = []

        return

    def show(self):

        for grain in self:
            print(grain.length)

    def Plot_ADFD(self, **kwargs):
        ages = []
        lengths = []
        for grain in self:
            ages.append(grain.HeAge)
            lengths.append(grain.length)

        fig = plt.figure()
        ax = plt.subplot(111)
        ax.plot(lengths,  ages, "o", **kwargs)
        ax.set_xlabel("Grain Length")
        ax.set_ylabel("Age")
        ax.set_title("ADFD plot")
        if __IPYTHON__:
            plotly_fig = tls.mpl_to_plotly(fig)
            iplot(plotly_fig)
        else:
            plt.show()
        
        return ax

    @property
    def data(self):
        return self._data

    @data.getter
    def data(self):
        radii = pd.Series([grain.radius for grain in self])
        lengths = pd.Series([grain.length for grain in self])
        widths = pd.Series([grain.diameter for grain in self])
        uranium = pd.Series([grain.Uppm for grain in self])
        thorium = pd.Series([grain.Thppm for grain in self])
        D0s = pd.Series([grain.D0 for grain in self])
        Eas = pd.Series([grain.Ea for grain in self])
        Ages = pd.Series([grain.HeAge for grain in self])
       
        d = {"Length": lengths,
             "Radius": radii,
             "Width": widths,
             "D0": D0s,
             "EA": Eas,
             "U (ppm)": uranium,
             "Th (ppm)": thorium}

        if Ages.size:
            d["U-Th/He Age"] = Ages

        self._data = pd.DataFrame(d)
        return self._data

    @property
    def cooker(self):
        return self._cooker

    @cooker.setter
    def cooker(self, cooker):
        for grain in self:
            grain.cooker = cooker
            self._cooker.append(cooker)
        return self._cooker

    def bake(self):
        for grain in self:
            grain.bake()

class FragmentList(GrainList):

    def __init__(self):

        return

class Sample(object):
    def __init__(self, name="Sample"):
        self.name = "Sample"
        self.location = "loc"

class Grain(Sample):

    density = ap_density

    # Half stopping distances of radiogenic isotopes
    z238 = S238/2.0
    z235 = S235/2.0
    z232 = S232/2.0

    def __init__(self, length, radius=None, diameter=None, Ea=138e3,
                 D0=0.00316, U=20.0, Th=20.0, Eu=None, ThUR=None,
                 lr=None, Units="ppm", label=None,
                 Nr=30, kineticK="ETCHPIT LENGTH", kineticPar=1.65):
        """
        Create a Grain (Apatite) assuming a cylindrical shape.

        Keyword arguments:
        length   -- length of the cylinder in microns (must be specified)
                    It can be specified as a single value or as a range
                    (Min, Max). If the latter is used, the length is randomly
                    picked within the range.
        radius   -- radius of the cylinder in microns(default is None)
                    Can be a range (see length)
        diameter -- diameter of the cylinder in microns (default is None)
                    Can be a range (see length)
        Ea       -- Energy of Activation (default 138e3 kilojoules)
                    Can be a range (see length)
        D0       -- Diffusivity at infinite temperature (default 0.00316 cm**2/s)
                    Can be a range (see length)
        U        -- Uranium Content (default 20ppm)
                    Can be a range (see length)
        Th       -- Uranium Content (default 20ppm)
                    Can be a range (see length)
        Eu       -- Effective Uranium Content (default is None)
                    Can be a range (see length)
        ThUR     -- Thorium / Uranium ratio (default is None)
                    Can be a range (see length)
        lr       -- Length / Radius ratio (default is None)
        label    -- Some label for the grain (default is None)
        Nr       -- Number of Modes used in the diffusion equation (default is 30)
        kineticK -- Kinetic Parameter, options are:
                    "ETCHPIT LENGTH",
                    "CL_WT_PCT",
                    "L_PFU",
                    "OH_PFU"
                    (default is "ETCHPIT LENGTH")
        kineticPar -- Kinetic Parameter value (default is 1.65 microns)
        """

        if(Eu and (U or Th)):
            return print("Error: You can not enter both Eu and U or Th content")
        if(radius and diameter):
            return print("Error: Enter either radius OR diameter")
        if(Eu and not ThUR):
            return print("Error: Enter ThUR please!")

        if(label):
            self.label = label
        else:
            self.label = None

        self.length = self.__GetVal(length)

        if radius:
            self.radius = self.__GetVal(radius)
            self.diameter = self.radius * 2.0
        if diameter:
            self.diameter = self.__GetVal(diameter)
            self.radius = diameter / 2.0

        self.lr = self.length / self.radius

        self.Ea = self.__GetVal(Ea)
        self.D0 = self.__GetVal(D0)

        self.volume = pi * self.radius**2 * self.length
        self.surface = 2.0 * pi * self.radius * self.length + 2 * pi * self.radius**2
        self.mass = self.volume * self.density
        self.Eradius = ((self.length * self.radius) / (2.0 * (self.length + self.radius)))*3

        # Calculate non-dimensional values
        self.NDradius = self.radius / self.radius
        self.NDEradius = self.Eradius / self.radius
        self.NDlength = self.length / self.radius
        self.l = self.NDlength
        self.NDdiameter = self.diameter / self.radius
        self.NDz238 = self.z238 / self.radius
        self.NDz235 = self.z235 / self.radius
        self.NDz232 = self.z232 / self.radius

        if(Eu and Units == "ppm"):
            self.Euppm = self.__GetVal(Eu)
            self.ThUR = self.__GetVal(ThUR)
            self.Uppm = self.Euppm / (1.0 + 0.24*self.ThUR)
            self.Thppm = self.Thppm*self.ThR
        
        if(U and Units == "ppm"):
            self.Uppm = self.__GetVal(U)
            self.Thppm = self.__GetVal(Th)
            self.ThUR = self.Thppm / self.Uppm
            self.Euppm = self.Uppm * (1.0 + 0.24*self.ThUR)
        
        self.U238ppm = self.Uppm / (unatrt + 1.0)
        self.U235ppm = self.Uppm - self.U238ppm
        self.U238molesm3 = ppm2molesm3(self.U238ppm, U238_ATOM_MASS)
        self.U235molesm3 = ppm2molesm3(self.U235ppm, U235_ATOM_MASS)

        self.Th232ppm = self.Thppm / (tnatrt + 1.0)
        self.Th230ppm = self.Thppm - self.Th232ppm
        self.Th232molesm3 = ppm2molesm3(self.Th232ppm, TH232_ATOM_MASS)
        self.Th230molesm3 = ppm2molesm3(self.Th230ppm, TH230_ATOM_MASS)
        
        self.C_238 = C_238 = self.U238molesm3
        self.C_235 = C_235 = self.U235molesm3
        self.C_232 = C_232 = self.Th232molesm3
        self.mean_radiogenic = (C_238 + C_235 + C_232) / 3.0

        self.Nr = Nr
        self.Nz = int(ceil(self.Nr*self.NDlength))

        self._cooker = None
        self._Csol = None
        self._CylAmount = None
        self._Conc_sol = None
        self.RadialProfile = None
        self.LongitudinalProfile = None
        self._data = None
        self.HeAge = 0.
        self.kineticK = kineticK
        self.kineticPar = kineticPar
        self._RDAAM = None

    @property
    def cooker(self):
        return self._cooker

    @cooker.setter
    def cooker(self, obj):
        self._cooker = obj
       
        if obj.alpha:
            self.d_i = np.array([self.NDz238, self.NDz235, self.NDz232])
        
        ndt = len(obj.tau)
        tf = obj.tf
        
        self.C0 = np.zeros((self.Nr,self.Nz))
        self._Csol = np.zeros((self.Nr,self.Nz,ndt))
        
        self.U238ppm = Get238fromUcontent(self.Uppm, tf)
        self.U235ppm = Get235fromUcontent(self.Uppm, tf)
        self.U238molesm3 = ppm2molesm3(self.U238ppm, U238_ATOM_MASS)
        self.U235molesm3 = ppm2molesm3(self.U235ppm, U235_ATOM_MASS)

        self.Th232ppm = Get232fromThcontent(self.Thppm, tf)
        self.Th230ppm = Get230fromThcontent(self.Thppm, tf)
        self.Th232molesm3 = ppm2molesm3(self.Th232ppm, TH232_ATOM_MASS)
        self.Th230molesm3 = ppm2molesm3(self.Th230ppm, TH230_ATOM_MASS)
        
        self.C_238 = C_238 = GetU238atTime(self.U238molesm3, tf)
        self.C_235 = C_235 = GetU235atTime(self.U235molesm3, tf)
        self.C_232 = C_232 = GetTH232atTime(self.Th232molesm3, tf)
        self.mean_radiogenic = (C_238 + C_235 + C_232) / 3.0
        self.cif = np.array([C_238, C_235, C_232])
        self.cif /= self.mean_radiogenic

    @property
    def RDAAM(self):
        return self._RDAAM

    @RDAAM.setter
    def RDAAM(self, Model):

        if Model not in ["FLOWERS", "GAUTHERON"]:
            raise  ValueError("Could not find Model")

        if self._cooker == None:
            raise  ValueError("No Cooker Found")

        self._RDAAM = Model
        self._EAs, FineTime, FineTemp = self._rdaam_Eas()
        self._FineTime = FineTime / (1e6 * yr)
        self._FineTemp = FineTemp

    def bake(self):
        
        if self.cooker.cylinder:
            self._Csol = self.cooker._get_modes_cylinder(self)
            self._CylAmount = self.cooker._get_amount_cylinder(self)
            self.HeAge = self._get_cylinder_age()
        return

    def _get_Ea(self, t):
        if self.RDAAM != None:
            return np.interp(t, self._FineTime, self._EAs, left=self._EAs[0],
                    right=self._EAs[-1])
        else:
            return self.Ea

    def _get_beta(self, t):
        EA = self._get_Ea(t)
        D0 = self.D0

        if self.cooker.cylinder:
            R = self.radius*1.e-6
        else:
            R = self.Eradius*1.e-6
        
        return exp(log(tau_e * D0 / R**2) - EA / (RGAS * self.cooker.history.TMAX))
    
    def _get_gamma(self, t):
        EA = self._get_Ea(t)
        return self.cooker.history.dT * EA / (RGAS * self.cooker.history.TMAX**2)

    def _rdaam_Eas(self):
        sumDensityArray, FineTime, FineTemp = _get_sum_density(self.cooker.history,
                                                     self.kineticPar, self.kineticK)
        diffusivitiesArray = _rdaam_diffusivities(self.RDAAM, FineTime,
                                                  FineTemp, self.U238ppm,
                                                  self.U235ppm, self.Th232ppm,
                                                  sumDensityArray)


        self._sumDensityArray = sumDensityArray
        self._diffusivitiesArray = diffusivitiesArray
        EAsArray = -1.0 * np.log((diffusivitiesArray * 1e-4) / self.D0) * RGAS * FineTemp
        return EAsArray, FineTime, FineTemp

    @staticmethod
    def __GetVal(val, step=1):
        if(isinstance(val,tuple)):
            return random.choice(range(val[0], val[1], step))
        else:
            return val

    def SetGrainHeAge(self,Age):
        self.HeAge = Age

    def breakGrain(self, T0=None, T1=None, reinitialise=True):

        if reinitialise:
            self.fragments = FragmentList()

        for i in range(T1):
            start = 0.0
            end = np.random.uniform(40.0, self.length) 
            self.fragments.append(Fragment(int(start), int(end), self))
        for i in range(T0):
            start = np.random.uniform(0.0, self.length - 40.0) 
            end = np.random.uniform(start + 40.0, self.length)
            self.fragments.append(Fragment(int(start), int(end), self))
   
        return self.fragments

    def _get_diffusion_profile_cylinder(self):
        
        R = np.linspace(-1, 1, int(self.radius))
        Z = np.linspace(0, self.l, int(self.length))
        
        Conc_sol = np.zeros((R.size, Z.size))
        
        Nr, Nz = self.Nr, self.Nz
        C_sol = self._Csol

        l = self.l

        for I in range(R.size):
            for m in range(1, Nr+1):
                for n in range(1, Nz+1):
                    Conc_sol[I, int(Z.size/2)] += (C_sol[m-1,n-1,-1]*BesJ0(ALPHA[m-1]*R[I])*
                                                     sin(n*pi*Z[int(Z.size/2)]/l))
        
        Conc_sol[int(R.size/2), :] = 0.
        for J in range(Z.size):
            for m in range(1, Nr+1):
                for n in range(1, Nz+1):
                   Conc_sol[int(R.size/2), J] += (C_sol[m-1,n-1,-1]
                                                   *BesJ0(ALPHA[m-1]*R[int(R.size/2)])*sin(n*pi*Z[J]/l))

        self._Conc_sol  = Conc_sol

        self.RadialProfile = Conc_sol[:, int(Z.size/2)]
        self.LongitudinalProfile = Conc_sol[int(R.size/2), :]

        return self.RadialProfile, self.LongitudinalProfile, self._Conc_sol
    
    def _get_cylinder_age(self):

        He = (self._CylAmount * self.mean_radiogenic) / (pi * self.l)
        HeAge = GetHeliumAgeMD2005(He, self.U238molesm3,
                                       self.U235molesm3, 
                                       self.Th232molesm3,
                                       self.Th230molesm3)
        return HeAge
    
    def PlotRadialProfile(self):
        self.RadialProfile, self.LongitudinalProfile, _ = self._get_diffusion_profile_cylinder() 
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self.RadialProfile)
        if __IPYTHON__:
            plotly_fig = tls.mpl_to_plotly(fig)
            iplot(plotly_fig)
        else:
            plt.show()
        return ax
    
    def PlotLongitudinalProfile(self):
        self.RadialProfile, self.LongitudinalProfile, _ = self._get_diffusion_profile_cylinder() 
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(self.LongitudinalProfile)
        if __IPYTHON__:
            plotly_fig = tls.mpl_to_plotly(fig)
            iplot(plotly_fig)
        else:
            plt.show()
        return ax

    @property
    def data(self):
        return self._data

    @data.getter
    def data(self):
        vals = [self.length,
                self.radius,
                self.diameter,
                self.Eradius,
                self.Uppm,
                self.Thppm,
                self.Euppm,
                self.Ea,
                self.D0]
        indices = ["Length (microns)", 
                   "Radius (microns)",
                   "Diameter (microns)",
                   "Equiv. Radius (microns)", 
                   "[U] (ppm)",
                   "[Th] (ppm)",
                   "[eU] (ppm)",
                   "Ea (kj)",
                   "D0 (cm^2/s)"]

        if self.HeAge:
            vals.append(self.HeAge)
            indices.append("U-Th/He Age")

        d = pd.Series(vals, indices)
        self._data = pd.DataFrame({self.label:d})
        return self._data

class Fragment(Grain):
    
    def __init__(self, start, end, parent=None, length=None, radius=None):
       

        if parent != None:
            self.radius = parent.radius
            self.diameter = parent.diameter
            self.Uppm = parent.Uppm
            self.Thppm = parent.Thppm
            self.D0 = parent.D0
            self.Ea = parent.Ea
            self.l0 = parent.length
        else:
            if length != None and radius != None:
                super(Fragment, self).__init__(length, radius)
                self.l0 = self.length
       
        self.fragstart = start
        self.fragend = end
        self.length = end - start
        self.age = None
        self.l = self.length / self.radius
       
        if(start == 0.0):
            self.fragnterm = 1
        if(start != 0.0 and end == 1.0):
            self.fragnterm = 1
        if(start != 0.0 and end != 1.0):
            self.fragnterm = 0
        if(start == 0.0 and end == 1.0):
            self.fragnterm = 2
       
        if parent != None:
            #for prop in parent.__dict__.keys():
            #    self.__dict__[prop] = parent.__dict__[prop]
            
            self.U238molesm3   = parent.U238molesm3    
            self.U235molesm3   = parent.U235molesm3
            self.Th232molesm3  = parent.Th232molesm3 
            self.Th230molesm3  = parent.Th230molesm3 
            self.mean_radiogenic = parent.mean_radiogenic
            self.HeAge = 0.

            if parent._CylAmount:
                f = parent._cooker._get_amount_cylinder_section
                self._CylAmount = f(parent, start/parent.radius, end/parent.radius) 
                self.HeAge = self._get_cylinder_age()

        self._data = None

        return

    @property
    def data(self):
        return self._data

    @data.getter
    def data(self):
        self._data = super(Fragment, self).data
        vals = [self.fragnterm,
                self.l0]
        indices = ["T", 
                   "l0 (microns)"]
        d = pd.Series(vals, indices)
        self._data.append(d, ignore_index=True)
        return self._data

def GenerateListOfGrains(N, length, Ea=138000, D0=0.00316, radius=None, diameter=None, U=None,
                 Th=None, Eu=None, ThUR=None, lr=None, Units="ppm", label=None):
    """
    Create a  List of Grain (Apatite) assuming a cylindrical shape.

    Keyword arguments:
    N        -- Number of Grain to generate.
    length   -- length of the cylinder in microns (must be specified)
                It can be specified as a single value or as a range
                (Min, Max). If the latter is used, the length is randomly
                picked within the range.
    radius   -- radius of the cylinder in microns(default is None)
                Can be a range (see length)
    diameter -- diameter of the cylinder in microns (default is None)
                Can be a range (see length)
    Ea       -- Energy of Activation (default 138e3 kilojoules)
                Can be a range (see length)
    D0       -- Diffusivity at infinite temperature (default 0.00316 cm**2/s)
                Can be a range (see length)
    U        -- Uranium Content (default 20ppm)
                Can be a range (see length)
    Th       -- Uranium Content (default 20ppm)
                Can be a range (see length)
    Eu       -- Effective Uranium Content (default is None)
                Can be a range (see length)
    ThUR     -- Thorium / Uranium ratio (default is None)
                Can be a range (see length)
    lr       -- Length / Radius ratio (default is None)
    label    -- Some label for the grain (default is None)
    Nr       -- Number of Modes used in the diffusion equation (default is 30)
    kineticK -- Kinetic Parameter, options are:
                "ETCHPIT LENGTH",
                "CL_WT_PCT",
                "L_PFU",
                "OH_PFU"
                (default is "ETCHPIT LENGTH")
    kineticPar -- Kinetic Parameter value (default is 1.65 microns)
    """
    
    grainlist = GrainList()
    for i in range(N):
        grain = Grain(length=length, Ea=Ea, D0=D0, radius=radius, diameter=diameter, U=U,
                 Th=Th, Eu=Eu, ThUR=ThUR, lr=lr, Units=Units, label=label)
        grainlist.append(grain)

    return grainlist
