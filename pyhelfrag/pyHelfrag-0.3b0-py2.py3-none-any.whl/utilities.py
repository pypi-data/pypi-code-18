from __future__ import print_function

import random
from math import *
import numpy as np
from scipy.integrate import ode
import pylab as plt
from .constants import *
from .modeode import *
#from _registry import *

def Get238fromUcontent(U, t):
    cunatrt = unatrt * ((np.exp(U235_DECAYCT*t*1e6))/(np.exp(U238_DECAYCT*t*1e6))) 
    return U*(1/(cunatrt+1))

def Get235fromUcontent(U, t):
    U238 = Get238fromUcontent(U, t)
    return U - U238

def Get232fromThcontent(Th, t):
    #ctnatrt = unatrt * ((np.exp(TH232_DECAYCT*t*1e6))/(np.exp(TH230_DECAYCT*t*1e6))) 
    return Th*(1/(tnatrt+1))

def Get230fromThcontent(Th, t):
    TH232 = Get232fromThcontent(Th, t)
    return Th - TH232

def ppm2molesm3(val, atomic_mass):
    return val * 1e-3 * ap_density / atomic_mass

def moles_m3_2_ppm(val, atomic_mass):
    return val * 1e3 * atomic_mass / ap_density

def GetHeliumProdRate(U238, U235, Th232):
    return 8*U238_DECAYCT*U238+7*U235_DECAYCT*U235+6*TH232_DECAYCT*TH232

def GetHeliumProdRateRdaam(t1, t2, U238, U235, TH232):
    l238 = 4.916e-18 #/sec 
    l235 = 3.12e-17 #/sec
    l232 = 1.57e-18 #/sec

    A238  =  exp(l238*t2)-exp(l238*t1)
    A235  =  exp(l235*t2)-exp(l235*t1)
    A232  =  exp(l232*t2)-exp(l232*t1)
    return ((8 * U238 * A238 + 7*U235 * A235 + 6 * TH232 * A232) / 8.0)

def GetHeliumAgeMD2005(helium, uranium238, uranium235, thorium232, thorium230):
    """ Calculate Helium age as in Meesters and Dunai 2005 """

    # He4 Production rate
    U238_PRODRATE = 8 * U238_DECAYCT * uranium238
    U235_PRODRATE = 7 * U235_DECAYCT * uranium235
    TH232_PRODRATE = 6 * TH232_DECAYCT * thorium232
    TOTAL_PRODRATE = U238_PRODRATE + U235_PRODRATE + TH232_PRODRATE

    # Decay rate

    U238_DECAY_RATE = U238_PRODRATE * U238_DECAYCT / TOTAL_PRODRATE
    U235_DECAY_RATE = U235_PRODRATE * U235_DECAYCT / TOTAL_PRODRATE
    TH232_DECAY_RATE = TH232_PRODRATE * TH232_DECAYCT / TOTAL_PRODRATE
    WMEAN_DECAY_RATE = U238_DECAY_RATE + U235_DECAY_RATE + TH232_DECAY_RATE
               
    # Helium age

    HELIUM_AGE = (1/WMEAN_DECAY_RATE)*(log((WMEAN_DECAY_RATE/TOTAL_PRODRATE)*helium+1))
    return HELIUM_AGE*1e-6 
   
def GetHelium(HELIUM_AGE, uranium, thorium, helium):
    
    U238_PRODRATE = 8 * U238_DECAYCT * uranium * (1/(unatrt+1))
    U235_PRODRATE = 7 * U235_DECAYCT * uranium * (1-(1/(unatrt+1)))
    TH232_PRODRATE = 6 * TH232_DECAYCT * thorium
    TOTAL_PRODRATE = U238_PRODRATE + U235_PRODRATE + TH232_PRODRATE
    
    U238_DECAY_RATE = U238_PRODRATE * U238_DECAYCT / TOTAL_PRODRATE
    U235_DECAY_RATE = U235_PRODRATE * U235_DECAYCT / TOTAL_PRODRATE
    TH232_DECAY_RATE = TH232_PRODRATE * TH232_DECAYCT / TOTAL_PRODRATE
    WMEAN_DECAY_RATE = U238_DECAY_RATE + U235_DECAY_RATE + TH232_DECAY_RATE
    
    helium = ((exp(HELIUM_AGE*WMEAN_DECAY_RATE)-1) * TOTAL_PRODRATE) / WMEAN_DECAY_RATE
    return helium

def GetU238atTime(U238,t):
    return U238 * exp(-U238_DECAYCT*t*1e6)

def GetU235atTime(U235,t):
    return U235 * exp(-U235_DECAYCT*t*1e6)

def GetTH232atTime(TH232,t):
    return TH232 * exp(-TH232_DECAYCT*t*1e6)

def GetTH2320atTime(TH230,t):
    return TH230 * exp(-TH230_DECAYCT*t*1e6)

def FarleyFactor():
    return 0

def ReadGrainFileList(filename,order={"Length":1, "Radius":2}):
    f = open(filename, "r")
    lines = f.readlines()
    return

def PlotADFD(grainlist):
    return 0

def PlotAgeVsEu(grainlist):
    Ages = [grain.HeAge for grain in grainlist]
    Eu = [grain.Eu for grain in grainlist]
    plt.title("Eu vs Age")
    plt.xlabel("Eu (ppm)")
    plt.ylabel("Age (Myr)")
    plt.xlim((0,100))
    plt.ylim((0,200))
    return plt.plot(Eu, Ages)

def PlotAgeVsERadius(grainlist):
    Ages = [grain.HeAge for grain in grainlist]
    Eradii = [grain.Eradius for grain in grainlist]
    plt.title("Eradius vs Age")
    plt.xlabel("Eradius")
    plt.ylabel("Age (Myr)")
    plt.xlim((0,200))
    plt.ylim((0,200))
    return plt.plot(Eradii, Ages)
