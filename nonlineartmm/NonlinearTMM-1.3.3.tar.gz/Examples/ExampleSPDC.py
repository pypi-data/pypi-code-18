import numpy as np
import pylab as plt
from NonlinearTMM import SecondOrderNLTMM, Material
from LabPy import Constants

def SpdcPowerQuantum(wlP1, wlP2, betaP1, betaP2, nF, chi2, crystalL, pwrP1, dwl, solidAngleSpdc, deltaThetaSpdc):
    wlGen = Constants.OmegaToWl(Constants.WlToOmega(wlP1) - Constants.WlToOmega(wlP2))
    betaGen = wlGen * (betaP1 / wlP1 - betaP2 / wlP2);
    
    # Omegas
    omegaP1 = Constants.WlToOmega(wlP1)
    omegaP2 = Constants.WlToOmega(wlP2)
    omegaGen = Constants.WlToOmega(wlGen)
    
    # Refractive indices
    nP1 = nF(wlP1)
    nP2 = nF(wlP2)
    nGen = nF(wlGen)
    
    # Wave vectors
    k0P1 = 2.0 * np.pi / wlP1
    k0P2 = 2.0 * np.pi / wlP2
    k0Gen = 2.0 * np.pi / wlGen
    kP1 = k0P1 * nP1
    kP2 = k0P2 * nP2
    kGen = k0Gen * nGen
    
    # Pump 1
    kxP1 = betaP1 * k0P1
    kzP1 = np.sqrt(kP1 ** 2.0 - kxP1 ** 2.0)
    
    # Pump 2 / vacuum fluctuations
    kxP2 = k0P2 * betaP2
    kzP2 = np.sqrt(kP2 ** 2.0 - kxP2 ** 2.0)
    
    # Gen
    kxGen = betaGen * k0Gen
    kzGenSqr = kGen ** 2.0 - kxGen ** 2.0
    kzGen = np.sqrt(kzGenSqr)
    
    # dk
    dkz = kzP1 - kzP2 - kzGen
    #print("wlGen, betaGen, dkz", 1e9 * wlGen, betaGen, dkz)
        
    res = dwl * solidAngleSpdc / deltaThetaSpdc * \
        Constants.hp * chi2 ** 2.0 / (8.0 * np.pi ** 4 * Constants.eps0) * \
        omegaGen ** 6 * omegaP1 * omegaP2 ** 2 / (Constants.c ** 8) * pwrP1 * \
        1.0 / (kzGen * kzP1 * kP2) * \
        np.sin(0.5 * dkz * crystalL) ** 2 / (0.5 * dkz) ** 2
        
    return res

if __name__ == "__main__":
    # Define params
    wlP1 = 400e-9
    wlP2 = 800e-9
    polP1 = "s"
    polP2 = "s"
    polGen = "s"
    betaP1 = 0.0
    betasP2 = np.linspace(0.0, 0.9, 10000)
    betasP1 = np.ones_like(betasP2) * betaP1
    crystalDs = np.linspace(0.1e-3, 1e-3, 20)
    deltaThetaSpdc = np.radians(0.5)
    solidAngleSpdc = 7.61543549467e-05
    deltaWlSpdc = 2.5e-9
    chi2 = 1.4761823412e-12
    pwrP1 = 0.1
    w0 = 0.1e-3
    Ly = 1e-3
    I0 = pwrP1 / (w0 * Ly)
    
    # Define materials
    wlsCrystal = np.array([400e-9, 800.0001e-9])
    nsCrystal = np.array([1.61681049944, 1.6913720951], dtype = complex)
    prism = Material.Static(n = 1.0)#Material(wlsCrystal, nsCrystal)
    crystal = Material(wlsCrystal, nsCrystal)
    dielectric = Material.Static(n = 1.0) #Material(wlsCrystal, nsCrystal)
    crystal.chi2.Update(chi111 = chi2, chi222 = chi2, chi333 = chi2)
    print(prism.GetN(wlP1), prism.GetN(wlP2))
    
    # Init SecondOrderNLTMM
    tmm = SecondOrderNLTMM(mode = "spdc", deltaWlSpdc = deltaWlSpdc, \
                           solidAngleSpdc = solidAngleSpdc, deltaThetaSpdc = deltaThetaSpdc)
    tmm.P1.SetParams(wl = wlP1, pol = polP1, I0 = I0)
    tmm.P2.SetParams(wl = wlP2, pol = polP2, overrideE0 = True, E0 = 1.0)
    tmm.Gen.SetParams(pol = polGen)
    
    # Add layers
    tmm.AddLayer(float("inf"), prism)
    tmm.AddLayer(0.0, crystal)
    tmm.AddLayer(float("inf"), dielectric)
    
    # Waves
    waveP1Params = {"waveType": "gaussian", "pwr": pwrP1, "w0": w0, "Ly": Ly, "dynamicMaxXCoef": 10, "nPointsInteg": 500, "maxPhi": np.radians(10.0)}
    waveP2Params = {"waveType": "spdc", "w0": w0, "Ly": Ly, "overrideE0": True, "nPointsInteg": 50}
    tmm.P1.wave.SetParams(**waveP1Params)
    tmm.P2.wave.SetParams(**waveP2Params)
    #tmm.Solve()
    #print(tmm.WaveGetPowerFlows(2))
    

    spdcRates = np.zeros_like(crystalDs)
    pwrsSpdc = np.zeros_like(crystalDs)
    pwrsSpdcW = np.zeros_like(crystalDs)
    for i, crystalD in enumerate(crystalDs):
        # Update cryustal d
        tmm.P1.layers[1].d = crystalD
        tmm.P2.layers[1].d = crystalD
        tmm.Gen.layers[1].d = crystalD
        
        # Solve
        sr = tmm.Sweep("beta", betasP1, betasP2)
        #srW = tmm.WaveSweep("beta", betasP1, betasP2)
        #quantumSpdc = SpdcPowerQuantum(wlP1, wlP2, betaP1, betasP2, lambda wl: prism.GetN(wl).real, chi2, crystalD, pwrP1, deltaWlSpdc, solidAngleSpdc, deltaThetaSpdc)
        
        # Find betaP2 integration range
        wlGen = sr.wlsGen[0]
        n0Gen = prism.GetN(wlGen).real
        maxBetaP2 = betasP2[np.argmax(sr.Gen.It)]
        maxBetaGen = sr.betasGen[np.argmax(sr.Gen.It)]
        kz0Gen = (2.0 * np.pi / wlGen) * np.sqrt(n0Gen ** 2 - maxBetaGen ** 2)
        deltaKxP2 = kz0Gen / (2.0 * n0Gen) * deltaThetaSpdc
        deltaBetaP2 = deltaKxP2 / (2.0 * np.pi / wlP2)
        
        tmm.P1.beta = betaP1
        tmm.P2.beta = maxBetaP2
        
        # Integrate
        betasP2Int = np.linspace(maxBetaP2 - deltaBetaP2, maxBetaP2 + deltaBetaP2, 100)
        betasP1Int = np.ones_like(betasP2Int) * betaP1
        kxsP2Int = betasP2Int * (2.0 * np.pi / wlP2)
        srInt = tmm.Sweep("beta", betasP1Int, betasP2Int)
        E0Vac = tmm.P2.E0
        
        # Int power
        pwrSPDC = np.trapz(srInt.Gen.It, kxsP2Int)
        pwrsSpdcW[i] = tmm.WaveGetPowerFlows(2)[0]
        beamArea = tmm.P1.wave.beamArea
        pwrSPDC *= beamArea
        
        ratePump = pwrP1 / (Constants.hp * Constants.WlToOmega(wlP1))
        rateGen = pwrSPDC / (Constants.hp * Constants.WlToOmega(wlGen))
        spdcRates[i] = rateGen;
        
        pwrsSpdc[i] = pwrSPDC;
        
        
        
        #plt.figure()
        #plt.plot(tmm.P2.wave.betas, tmm.P2.wave.expansionCoefsKx, "x-", label = "P2")
        #plt.plot(betasP2Int, np.ones_like(betasP2Int))
        #plt.legend()
        
        
        
        print("pwrSPDC", beamArea * pwrsSpdc[i])
        print("pwrsSpdcW", pwrsSpdcW[i])
        print("pairs / mW", 1e-3 * rateGen / pwrP1)
        print("E0", E0Vac, tmm.P2.wave.expansionCoefsKx[0])
        print("betasP2Int", betasP2Int[0], tmm.P2.wave.betas[0])
        print("betasP2Int", betasP2Int[-1], tmm.P2.wave.betas[-1])
        print("tmm.waveP1.beamArea", beamArea)
        
        
        # Plot generated reflection and transmission
        """
        plt.figure()
        plt.title("DFG generation from crystal (d = %.0f $\mu m$)" % (1e6 * crystalD))
        #plt.plot(betasP2, sr.Gen.Ir, label = "R")
        plt.plot(betasP2, sr.Gen.It, label = "T")
        plt.plot(betasP2Int, srInt.Gen.It, "x", label = "T")
        
        plt.axvline(maxBetaP2, ls = "--", color = "red", lw = 1.0)
        plt.axvline(maxBetaP2 + deltaBetaP2, ls = "--", color = "blue", lw = 1.0)
        plt.axvline(maxBetaP2 - deltaBetaP2, ls = "--", color = "blue", lw = 1.0)
        plt.legend()
        plt.xlabel(r"$\beta$")
        plt.ylabel(r"($W / m^{2}$)")
        """
        
    
    plt.figure()
    #plt.plot(1e3 * crystalDs, 1e-3 * spdcRates / pwrP1, "x-")
    plt.plot(1e3 * crystalDs, pwrsSpdc)
    plt.plot(1e3 * crystalDs, pwrsSpdcW, "x")
    
    plt.figure()
    plt.plot(1e3 * crystalDs, pwrsSpdcW / pwrsSpdc)
        
    #srW = tmm.WaveSweep("beta", betasP1, betasP2)
    #plt.plot(betasP2, srW.Gen.Pt)
        
    # Fields
    
    zs = np.linspace(-1000e-6, 1500e-6, 300)
    xs = np.linspace(-1000e-6, 1500e-6, 310)
    
    
    fP1 = tmm.P1.WaveGetFields2D(zs, xs)
    fP2 = tmm.P2.WaveGetFields2D(zs, xs)
    fGen = tmm.WaveGetFields2D(zs, xs)
    
    plt.figure()
    plt.subplot(221)
    plt.pcolormesh(1e6 * zs, 1e6 * xs, fP1.EN.T)
    plt.colorbar()
    
    plt.subplot(222)
    plt.pcolormesh(1e6 * zs, 1e6 * xs, fP2.EN.T)
    plt.colorbar()
    
    
    plt.subplot(223)
    plt.pcolormesh(1e6 * zs, 1e6 * xs, fGen.EN.T)
    plt.colorbar()
    
        
    plt.show()
    
    """
    
    #kz0 = np.sqrt(n0Gen ** 2.0 -  )
    tmm.P1.beta = betaP1
    tmm.P2.beta = maxBetaP2
    tmm.Solve()
    print("maxBetaP2", maxBetaP2)
    print("maxBetaGen", maxBetaGen)
    print("kz0Gen", kz0Gen, (2.0 * np.pi / wlGen))
    print("deltaKxP2", deltaKxP2)
    print("deltaBetaP2", deltaBetaP2)
    print("E0vac", tmm.P2.E0 * np.sqrt((2.0 * np.pi / wlP2)))
    
    pwrSPDC = np.trapz(sr.Gen.It, betasP2 * (2.0 * np.pi / wlP2))
    ratePump = 1.0 / (Constants.hp * Constants.WlToOmega(wlP1))
    rateGen = pwrSPDC / (Constants.hp * Constants.WlToOmega(wlGen)) 
    spdcEff = rateGen / ratePump
        
    print("pwrSPDC", pwrSPDC)
    print("spdcEff", spdcEff)
    print("pairs per mW", 1e-3 * rateGen)
    """
    