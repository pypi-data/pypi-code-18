import numpy as np
import pylab as plt
from NonlinearTMM import SecondOrderNLTMM, Material

if __name__ == "__main__":
    # Define params
    wlP1 = 1000e-9
    wlP2 = 1000e-9
    polP1 = "s"
    polP2 = "s"
    polGen = "s"
    I0P1 = 1.0
    Ly = 1e-3
    w0P1 = 4000e-6
    w0P2 = 4000e-6
    pwrP1 = 1.0
    E0P2 = 1.0
    
    betas = np.linspace(0.0, 1.4, 10)
    crystalD = 50e-6

    
    # Define materials
    wlsCrystal = np.array([400e-9, 1100e-9])
    nsCrystal = np.array([1.54, 1.53], dtype = complex)
    prism = Material.Static(1.5)
    crystal = Material(wlsCrystal, nsCrystal)
    dielectric = Material.Static(1.6)
    crystal.chi2.Update(d11 = 1e-12, d22 = 1e-12, d33 = 1e-12)
    
    # Init SecondOrderNLTMM
    tmm = SecondOrderNLTMM()
    tmm.P1.SetParams(wl = wlP1, pol = polP1, beta = 0.0, I0 = pwrP1 / (Ly * w0P1))
    tmm.P2.SetParams(wl = wlP2, pol = polP2, beta = 0.0, overrideE0 = True, E0 = E0P2)
    tmm.Gen.SetParams(pol = polGen)
    
    # Add layers
    tmm.AddLayer(float("inf"), prism)
    tmm.AddLayer(crystalD, crystal)
    tmm.AddLayer(float("inf"), dielectric)

    # Init waves
    waveP1Params = {"waveType": "gaussian", "pwr": pwrP1, "w0": w0P1, "Ly": Ly, "dynamicMaxXCoef": 10, "nPointsInteg": 500, "maxPhi": np.radians(10.0)}
    waveP2Params = {"waveType": "planewave", "w0": w0P2, "Ly": Ly, "overrideE0": True, "E0": E0P2}
    tmm.P1.wave.SetParams(**waveP1Params)
    tmm.P2.wave.SetParams(**waveP2Params)
    
    sr = tmm.Sweep("beta", betas, betas)
    srW = tmm.WaveSweep("beta", betas, betas)
    
    plt.figure()
    plt.subplot(121)
    plt.plot(betas, sr.Gen.Ir * srW.Gen.beamArea, label = "R")
    plt.plot(betas, srW.Gen.Pr, "x", label = "WR")
    plt.legend()
    plt.subplot(122)
    plt.plot(betas, sr.Gen.It * srW.Gen.beamArea, label = "T")
    plt.plot(betas, srW.Gen.Pt, ".", label = "WT")
    plt.legend()
    plt.xlabel(r"$\beta$")
    plt.ylabel(r"($W / m^{2}$)")
   
     
    # Wave fields
    tmm.P1.beta = 0.0
    tmm.P2.beta = 0.0
    zs = np.linspace(-300e-6, 1000e-6, 500)
    xs = np.linspace(-500e-6, 500e-6, 510)
    f = tmm.WaveGetFields2D(zs, xs)
    plt.figure()
    plt.pcolormesh(1e6 * zs, 1e6 * xs, f.EN.T, cmap = "RdBu_r")
    plt.colorbar()
    
   
    plt.show()
    
    