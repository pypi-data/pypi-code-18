import numpy as np
from scipy.constants import Avogadro
from .constants import U238_ATOM_MASS, U235_ATOM_MASS, TH232_ATOM_MASS, yr, RGAS
from .utilities import GetHeliumProdRateRdaam
from math import *


ketch07_c0 = 0.39528
ketch07_c1 = 0.01073
ketch07_c2 = -65.12969
ketch07_c3 = -7.91715
ketch07_alpha = 0.04672


def _get_rmr0_kappa(kineticPar, options="ETCHPIT LENGTH"):
    """ Calculates rmr0 and kappa for a given composition 
    (determined by the kinetic parameter type and its value """

    if options == "ETCHPIT LENGTH":
        if   kineticPar <= 1.75:
            rmr0 = 0.84
        elif kineticPar >= 4.58:
            rmr0 = 0.00
        else:
            rmr0 = 0.84 * ((4.58 - kinpar) / 2.98)**0.21
    
    if options == "CL_WT_PCT":
        kineticPar = kineticPar * 0.2978
    
    if options == "L_PFU":
       calc = abs(kineticPar - 1)
       if calc <= 0.130:
           rmr0 = 0.
       else:
           rmr0 = 1.0 - exp(2.107 * (1.0 - calc) - 1.834) 
    
    if options == "OH_PFU":
        calc = abs(kineticPar - 1.0)
        rmr0 = 0.84 * (1.0 - (1.0 - calc)**4.5)
    
    if options is None:
        rmr0 = kineticPar
  
    kappa = 1.04 - rmr0

    return rmr0, kappa

def _equivTime(r, temperature):
    g = ( 1.0 / r - 1.0)**(ketch07_alpha)
    return exp(ketch07_c2 - (g - ketch07_c0) / ketch07_c1
               * (log(temperature) + ketch07_c3))

def _rcDensity(cParLen):
   
    if cParLen > 0.757:
      rcDensity = 1.600 * cParLen - 0.599
    elif cParLen >= 0.55:
      rcDensity =  9.205 * cParLen * cParLen - 9.157 * cParLen + 2.269
    else:
      rcDensity = 0.

    return max(rcDensity, 0.)

def _FTanneal(time, temperature):
    
    FTanneal = (ketch07_c0 - ketch07_c1 * (log(time)
                - ketch07_c2) / (log(temperature) + ketch07_c3))

    if FTanneal <= 0:
       FTanneal = 0.
    else:
       FTanneal = 1.0 / (FTanneal**(1 / ketch07_alpha) + 1)
    return FTanneal

def _get_fine_history(coolpath):
    time = coolpath.t
    temperature = coolpath.TK
    dTemp = 2.0

    mtimes = np.abs(np.diff(temperature) / dTemp)
    mtimes = mtimes.astype(int)
    mtimes = np.where(mtimes < 10, 10, mtimes)

    if time.size > 50:
        mtimes = np.ones(time.shape)

    dTemps = np.diff(temperature) / mtimes
    dts = np.diff(time) / mtimes
    sdls = np.diff(time) / time.max()

    # Adjust dts, mtimes etc.
    for i, (dt, sdl) in enumerate(zip(dts, sdls)):
        if dt > np.diff(time)[i] / 50 and sdl > 0.5:
            dts[i] = (time[i+1] - time[i]) / 50
            mtimes[i] = (time[i+1] - time[i]) / dts[i]
            dTemps[i] = (temperature[i+1] - temperature[i]) / mtimes[i]

    fineTime = [np.linspace(time[i], time[i+1], mtimes[i], endpoint=False)
                for i in range(len(mtimes))] + [[time[-1]]]
    fineTemp = [np.linspace(temperature[i], temperature[i+1], mtimes[i], endpoint=False)
                for i in range(len(mtimes))] + [[temperature[-1]]]

    fineTime = np.concatenate(fineTime)
    fineTemp = np.concatenate(fineTemp)
    fineTemp = np.concatenate([fineTemp, [fineTemp[-1]]])
    fineTemp = (fineTemp[:-1] + fineTemp[1:]) / 2.0

    return fineTime, fineTemp

def _get_sum_density(coolpath, kineticPar, kineticK="ETCHPIT LENGTH"):
    """

    """
    
    # Do a fine loop on temperature to calculate the diffusivity dependent on Eu
    timePoints, tempPoints = _get_fine_history(coolpath)
    timePoints *= yr * 1e6

    rmr0, kappa = _get_rmr0_kappa(kineticPar, kineticK)

    # Initialize tracks ages from 0 to maxtime
    # (constant production of tracks with time) 
    nbTracks = 100
    trackAges = np.arange(0, nbTracks) * timePoints.max() / nbTracks
    lengths = np.zeros(trackAges.shape)
    created = np.zeros(trackAges.shape, dtype=bool)

    dts = np.diff(timePoints)
    dts = np.concatenate([dts] + [[dts[-1]]])
    ftrack = np.zeros(timePoints.shape)


    # Track are continuously created all along the thermal history.
    # The track density and so the radiation damage are a combination of the
    # tracks formed at different times. The following loop keep track of the track lengths
    # for tracks formed at different times.  
  
    
    for timeId, (time, temperature) in enumerate(zip(timePoints, tempPoints)):
       
        sum_density=0.
        nonzero = 0
        ik = 0
        while ik <= nbTracks - 1 and time - trackAges[ik] > 1.0e-20:
          
            dt = dts[timeId]
            density = 0.

            if not created[ik]:

                created[ik] = True
                #  For this study we use the fission-track annealing calibration of
                #  Ketcham et al. (2007). This model characterizes the reduced mean length
                #  of fission tracks that form along the crystallographic c axis
                #  for highly-annealing-resistant apatite B2 (Carlson et al., 1999)
                #  (see function FTanneal)
                lengths[ik] = _FTanneal(time - trackAges[ik] , temperature)

                # The reduced mean c-axis-projected length (lengthcomp) of fission tracks 
                # in some less-resistant apatite  :
                if lengths[ik] - rmr0 > 0.:
                    lengthcomp = ((lengths[ik] - rmr0) / (1 - rmr0))**kappa
                else:
                    lengthcomp = 0.
            
                # Reduced length (lengthcomp) is then converted to reduced spontaneous density
                # (density) using the empirical length-density conversion provided
                # by Ketcham et al. (2003)
                density = _rcDensity(lengthcomp)  
                
                if density > 0.:
                    nonzero = nonzero+1
          
            elif lengths[ik] > 0:
                # If the track length is greater than 0. (track exists) then: calculates the 
                # equivalent time at given temperature to obtain that length. 
           
                Eqtime = _equivTime(lengths[ik], temperature)
                #  Calculate the track length for this step
                lengths[ik] = _FTanneal(Eqtime + dt, temperature)

                # Calculates the reduced track length
                if lengths[ik] - rmr0 > 0.:
                    lengthcomp = ((lengths[ik] - rmr0 ) / (1 - rmr0))**kappa
                else: 
                    lengthcomp = 0.0
            
                # Convert to reduced spontaneous density
                density = _rcDensity(lengthcomp)
               
                if density > 0.:
                    nonzero = nonzero+1
                        
            sum_density += density
            ik += 1

        if nonzero > 0:
            sum_density /= nonzero
        else: 
            sum_density = 0.
            
        ftrack[timeId] = sum_density
        
    return ftrack, timePoints, tempPoints

def _rdaam_diffusivities(Model, time, temperature, U238PPM, U235PPM, TH232PPM, sumDensityArray):
    if Model == "GAUTHERON":
        return _gautheron_diffusivities(time, temperature, U238PPM, U235PPM, TH232PPM, sumDensityArray)
    if Model == "FLOWERS":
        return _flowers_diffusivities(time, temperature, U238PPM, U235PPM, TH232PPM, sumDensityArray)

def _gautheron_diffusivities(time, temperature, U238PPM, U235PPM, TH232PPM, sumDensityArray):

    # Cecile's model
    cc = 3.0e-7  # ppm/ Myr
    Eaa = 109200 # joules/mol
    Eab = 31400  # joules/mol
    D0c = 2.e-3  # cm2/s  
  
    eeU = U238PPM + U235PPM + 0.24 * TH232PPM
    Drad = cc * time /(yr * 1e6) * sumDensityArray * eeU
    return D0c * np.exp(-Eaa / (RGAS * temperature)) / (1.0 + Drad * np.exp( Eab / (RGAS * temperature)))

def _flowers_diffusivities(time, temperature, U238PPM, U235PPM, TH232PPM, sumDensityArray):
    # Flowers model
    lambdaf = 8.46e-17     # 1/yr
    lambdad = 1.55125e-10  # 1/yr
    nq = 0.91          
    letch = 8.1            # microns
    omega = 1e-22          # log(omega)=-22.0 (Hefty 1e-22)
    psi = 1e-13            # log(psi)=-13.0 Flowers,2009                           
    D0L = 0.60714          # 0.6071 Hefty (cm2/sec)
    Etrap = 34000          # joules/mol (34140: HEfty)
    EL = 122300            # joules/mol (122300: Hefty)
    
    # Calculate number of atoms
    U238atoms  =  U238PPM * 1e-6 * Avogadro / U238_ATOM_MASS * 3.2
    U235atoms  =  U235PPM * 1e-6 * Avogadro / U235_ATOM_MASS * 3.2
    TH232atoms = TH232PPM * 1e-6 * Avogadro / TH232_ATOM_MASS * 3.2

    HeProdArray = np.zeros(time.shape)
    for i, t in enumerate(time):
        HeProdArray[i] = GetHeliumProdRateRdaam(0., t, U238atoms, U235atoms, TH232atoms)

    sumDensityArray *= lambdaf / lambdad * nq * letch * 1e-4 * HeProdArray
    Drad = psi + omega * sumDensityArray**3
    return D0L * np.exp( -EL / (RGAS * temperature)) /(1.0 + Drad * np.exp( Etrap / (RGAS * temperature))) 

