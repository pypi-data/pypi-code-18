import numpy as np
from .parameters import MAXCOUNT
from .utilities import drawbinom
from .utilities import draw_from_distrib
import pylab as plt
import random
import math
from ctypes import *
import os
import glob

_ROOT = os.path.abspath(os.path.dirname(__file__))

# This is a workaround to locate the shared library file.
# File name is attributed at compile time.
_KETCHAM_ = glob.glob(_ROOT+"/../ketcham*")
_KETCHAM_ = [val for val in _KETCHAM_ if ".py" not in val][0]

class Sample(object):

    def __init__(self, name, counts=[], AFT=None, AFT_error=None,
                 tls=[], zeta=None, rhod=None):
        self.name = name
        self.counts = counts
        self.nc = len(counts)

        if counts:
            #self.ns, self.ni = [*zip(counts)]
            self.ns, self.ni = list(zip(counts))
        
        self.AFT = AFT
        self.AFT_error = AFT_error
        self.tls = tls
        self.zeta = zeta
        self.rhod = rhod

    def write_mtx_file(self, filename):
        write_mtx_file(filename, self.name, self.AFT, self.AFT_error, self.tls,
                       self.ns, self.ni, self.zeta, self.rhod)

class Synthetic(Sample):

    def __init__(self, name=None, nc=30, ntl=100, history=None):
        Sample.__init__(self, name=name)
        if not self.name:
            self.name = "Synthetic"
        if not self.zeta:
            self.zeta = 323.
        if not self.rhod:
            self.rhod = 1.e6
        self.nc = nc
        self.ntl = ntl
        self.history = history
        if history:
            self.ketcham_model()
            self.synthetic_counts()
            # Add noise
            self.synthetic_lengths()
            # Add noise


    def ketcham_model(self, alo=16.3):
        """Return Apatite Fission Track Age (AFTA) and Track Length
        distribution using Ketcham et al. 1999 annealing model.
       
        Parameter:
        ---------
        alo -- Initial track length
        """
        data = KetchamModel(self.history, alo=alo)
        # Process Fission Track Distribution
        # distribution range from 0 to 20 microns
        # We have 200 values.
        vals, fdist = data["Fission Track length distribution"]
        probs = [i for i in fdist]
        
        self.AFT = data["Final Age"]
        self.AFT_error = self.AFT*0.05
        self.Oldest_Age = data["Oldest Age"]
        self.MTL = data["Mean Track Length"]
        self.TLD = fdist  
        self.reDensity = data["redDensity"]
        self.rho = self.reDensity
        self.bins = vals
        return

    def synthetic_counts(self):
        data = generate_synthetic_counts(self.rho, self.nc)
        self.ns = data["Spontaneous tracks (Ns)"]
        self.ni = data["Induced tracks (Ni)"]
        #self.counts=[*zip(self.ns, self.ni)]
        self.counts=list(zip(self.ns, self.ni))
        return

    def synthetic_lengths(self):
        self.tls = draw_from_distrib(self.bins, self.TLD, self.ntl)
        self.mtl = (float(sum(self.tls))/len(self.tls) 
                    if len(self.tls) > 0 else float('nan'))
        self.mtl_sd = np.std(self.tls)

    def plot_predicted_TLD(self):
        plt.plot(self.bins, self.TLD)
        plt.xlabel("Length (microns)")
        plt.ylabel("Density")
    
    def plot_history(self):
        t = self.history.time
        T = self.history.Temperature
        plt.plot(t, T)
        plt.ylim((max(T)+10, min(T)-10))
        plt.xlim((max(t), min(t)))
        plt.xlabel("time (Ma)")
        plt.ylabel("Temperature (Celcius)")

    def plot_track_histogram(self):
        plt.hist(self.tls)
        plt.xlim(0,20)
        plt.xlabel("Length (microns)")
        plt.ylabel("counts")

def write_mtx_file(filename, sample_name, FTage, FTage_error, TL, NS, NI,
                    zeta, rhod):

    f = open(filename, "w")
    f.write("{name:s}\n".format(name=sample_name))
    f.write("{value:s}\n".format(value=str(-999)))
    f.write("{nconstraints:d} {ntl:d} {nc:d} {zeta:5.1f} {rhod:12.1f} {totco:d}\n".format(
             nconstraints=0, ntl=len(TL), nc=NS.size, zeta=zeta, rhod=rhod,
            totco=2000))
    f.write("{age:5.1f} {age_error:5.1f}\n".format(age=FTage,
                                                   age_error=FTage_error))
    TLmean = (float(sum(TL))/len(TL) if len(TL) > 0 else float('nan'))
    TLmean_sd = np.std(TL)
    
    f.write("{mtl:5.1f} {mtl_error:5.1f}\n".format(mtl=TLmean,
                                                   mtl_error=TLmean*0.05))
    f.write("{mtl_std:5.1f} {mtl_std_error:5.1f}\n".format(mtl_std=TLmean_sd,
                                                           mtl_std_error=TLmean_sd*0.05))
    for i in range(NS.size):
        f.write("{ns:d} {ni:d}\n".format(ns=NS[i], ni=NI[i]))

    for track in TL:
        f.write("{tl:4.1f}\n".format(tl=track))

    f.close()
    return 0

def generate_synthetic_counts(rho, Nc=30):
    """Generate Synthetic AFT data.

    Parameters:
    rho : track density
    Nc : Number of crystals

    """
    # Probability in binomial distribution
    prob = rho / (1. + rho)

    # For Nc crystals, generate synthetic Ns and Ni count data using binomial
    # distribution, conditional on total counts Ns + Ni, sampled randomly with
    # a maximum of 1000.
    # Nc is the number of
    NsNi = np.random.randint(5, MAXCOUNT, Nc)
    Ns = np.array([drawbinom(I, prob) for I in NsNi])
    Ni = NsNi - Ns
    return {"Spontaneous tracks (Ns)": Ns, "Induced tracks (Ni)": Ni}

def calculate_central_age(Ns, Ni, zeta, seZeta, rhod, seRhod, sigma=0.15):
    """Function to calculate central age."""

    #Calculate mj
    lbda = 1.55125e-10
    m  = Ns+Ni
    p  = Ns/m
    
    theta = sum(Ns)/sum(m)
    
    
    for i in range(0, 30):
        w = m/(theta*(1-theta)+(m-1)*theta**2*(1-theta)**2*sigma**2)
        #Calculate new value of sigma and theta
        sigma = sigma*sqrt(sum(w**2*(p-theta)**2)/sum(w))
        theta = sum(w*p)/sum(w)
    
    t = (1/lbda)*log(1+1/2*lbda*zeta*rhod*(theta)/(1-theta))
    se = sqrt(1/(theta**2*(1-theta)**2*sum(w))+(seRhod/rhod)**2+(seZeta/zeta)**2)*t
    
    return {"Central":t/1e6, "2 sigma Error": 2*se/1e6, "Dispersion":sigma*100}

def calculate_pooled_age(Ns, Ni, zeta, seZeta, rhod, seRhod):

    #Calculate mj
    lbda = 1.55125e-10
    sigma = 0
    m = Ns+Ni
    p = Ns/m
    
    theta = sum(Ns)/sum(m)
    
    
    for i in range(0, 30):
        w = m/(theta*(1-theta)+(m-1)*theta**2*(1-theta)**2*sigma**2)
        theta = sum(w*p)/sum(w)
    
    t = (1/lbda)*log(1+1/2*lbda*zeta*rhod*(theta)/(1-theta))
    se<-sqrt(1/sum(Ns)+1/sum(Ni)+(seRhod/rhod)**2+(seZeta/zeta)**2)*t
    
    return {"Pooled Age":t/1e6, "2 sigma Error": 2*se/1e6}

def calculate_single_grain_ages(Ns, Ni, rhod, zeta, g=0.5, trf="Linear"):
    # Total Decay constant for 238U
    lbda = 1.55125e-10

    # Linear Transformation
    if (trf == "linear"):
        z = 1/lbda*log(1+g*zeta*lbda*rhod*(Ns/Ni))
        sez = z*np.sqrt(1/Ns + 1/Ni)
        z0 = sum(z/sez**2) / sum(1/sez**2)

    #Logarithmic transformation
    if trf == "Log":
        z = log(g*zeta*lbda*rhod*(Ns/Ni))
        sez = z*sqrt(1/Ns+1/Ni)
        z0 = log(g*zeta*lbda*rhod*(sum(Ns)/sum(Ni)))
    
    #Arcsine
    if trf == "arcsine":
        z = asin(sqrt((Ns+3/8)/(Ns+Ni+3/4)))
        sez = 1/(2*sqrt(Ns+Ni))
        z0 = asin(sqrt(sum(Ns)/sum(Ns+Ni)))


    Age = z/1e6
    Error = sez / 1e6
    
    return Age, Error

def radialplot(Ns, Ni, zeta, seZeta, rhoD, seRhoD):

    #Calculate single grain ages
    Ages, Errors = calculate_single_grain_ages(Ns, Ni, rhoD, zeta)
    
    #Calculate central age
    CentralAge = calculate_central_age(Ns, Ni, zeta, seZeta, rhoD, seRhoD)
    #Calculate pooled age
    PooledAge = calculate_pooled_age(Ns, Ni, zeta, seZeta, rhoD, seRhoD)
    
    x = Ages / Errors
    y = (Ages - CentralAge) / Errors
    
    A = plt.plot(x, y, "o")
    return A

def PlotPlot(age, error):
     
    # scale
    z = age
    ze = error
    z0 = sum(age / error**2) / sum(1 / error**2)      

def KetchamModel(history, alo=16.3):
    """Return Apatite Fission Track Age (AFTA) and Track Length
    distribution using Ketcham et al. 1999 annealing model.
   
    Parameter:
    ---------
    history -- A Thermal history class instance
    alo -- Initial track length
    """
    t = history.time
    T = history.Temperature

    A = cdll.LoadLibrary(_KETCHAM_)
    ketcham = A.ketch_main_
    n = c_int(len(t))
    n = pointer(n)
    alo = c_double(alo)
    t = (c_float*len(t))(*t)
    T = (c_float*len(T))(*T)
    alo = pointer(alo)
    final_age = pointer(c_double())
    oldest_age = pointer(c_double())
    fmean = pointer(c_double())
    fdist = (c_double*200)()
    dx = 20. / 200.
    redDensity = pointer(c_double())
    ketcham(n, t, T, alo, final_age, oldest_age, fmean, fdist, redDensity)
    return {"Final Age": final_age.contents.value,
            "Oldest Age": oldest_age.contents.value,
            "Mean Track Length": fmean.contents.value,
            "Fission Track length distribution": (np.array([dx/2.0 +
             dx*float(a) for a in range(200)]),np.array([i*dx for i in fdist])),
            "redDensity": redDensity.contents.value}

def project_fission_track():
    """Project fission track onto C-axis"""
    return

def get_path(path):
    return os.path.join(_ROOT, 'lib', path)


