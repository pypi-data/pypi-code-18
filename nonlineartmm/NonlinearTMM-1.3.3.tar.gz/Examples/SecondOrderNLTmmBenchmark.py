import numpy as np
import pylab as plt
import LabPy
#import cProfile, pstats
from time import time
from NonlinearTMM import SecondOrderNLTMM, Material


if __name__ == "__main__":
    #profile = cProfile.Profile()
    
    wlP1 = 1064e-9
    wlP2 = 1064e-9
    polP1 = "p"
    polP2 = "p"
    polGen = "p"
    I0P1 = 1.0
    I0P2 = 1.0
    dValues = {"d11": 1e-12, "d22": 1e-12, "d33": 1e-12}
    metalD = 50e-9
    crystalD = 5e-6
    betasP1 = np.linspace(1.50001, 1.6, 1000)
    betasP2 = betasP1
    nSweep = 10#150
    nFields = 10000
    betaFields = 0.3
    xs = np.linspace(-200e-6, 700e-6, 100)
    zs = np.linspace(-200e-6, 700e-6, 100)
    
    # Python
    prismPy = LabPy.Material("Static", n = 1.8)
    metalPy = LabPy.Material("main/Ag/Johnson")
    crystalPy = LabPy.Material("special/gaussian_test", kAdditional = 1e-3) 
    dielectricPy = LabPy.Material("special/gaussian_test", kAdditional = 1e-3)
    chi2 = LabPy.Chi2Tensor(**dValues)

    tmmPy = LabPy.SecondOrderNLTmm()
    tmmPy.SetParams(wlP1 = wlP1, wlP2 = wlP2, polP1 = polP1, polP2 = polP2, \
                    I0P1 = I0P1, I0P2 = I0P2, polGen = polGen) 
    tmmPy.AddLayer(float("inf"), prismPy)
    tmmPy.AddLayer(metalD, metalPy)
    tmmPy.AddLayer(crystalD, crystalPy, chi2)
    tmmPy.AddLayer(float("inf"), dielectricPy)
    
    # C++
    
    prism = Material.FromLabPy(prismPy)
    crystal = Material.FromLabPy(crystalPy)
    metal = Material.FromLabPy(metalPy)
    dielectric = Material.FromLabPy(dielectricPy)
    crystal.chi2.Update(**dValues)

    tmmCpp = SecondOrderNLTMM()
    tmmCpp.P1.SetParams(wl = wlP1, pol = polP1, I0 = I0P1)
    tmmCpp.P2.SetParams(wl = wlP2, pol = polP2, I0 = I0P2)
    tmmCpp.Gen.SetParams(pol = polGen)
    tmmCpp.AddLayer(float("inf"), prism)
    tmmCpp.AddLayer(metalD, metal)
    tmmCpp.AddLayer(crystalD, crystal)
    tmmCpp.AddLayer(float("inf"), dielectric)
    
    # Sweep
    
    """
    #profile.enable()
    enhLayer, enhZ = 2, 0.0
    startTime = time()
    for i in range(nSweep):
        srCpp = tmmCpp.Sweep("beta", betasP1, betasP2, outEnh = True, layerNr = enhLayer, layerZ = enhZ)
    timeSweepCpp = time() - startTime
    
    #profile.disable()
    #pstats.Stats(profile).sort_stats("cumtime").print_stats(30)

    #profile.enable()
    
    startTime = time()
    for i in range(nSweep):
        srPy = tmmPy.Sweep(["betaP1", "betaP2"], [betasP1, betasP2], enhpos = (enhLayer, enhZ))
    timeSweepPy = time() - startTime
    
    #profile.disable()
    #pstats.Stats(profile).sort_stats("cumtime").print_stats(30)


    print("C++ sweep", timeSweepCpp)
    print("Py sweep", timeSweepPy)
    print("Speedup", timeSweepPy / timeSweepCpp)
    # i7 620M: 730x speedup (s-pol)
    
    plt.figure()
    plt.subplot(221)
    plt.plot(betasP1, srPy["RP1"].real)
    plt.plot(betasP1, srPy["TP1"].real)
    plt.plot(betasP1, srCpp.P1.R, "x", color = "black")
    plt.plot(betasP1, srCpp.P1.T, "x", color = "black")

    plt.subplot(222)
    plt.plot(betasP1, srPy["enhP1"].real)
    plt.plot(betasP1, srCpp.P1.enh, "x", color = "black")
    plt.plot(betasP1, srCpp.P1.enh / srPy["enhP1"].real, "--", color = "black")
    
    plt.subplot(224)
    plt.plot(betasP1, srPy["RGen"].real)
    plt.plot(betasP1, srPy["TGen"].real)
    plt.plot(betasP1, srCpp.Gen.R, "x", color = "black")
    plt.plot(betasP1, srCpp.Gen.T, "x", color = "black")
    """
    
    
    # Absorbed power
    """
    AP1Py = np.zeros_like(betasP1)
    AP1Cpp = np.zeros_like(betasP1)
    AGenPy = np.zeros_like(betasP1)
    AGenCpp = np.zeros_like(betasP1)
    for i, (betaP1, betaP2) in enumerate(zip(betasP1, betasP2)):
        rP1, rP2, rGen = tmmPy.Solve(betaP1 = betaP1, betaP2 = betaP2)
        tmmCpp.P1.SetParams(beta = betaP1)
        tmmCpp.P2.SetParams(beta = betaP2)
        tmmCpp.Solve()
        
        AP1Py[i] = rP1[6]
        AP1Cpp[i] = tmmCpp.P1.GetAbsorbedPower()
        AGenPy[i] = rGen[6]
        AGenCpp[i] = tmmCpp.Gen.GetAbsorbedPower()
    
    plt.figure()
    plt.subplot(221)
    plt.plot(betasP1, AP1Py)
    plt.plot(betasP1, AP1Cpp, "--")
    plt.subplot(222)
    plt.plot(betasP1, AGenPy)
    plt.plot(betasP1, AGenCpp, "--")
    """
    
    
    # Fields
    # Cpp
    tmmCpp.P1.SetParams(beta = betaFields)
    tmmCpp.P2.SetParams(beta = betaFields)

    #profile.enable()
    
    startTime = time()
    for i in range(nFields):
        tmmCpp.Solve()
        fieldsCpp = tmmCpp.Gen.GetFields2D(zs, xs)
    timefieldsCpp = time() - startTime
    
    #profile.disable()
    #pstats.Stats(profile).sort_stats("cumtime").print_stats(30)
    
    # Py
    tmmPy.SetParams(betaP1 = betaFields, betaP2 = betaFields)
    startTime = time()
    for i in range(nFields):
        tmmPy.Solve()
        EPy, HPy = tmmPy.tmmGen.GetFields2D(zs, xs)
    timefieldsPy = time() - startTime
    
    print("C++ fields2d", timefieldsCpp)
    print("Py fields2d", timefieldsPy)
    print("Speedup", timefieldsPy / timefieldsCpp)
    
    plt.figure()
    plt.subplot(121)
    plt.pcolormesh(1e6 * zs, 1e6 * xs, fieldsCpp.EN.real.T)
    plt.colorbar()
    
    plt.subplot(122)
    plt.pcolormesh(1e6 * zs, 1e6 * xs, np.linalg.norm(EPy, axis = 2).real.T)
    plt.colorbar()
    
    plt.show()
    
    
    