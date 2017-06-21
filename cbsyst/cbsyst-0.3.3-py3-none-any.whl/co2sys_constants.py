import numpy as np

"""
 SUB Constants, version 04.01, 10-13-97, written by Ernie Lewis.
 Inputs: pHScale, WhichKs, WhoseKSO4, Sali, TempCi, Pdbar
 Outputs: K0, K(), T(), fH, FugFac, VPFac
 This finds the Constants of the CO2 system in seawater or freshwater,
 corrects them for pressure, and reports them on the chosen pH scale.
 The process is as follows: the Constants (except KS, KF which stay on the
 free scale - these are only corrected for pressure) are
       1) evaluated as they are given in the literature
       2) converted to the SWS scale in mol/kg-SW or to the NBS scale
       3) corrected for pressure
       4) converted to the SWS pH scale in mol/kg-SW
       5) converted to the chosen pH scale

       PROGRAMMER'S NOTE: all logs are log base e
       PROGRAMMER'S NOTE: all Constants are converted to the pH scale
               pHScale (the chosen one) in units of mol/kg-SW
               except KS and KF are on the free scale
               and KW is in units of (mol/kg-SW)^2

***************************************************************************
CorrectKsForPressureNow:
 Currently: For WhichKs = 1 to 7, all Ks (except KF and KS, which are on
       the free scale) are on the SWS scale.
       For WhichKs = 6, KW set to 0, KP1, KP2, KP3, KSi don't matter.
       For WhichKs = 8, K1, K2, and KW are on the "pH" pH scale
       (the pH scales are the same in this case); the other Ks don't matter.


 No salinity dependence is given for the pressure coefficients here.
 It is assumed that the salinity is at or very near Sali = 35.
 These are valid for the SWS pH scale, but the difference between this and
 the total only yields a difference of .004 pH units at 1000 bars, much
 less than the uncertainties in the values.
****************************************************************************
 The sources used are:
 Millero, 1995:
       Millero, F. J., Thermodynamics of the carbon dioxide system in the
       oceans, Geochemica et Cosmochemica Acta 59:661-677, 1995.
       See table 9 and eqs. 90-92, p. 675.
       TYPO: a factor of 10^3 was left out of the definition of Kappa
       TYPO: the value of R given is incorrect with the wrong units
       TYPO: the values of the a's for H2S and H2O are from the 1983
                values for fresh water
       TYPO: the value of a1 for B(OH)3 should be +.1622
        Table 9 on p. 675 has no values for Si.
       There are a variety of other typos in Table 9 on p. 675.
       There are other typos in the paper, and most of the check values
       given don't check.
 Millero, 1992:
       Millero, Frank J., and Sohn, Mary L., Chemical Oceanography,
       CRC Press, 1992. See chapter 6.
       TYPO: this chapter has numerous typos (eqs. 36, 52, 56, 65, 72,
               79, and 96 have typos).
 Millero, 1983:
       Millero, Frank J., Influence of pressure on chemical processes in
       the sea. Chapter 43 in Chemical Oceanography, eds. Riley, J. P. and
       Chester, R., Academic Press, 1983.
       TYPO: p. 51, eq. 94: the value -26.69 should be -25.59
       TYPO: p. 51, eq. 95: the term .1700t should be .0800t
       these two are necessary to match the values given in Table 43.24
 Millero, 1979:
       Millero, F. J., The thermodynamics of the carbon dioxide system
       in seawater, Geochemica et Cosmochemica Acta 43:1651-1661, 1979.
       See table 5 and eqs. 7, 7a, 7b on pp. 1656-1657.
 Takahashi et al, in GEOSECS Pacific Expedition, v. 3, 1982.
       TYPO: the pressure dependence of K2 should have a 16.4, not 26.4
       This matches the GEOSECS results and is in Edmond and Gieskes.
 Culberson, C. H. and Pytkowicz, R. M., Effect of pressure on carbonic acid,
       boric acid, and the pH of seawater, Limnology and Oceanography
       13:403-417, 1968.
 Edmond, John M. and Gieskes, J. M. T. M., The calculation of the degree of
       seawater with respect to calcium carbonate under in situ conditions,
       Geochemica et Cosmochemica Acta, 34:1261-1291, 1970.
****************************************************************************
 These references often disagree and give different fits for the same thing.
 They are not always just an update either; that is, Millero, 1995 may agree
       with Millero, 1979, but differ from Millero, 1983.
 For WhichKs = 7 (Peng choice) I used the same factors for KW, KP1, KP2,
       KP3, and KSi as for the other cases. Peng et al didn't consider the
       case of P different from 0. GEOSECS did consider pressure, but didn't
       include Phos, Si, or OH, so including the factors here won't matter.
 For WhichKs = 8 (freshwater) the values are from Millero, 1983 (for K1, K2,
       and KW). The other aren't used (TB = TS = TF = TP = TSi = 0.), so
       including the factors won't matter.
****************************************************************************
       deltaVs are in cm3/mole
       Kappas are in cm3/mole/bar
****************************************************************************
"""

# ****************************  MASTER  ************************************

def generate_constants(sal, tempC, pres=None,
                       TB='Uppstrom', KS='Dickson',
                       TS='Morris', TF='Riley', KP='Yao & Millero',
                       K1K2='Millero 2010', pH_scale='SWS', uc=1):
    """Aggregate all constants except K1 and K2 into one dictionary."""

    KP1, KP2, KP3 = calc_KPs(sal, tempC, pres, KP)

    cdict = {"KB"  : calc_KB(sal, tempC, pres, KS),
             "TB"  : calc_TB(sal, TB, uc),
             "TS"  : calc_TS(sal, TS, uc),
             "TF"  : calc_TF(sal, TF, uc),
             "KF"  : calc_KF(sal, tempC, pres=pres),
             "KS"  : calc_KS(sal,  tempC, pres, mode=KS),
             "KW"  : calc_KW(sal,  tempC, pres),
             "KP1" : KP1,
             "KP2" : KP2,
             "KP3" : KP3,
             "KSi" : calc_KSi(sal, tempC, pres),
             "K0"  : calc_K0(sal, tempC),
             "FugFac"    : calc_fugfac(tempC),
             'TB_mode': TB,
             'KS_mode': KS,
             'TS_mode': TS,
             'TF_mode': TF,
             'SWStoTOT': calc_SWStoTOT(sal, tempC, pres, KS),
             'FREEtoTOT': calc_FREEtoTOT(sal, tempC, pres, KS),
             'K1K2_mode': K1K2,
             'pH_scale': pH_scale}
    cdict['K1'], cdict['K2'] = calc_K1K2(sal, tempC, pres, K1K2)


    return convert_pH_scale(cdict, sal, tempC)


# ****************************  GENERAL  ************************************

def tc_2_tk(tempC):
    """
    Convert centigrate to kelvin
    """
    return  tempC + 273.15

def calc_RT(tempC, RGasConstant=83.1451):
    return RGasConstant * tc_2_tk(tempC)

def calc_IonS(sal):
    """DOE handbook, Chapter 5, p. 13/22, eq. 7.2.4"""
    return 19.924 * sal / (1000 - 1.005 * sal)

def calc_SWStoTOT(sal, tempC, pres, KSmode):
    TS = calc_TS(sal)
    KS = calc_KS(sal, tempC, pres=pres, mode=KSmode)
    TF = calc_TF(sal)
    KF = calc_KF(sal, tempC, pres=pres)

    return (1 + TS/KS) / (1 + TS/KS + TF/KF)

def calc_FREEtoTOT(sal, tempC, pres, KSmode):
    TS = calc_TS(sal)
    KS = calc_KS(sal, tempC, pres=pres, mode=KSmode)

    return 1 + TS / KS

def calc_fH(sal, tempC):
    """Takahashi et al, Chapter 3 in GEOSECS Pacific Expedition,
        v. 3, 1982 (p. 80);

        Used in NBS pH conversion
    """
    #Use GEOSECS's value for cases 1,2,3,4,5 (and 6) to convert pH scales.
    tempK = tc_2_tk(tempC)
    fH = 1.2948 - 0.002036*tempK + (0.0004607 - 0.000001475*tempK) * sal**2
    return fH

def convert_pH_scale(cdict, sal, tempC):
    "Convert cdict to other pHscale"""

    if 'tot' in cdict['pH_scale'].lower(): #Total
        pHfactor = cdict['SWStoTOT']
    elif 'sws' in cdict['pH_scale'].lower(): #SWS, they are all on this now
        pHfactor = 1
    elif 'free' in cdict['pH_scale'].lower(): #pHfree
        pHfactor = cdict['SWStoTOT'] / cdict['FREEtoTOT']
    elif 'nbs' in cdict['pH_scale'].lower(): #pHNBS
        pHfactor = calc_fH(sal, tempC)

    for key in ["K1", "K2", "KW", "KB", "KP1", "KP2", "KP3", "KSi"]:
        cdict[key] = cdict[key] * pHfactor

    cdict['pHfactor'] = pHfactor
    return cdict

# ****************************  BORON  ************************************

def calc_TB_Uppstrom(sal):
    """
    Calculate total boron using Uppstrom (1974)
    Uppstrom, L., Deep-Sea Research 21:161-162, 1974

    Parameters
    ----------
    sal : float
        Salinity
    mode : str or array-like
        'Uppstrom' :
        'Lee' : Lee, Kim, Byrne, Millero, Feely, Yong-Ming Liu. 2010.
                Geochimica Et Cosmochimica Acta 74 (6): 1801?1811.
        array-like : TB to be used in calculations

    Returns
    -------
    Total B concentration in mol/kg SW
    """
    return 0.0004157 * sal / 35


def calc_TB_Lee(sal):
    """
    Calculate total boron using Lee et al (2010)

    Lee, Kim, Byrne, Millero, Feely, Yong-Ming Liu. 2010.
    Geochimica Et Cosmochimica Acta 74 (6): 1801?1811.

    Parameters
    ----------
    sal : float
        Salinity
    mode : str or array-like
        'Uppstrom' :
        'Lee' :
        array-like : TB to be used in calculations

    Returns
    -------
    Total B concentration in mol/kg SW
    """
    return 0.0004326 * sal / 35

fdict_TB = {'Uppstrom': calc_TB_Uppstrom,
            'Lee': calc_TB_Lee}

def calc_TB(sal, mode='Lee', uc=1):
    """
    Calculate Total Boron

    Using parameterisation of Uppstrom or Lee, or specifying TB.

    Parameters
    ----------
    sal : float
        Salinity
    mode : str
        Uppstrom : Uppstrom (1974)
        Lee : Lee et al (2010)
    BT : array-like (optional)
        Specify B concentration. If more than one value,
        must be the same shape as any other analysis parameters

    Returns
    -------
    Total Boron concentration in mol / kg SW.
    """
    if isinstance(mode, str):
        return fdict_TB[mode](sal)
    else:
        return mode / uc


def calc_KB(sal, tempC, pres=None, KSmode='Dickson'):
    """Calculate KB

    Dickson, A. G., Deep-Sea Research 37:755-766, 1990:
    Pressure effects from: Millero, 1979.
    with parameters from Culberson and Pytkowicz, 1968.
    Millero 1983: deltaV = -28.56 + .1211.*TempCi - .000321.*TempCi.*TempCi
                  Kappa = (-3 + .0427.*TempCi)./1000
                  lnKBfac = (-deltaV + 0.5.*Kappa.*Pbar).*Pbar./RT(tempC);
    Millero 1992: deltaV = -29.48 + .1622.*TempCi + .295.*(Sali - 34.8)
                  Kappa + .354.*(Sali - 34.8)./1000
    Millero 1995: deltaV = -29.48 - .1622.*TempCi - .002608.*TempCi.*TempCi
                  Kappa + .354.*(Sali - 34.8)./1000
    Millero 1979: deltaV = deltaV + .295.*(Sali - 34.8);
                  Kappa  = -2.84./1000; # Millero, 1979
    """
    tempK = tc_2_tk(tempC)
    lnKBtop = (-8966.9 - 2890.53 * np.sqrt(sal) - 77.942 * sal + 1.728 *
               np.sqrt(sal) * sal - 0.0996 * sal**2)
    lnKB = (lnKBtop/tempK + 148.0248 + 137.1942*np.sqrt(sal) + 1.62142*sal +
            (-24.4344 - 25.085*np.sqrt(sal) - 0.2474 * sal) * np.log(tempK) +
            0.053105 * np.sqrt(sal) * tempK)
    KB = np.exp(lnKB) / calc_SWStoTOT(sal, tempC, pres, KSmode)
    # pressure correction
    if pres is not None:
        Pbar = pres/10
        deltaV  = -29.48 + 0.1622 * tempC - 0.002608 * tempC**2
        Kappa   = -2.84 / 1000
        lnKBfac = (-deltaV + 0.5 * Kappa * Pbar) * Pbar / calc_RT(tempC)
        KBfac  = np.exp(lnKBfac)
        KB     = KB * KBfac
    return KB

# ****************************  WATER  ************************************


def calc_KW(sal, tempC, pres=None):
    """Calculate KW"""
    tempK = tc_2_tk(tempC)
    lnKW = (148.9802 - 13847.26 / tempK - 23.6521 * np.log(tempK) +
            (-5.977 + 118.67 / tempK + 1.0495 * np.log(tempK)) *
            np.sqrt(sal) - 0.01615 * sal)
    KW = np.exp(lnKW) # SWS pH scale in (mol/kg-SW)^2
    if pres is not None:
        Pbar = pres / 10.
        # Millero, 1983 and his programs CO2ROY(T).BAS.
        deltaV  = -20.02 + 0.1119 * tempC - 0.001409 * tempC**2
        # Millero, 1992 and Millero, 1995 have:
        Kappa   = (-5.13 + 0.0794 * tempC) / 1000 # Millero, 1983
        # Millero, 1995 has this too, but Millero, 1992 is different.
        lnKWfac = (-deltaV + 0.5 * Kappa * Pbar) * Pbar / calc_RT(tempC)
        # Millero, 1979 does not list values for these.
        KW = KW * np.exp(lnKWfac)
    return KW


# ****************************  FLUORINE  ************************************

def calc_TF(sal, mode='Riley', uc=1):
    """
    Calculate total Fluorine

    Riley, J. P., Deep-Sea Research 12:219-220, 1965:
    this is .000068.*Sali./35. = .00000195.*Sali
    """
    if isinstance(mode, str):
        return (0.000067/18.998) * (sal/1.80655) # mol/kg-SW
    else:
        return mode / uc

def calc_KF(sal, tempC, pres=None):
    """Dickson, A. G. and Riley, J. P., Marine Chemistry 7:89-99, 1979
    Pressure effects from Millero, 1983, 1995
    It is assumed that KF is on the free pH scale.
    """
    # exp(lnKF) is on the free pH scale in mol/kg-H2O
    lnKF = 1590.2/tc_2_tk(tempC) - 12.641 + 1.525 * calc_IonS(sal)**0.5
    KF = np.exp(lnKF) * (1 - 0.001005 * sal) # mol/kg-SW
    if pres is not None:
        Pbar = pres / 10
        deltaV  = -9.78 - 0.009 * tempC - 0.000942 * tempC**2
        Kappa   = (-3.91 + 0.054 * tempC) / 1000
        lnKFfac = (-deltaV + 0.5 * Kappa * Pbar) * Pbar / calc_RT(tempC)
        KFfac   = np.exp(lnKFfac)
        KF      = KF * KFfac
    return KF

# def calc_KF_perez_fraga_1987(sal, tempC):
#     """Perez and Fraga 1987.
#     Not used here since ill defined for low salinity.
#     (to be used for S: 10-40, T: 9-33)
#     Nonetheless, P&F87 might actually be better than the fit of D&R79 above,
#     which is based on only three salinities: [0 26.7 34.6]
#     """
#     lnKF = 874. / tc_2_tk(tempC) - 9.68 + 0.111 * sal**0.5
#     return np.exp(lnKF) # the free pH scale in mol/kg-SW

# ****************************  SULPHATE  ************************************

def calc_TS(sal, mode='Morris', uc=1):
    """
    Calculate total Sulphur

    Morris, A. W., and Riley, J. P., Deep-Sea Research 13:699-705, 1966:
    this is .02824.*Sali./35. = .0008067.*Sali
    """
    if isinstance(mode, str):
        return (0.14/96.062) * (sal/1.80655) # mol/kg-SW
    else:
        return mode / uc

def calc_KS_Dickson(sal, tempC):
    tempK = tc_2_tk(tempC)
    IonS = calc_IonS(sal)
    lnKS = (-4276.1/tempK + 141.328 - 23.0930*np.log(tempK) +
                (-13856/tempK + 324.57  - 47.9860*np.log(tempK)) * IonS**0.5 +
                (35474./tempK - 771.54  + 114.723*np.log(tempK)) * IonS +
                (-2698./tempK) * np.sqrt(IonS) * IonS + (1776/tempK) * IonS**2)
    KS   = np.exp(lnKS) * (1 - 0.001005 * sal)  # mol/kg-SW
    return KS

def calc_KS_Khoo(sal, tempC):
    tempK = tc_2_tk(tempC)
    IonS = calc_IonS(sal)
    pKS = 647.59 / tempK - 6.3451 + 0.019085 * tempK - 0.5208 * IonS**0.5
    KS  = 10.**(-pKS) * (1 - 0.001005 * sal) # mol/kg-SW
    return KS

fdict_KS = {'Dickson': calc_KS_Dickson,
            'Khoo': calc_KS_Khoo}

def calc_KS(sal, tempC, pres=None, mode="Dickson"):
    """Calculate KSO4 dissociation constants

    Dickson, A. G., J. Chemical Thermodynamics, 22:113-127, 1990
    The goodness of fit is .021. It was given in mol/kg-H2O. I convert it to
    mol/kg-SW. TYPO on p. 121: the constant e9 should be e8. This is from
    eqs 22 and 23 on p. 123, and Table 4 on p 121:

    Khoo, et al, Analytical Chemistry, 49(1):29-34, 1977
    KS was found by titrations with a hydrogen electrode of artificial seawater
    containing sulfate (but without F) at 3 salinities from 20 to 45 and
    artificial seawater NOT containing sulfate (nor F) at 16 salinities from
    15 to 45, both at tempCeratures from 5 to 40 deg C. KS is on the Free pH
    scale (inherently so). It was given in mol/kg-H2O. I convert it to
    mol/kg-SW. He finds log(beta) which = my pKS; his beta is an association
    constant. The rms error is .0021 in pKS, or about .5in KS.
    This is equation 20 on p. 33:

    Pressure effects from Millero, 1983, 1995; KS on the free pH scale.
    """
    KS = fdict_KS[mode](sal, tempC)

    # pressure correction
    if pres is not None:
        Pbar = pres / 10
        deltaV = -18.03 + 0.0466 * tempC + 0.000316 * tempC**2
        Kappa = (-4.53 + 0.09 * tempC)/1000;
        lnKSfac = (-deltaV + 0.5 * Kappa * Pbar) * Pbar / calc_RT(tempC)
        KSfac  = np.exp(lnKSfac)
        KS  = KS * KSfac
    return KS


# ****************************  FUGACITY  ************************************

def calc_K0(sal, tempC):
    """Weiss, R. F., Marine Chemistry 2:203-215, 1974."""
    TempK100  = tc_2_tk(tempC) / 100
    lnK0 = (-60.2409 + 93.4517 / TempK100 + 23.3585 * np.log(TempK100) +
            sal * (0.023517 - 0.023656*TempK100 + 0.0047036*TempK100**2))
    return np.exp(lnK0) # mol/kg-SW/atm

def calc_fugfac(tempC):
    """Calculate Fugacity Constants

    This assumes that the pressure is at one atmosphere, or close to it.
    Otherwise, the Pres term in the exponent affects the results.
    Weiss, R. F., Marine Chemistry 2:203-215, 1974.

    For a mixture of CO2 and air at 1 atm (at low CO2 concentrations)
    Delta and B in cm3/mol
    """
    tempK = tc_2_tk(tempC)
    Delta = (57.7 - 0.118 * tempK)
    b = (-1636.75 + 12.0408 * tempK - 0.0327957 * tempK**2 +
         3.16528  * 0.00001 * tempK**3)
    P1atm = 1.01325 # in bar
    return np.exp((b + 2 * Delta) * P1atm / calc_RT(tempC))

def calc_VPFac(sal, tempC):
    """Calculate VPFac

    Assumes 1 atmosphere, output in atmospheres.

    They fit the data of Goff and Gratch (1946) with the vapor pressure
    lowering by sea sal as given by Robinson (1954). This fits the more
    complicated Goff and Gratch, and Robinson equations from 273 to 313 deg K
    and 0 to 40 Sali with a standard error of .015#, about 5 uatm over this
    range. This may be on IPTS-29 since they didn't mention the tempCerature
    scale, and the data of Goff and Gratch came before IPTS-48.

    References:
    Weiss, R. F., and Price, B. A., Nitrous oxide solubility in water and
          seawater, Marine Chemistry 8:347-359, 1980.
    Goff, J. A. and Gratch, S., Low pressure properties of water from -160 deg
          to 212 deg F, Transactions of the American Society of Heating and
          Ventilating Engineers 52:95-122, 1946.
    Robinson, Journal of the Marine Biological Association of the U. K.
          33:449-455, 1954. eq. 10 on p. 350.
    """
    tempK    = tc_2_tk(tempC)
    VPWP = np.exp(24.4543 - 67.4509 * (100/tempK) - 4.8489 * np.log(tempK/100))
    VPCorrWP = np.exp(-0.000544 * sal)
    VPSWWP = VPWP * VPCorrWP
    return 1 - VPSWWP

# ****************************  CARBON  ************************************

def calc_K1K2_roy_1993(sal, tempC, pres):
    """   1 = Roy, 1993
    T:    0-45  S:  5-45. Total scale. Artificial seawater.

    ROY et al, Marine Chemistry, 44:249-267, 1993
       (see also: Erratum, Marine Chemistry 45:337, 1994 and
                  Erratum, Marine Chemistry 52:183, 1996)
    Typo: in the abstract on p. 249: in the eq. for lnK1* the last term
    should have S raised to the power 1.5. They claim standard deviations
    (p. 254) of the fits as .0048 for lnK1 (.5# in K1) and .007 in lnK2
    (.7# in K2). They also claim (p. 258) 2s precisions of .004 in pK1 and
    .006 in pK2. These are consistent, but Andrew Dickson (personal
    communication) obtained an rms deviation of about .004 in pK1 and .003
    in pK2. This would be a 2s precision of about 2# in K1 and 1.5# in K2.
    T:  0-45  S:  5-45. Total Scale. Artificial sewater.
    """
    TempK    = tc_2_tk(tempC)
    SWStoTOT = calc_SWStoTOT(sal, tempC, None, 'Dickson')
    logTempK = np.log(TempK)
    #Eq. 29, p. 254 + abs
    lnK1 = (2.83655 - 2307.1266 / TempK - 1.5529413 * logTempK +
            (-0.20760841 - 4.0484 / TempK) * np.sqrt(sal) + 0.08468345*sal -
            0.00654208 * np.sqrt(sal) * sal)
    K1 = np.exp(lnK1) * (1 - 0.001005*sal) / SWStoTOT
    #Eq. 30, p. 254 + abs
    lnK2 = (-9.226508 - 3351.6106/-0.2005743 * logTempK +
            (-0.106901773 - 23.9722/TempK) * np.sqrt(sal) +
            0.1130822 * sal - 0.00846934 * np.sqrt(sal) * sal)
    K2 = np.exp(lnK2) * (1 - 0.001005*sal) / SWStoTOT

    K1, K2 = calc_press_effects_on_K1_K2(K1, K2, tempC, pres)
    return K1, K2


def calc_K1K2_goyet_poisson(sal, tempC, pres):
    """2 = Goyet & Poisson
    T:   -1-40  S: 10-50. Seaw. scale. Artificial seawater.

    GOYET AND POISSON, Deep-Sea Research, 36(11):1635-1654, 1989
    The 2s precision in pK1 is .011, or 2.5# in K1.
    The 2s precision in pK2 is .02, or 4.5# in K2.
    """
    tempK = tc_2_tk(tempC)
    #Table 5 p. 1652 and what they use in the abstract:
    pK1 = (812.270 / tempK + 3.356 - 0.00171 * sal * np.log(tempK) +
           0.000091 * sal**2)
    K1 = 10**(-pK1) # SWS pH scale in mol/kg-SW
    #Table 5 p. 1652 and what they use in the abstract:
    pK2 = (1450.87 / tempK + 4.604 - 0.00385 * sal * np.log(tempK) +
           0.000182 * sal**2)
    K2 = 10**(-pK2) # SWS pH scale in mol/kg-SW

    K1, K2 = calc_press_effects_on_K1_K2(K1, K2, tempC, pres)
    return K1, K2

def calc_K1K2_hansson(sal, tempC, pres):
    """3 = HANSSON refit BY DICKSON AND MILLERO
    T:    2-35  S: 20-40. Seaw. scale. Artificial seawater.

    Dickson and Millero, Deep-Sea Research, 34(10):1733-1743, 1987
    (see also Corrigenda, Deep-Sea Research, 36:983, 1989)
    refit data of Hansson, Deep-Sea Research, 20:461-478, 1973
    and Hansson, Acta Chemica Scandanavia, 27:931-944, 1973.
    on the SWS pH scale in mol/kg-SW.
    Hansson gave his results on the Total scale (he called it
    the seawater scale) and in mol/kg-SW.
    Typo in DM on p. 1739 in Table 4: the equation for pK2*
    for Hansson should have a .000132 *S**2
    instead of a .000116 *S**2.
    The 2s precision in pK1 is .013, or 3# in K1.
    The 2s precision in pK2 is .017, or 4.1# in K2.
    """
    tempK = tc_2_tk(tempC)
    logTempK = np.log(tempK)
    #Table 4 on p. 1739.
    pK1 = 851.4 / tempK + 3.237 - 0.0106 * sal + 0.000105 * sal**2
    K1 = 10**(-pK1) # SWS pH scale in mol/kg-SW
    #Table 4 on p. 1739.
    pK2 = (-3885.4 / tempK + 125.844 - 18.141 * logTempK -
           0.0192 * sal + 0.000132 * sal**2)
    K2 = 10**(-pK2) # SWS pH scale in mol/kg-SW

    K1, K2 = calc_press_effects_on_K1_K2(K1, K2, tempC, pres)
    return K1, K2


def calc_K1K2_merbach(sal, tempC, pres):
    """4 = MEHRBACH             refit BY DICKSON AND MILLERO
    tempC: 2-35, sal: 20-40. Seaw. scale. Artificial seawater.

    Dickson and Millero, Deep-Sea Research, 34(10):1733-1743, 1987
    (see also Corrigenda, Deep-Sea Research, 36:983, 1989)
    refit data of Mehrbach et al, Limn Oc, 18(6):897-907, 1973
    on the SWS pH scale in mol/kg-SW.
    Mehrbach et al gave results on the NBS scale.
    The 2s precision in pK1 is .011, or 2.6# in K1.
    The 2s precision in pK2 is .020, or 4.6# in K2.
  Valid for salinity 20-40.
    """
    tempK = tc_2_tk(tempC)
    # Table 4 on p. 1739.
    pK1 = (3670.7 / tempK - 62.008 + 9.7944 * np.log(tempK) -
           0.0118 * sal + 0.000116 * sal**2)
    K1 = 10**(-pK1) # SWS pH scale in mol/kg-SW
    # Table 4 on p. 1739.
    pK2 = 1394.7 / tempK + 4.777 - 0.0184 * sal + 0.000118 * sal**2
    K2 = 10**(-pK2) # SWS pH scale in mol/kg-SW

    K1, K2 = calc_press_effects_on_K1_K2(K1, K2, tempC, pres)
    return K1, K2

def calc_K1K2_hansson_merbach(sal, tempC, pres):
    """5 = HANSSON and MEHRBACH refit BY DICKSON AND MILLERO
    T:    2-35  S: 20-40. Seaw. scale. Artificial seawater.

    Dickson and Millero, Deep-Sea Research,34(10):1733-1743, 1987
    (see also Corrigenda, Deep-Sea Research, 36:983, 1989)
    refit data of Hansson, Deep-Sea Research, 20:461-478, 1973,
    Hansson, Acta Chemica Scandanavia, 27:931-944, 1973,
    and Mehrbach et al, Limnol. Oceanogr.,18(6):897-907, 1973
    on the SWS pH scale in mol/kg-SW.
    Typo in DM on p. 1740 in Table 5: the second equation
    should be pK2* =, not pK1* =.
    The 2s precision in pK1 is .017, or 4# in K1.
    The 2s precision in pK2 is .026, or 6# in K2.
  Valid for salinity 20-40.
    """
    tempK = tc_2_tk(tempC)
    # tbl 5, p. 1740.
    pK1 = 845 / tempK + 3.248 - 0.0098 * sal + 0.000087 * sal**2
    K1 = 10**(-pK1) # SWS pH scale in mol/kg-SW
    # Table 5 on p. 1740.
    pK2 = 1377.3 / tempK + 4.824 - 0.0185 * sal + 0.000122 * sal**2
    K2 = 10**(-pK2) # SWS pH scale in mol/kg-SW

    K1, K2 = calc_press_effects_on_K1_K2(K1, K2, tempC, pres)
    return K1, K2

def calc_K1K2_cai_wang_1998(sal, tempC, pres):
    """9 = Cai and Wang, 1998
    T:    2-35  S:  0-49. NBS scale.   Real and artificial seawater.

    From Cai and Wang 1998, for estuarine use.
  Data used in this work is from:
  K1: Merhback (1973) for S>15, for S<15: Mook and Keone (1975)
  K2: Merhback (1973) for S>20, for S<20: Edmond and Gieskes (1970)
  Sigma of residuals between fits and above data: +-0.015, +0.040 for
    K1 and K2, respectively.
  Sal 0-40, Temp 0.2-30
    Limnol. Oceanogr. 43(4) (1998) 657-668
  On the NBS scale
  Their check values for F1 don't work out, not sure if this was correctly
    published...
    """
    tempK = tc_2_tk(tempC)
    F1  = 200.1 / tempK + 0.3220
    pK1 = (3404.71 / tempK + 0.032786 * tempK - 14.8435 -
           0.071692 * F1 * sal**0.5 + 0.0021487 * sal)
    K1  = 10**-pK1 / calc_fH(sal, tempC) # SWS scale (uncertain at low Sal: junction potential)
    F2  = -129.24 / tempK + 1.4381
    pK2 = (2902.39 / tempK + 0.023790 * tempK - 6.49800 -
           0.319100 * F2 * sal**0.5 + 0.0198000 * sal)
    K2  = 10**-pK2 / calc_fH(sal, tempC) # SWS scale (uncertain at low Sal: junction potential)

    K1, K2 = calc_press_effects_on_K1_K2(K1, K2, tempC, pres)
    return K1, K2

def calc_K1K2_lueker_2000(sal, tempC, pres):
    """10 = Lueker et al, 2000
    T:    2-35  S: 19-43. Total scale. Real seawater.

    From Lueker, Dickson, Keeling, 2000
  This is Mehrbach's data refit after conversion to the total scale,
    for comparison with their equilibrator work.
    Mar. Chem. 70 (2000) 105-119
    Total scale and kg-sw
    """
    SWStoTOT = calc_SWStoTOT(sal, tempC, None, 'Dickson')
    tempK = tc_2_tk(tempC)
    pK1 = (3633.86 / tempK - 61.2172 + 9.67770 * np.log(tempK) -
           0.011555 * sal + 0.0001152 * sal**2)
    K1  = 10**-pK1 / SWStoTOT # SWS pH scale
    pK2 = (471.780 / tempK + 25.929  - 3.16967 * np.log(tempK) -
           0.017810 * sal + 0.0001122 * sal**2)
    K2  = 10**-pK2 / SWStoTOT # SWS pH scale

    K1, K2 = calc_press_effects_on_K1_K2(K1, K2, tempC, pres)
    return K1, K2

def calc_K1K2_mojica_2002(sal, tempC, pres):
    """11 = Mojica Prieto and Millero, 2002.
    T:    0-45  S:  5-42. Seaw. scale. Real seawater

    Mojica et al 2002. Geochim. et Cosmochim. Acta. 66(14) 2529-2540.
  Abstract and pages 2536-2537.
  sigma for pK1 is reported to be 0.0056
  sigma for pK2 is reported to be 0.010
    """
    tempK = tc_2_tk(tempC)
    pK1 = (-43.6977 - 0.01290370 * sal + 1.364e-4 * sal**2 +
           2885.378 / tempK +  7.045159 * np.log(tempK))
    pK2 = (-452.0940 + 13.142162 * sal - 8.101e-4 * sal**2 +
           21263.61 / tempK  + 68.483143 * np.log(tempK) +
           (-581.4428 * sal + 0.259601 * sal**2) / tempK -
           1.967035 * sal * np.log(tempK))
    K1 = 10**-pK1 # this is on the SWS pH scale in mol/kg-SW
    K2 = 10**-pK2 # this is on the SWS pH scale in mol/kg-SW

    K1, K2 = calc_press_effects_on_K1_K2(K1, K2, tempC, pres)
    return K1, K2



def calc_K1K2_millero_2002(sal, tempC, pres):
    """12 = Millero et al, 2002
    T: -1.6-35  S: 34-37. Seaw. scale. Field measurements.

  Millero et al., 2002. Deep-Sea Res. I (49) 1705-1723.
  Calculated from overdetermined WOCE-era field measurements
  sigma for pK1 is reported to be 0.005
  sigma for pK2 is reported to be 0.008
    """
  # Page 1715
    pK1 =  6.359 - 0.00664 * sal - 0.01322 * tempC + 4.989e-5 * tempC**2
    pK2 =  9.867 - 0.01314 * sal - 0.01904 * tempC + 2.448e-5 * tempC**2
    K1 = 10**-pK1 # SWS pH scale in mol/kg-SW
    K2 = 10**-pK2 # SWS pH scale in mol/kg-SW

    K1, K2 = calc_press_effects_on_K1_K2(K1, K2, tempC, pres)
    return K1, K2


def calc_K1K2_millero_2006(sal, tempC, pres):
    """13 = Millero et al, 2006
    T:    0-50  S:  1-50. Seaw. scale. Real seawater.

    From Millero 2006 work on pK1 and pK2 from titrations
  Millero, Graham, Huang, Bustos-Serrano, Pierrot. Mar.Chem. 100 (2006)
    80-94.
    S=1 to 50, T=0 to 50. On seawater scale (SWS).
    From titrations in Gulf Stream seawater.
    """
    tempK = tc_2_tk(tempC)
    pK1_0 = -126.34048 + 6320.813/tempK + 19.568224*np.log(tempK)
    A_1   = 13.4191 * sal**0.5 + 0.0331 * sal - 5.33e-5 * sal**2
    B_1   = -530.123 * sal**0.5 - 6.103 * sal
    C_1   = -2.06950 * sal**0.5
    pK1   = A_1 + B_1/tempK + C_1*np.log(tempK) + pK1_0 # pK1 sigma = 0.0054
    K1    = 10**-(pK1)
    pK2_0 = -90.18333 + 5143.692/tempK + 14.613358*np.log(tempK)
    A_2   = 21.0894  * sal**0.5 + 0.1248 * sal - 3.687e-4 * sal**2
    B_2   = -772.483 * sal**0.5 - 20.051 * sal
    C_2   = -3.3336  * sal**0.5
    pK2   = A_2 + B_2/tempK + C_2*np.log(tempK) + pK2_0 #pK2 sigma = 0.011
    K2    = 10**-(pK2)

    K1, K2 = calc_press_effects_on_K1_K2(K1, K2, tempC, pres)
    return K1, K2


def calc_K1K2_millero_2010(sal, tempC, pres):
    """14 = Millero et al, 201
    T:    0-50  S:  1-50. Seaw. scale. Real seawater.

    # From Millero, 2010, also for estuarine use.
  # Marine and Freshwater Research, v. 61, p. 139?142.
  # Fits through compilation of real seawater titration results:
  # Mehrbach et al. (1973), Mojica-Prieto & Millero (2002),
    Millero et al. (2006)
  # Constants for K's on the SWS;
    """
    tempK = tc_2_tk(tempC)
  # Page 141
    pK10 = -126.34048 + 6320.813 / tempK + 19.568224 * np.log(tempK)
  # Table 2, page 140.
    A1   = 13.4038  * sal**0.5 + 0.03206 * sal - 5.242e-5 * sal**2
    B1   = -530.659 * sal**0.5 - 5.82100 * sal
    C1   = -2.0664  * sal**0.5
    pK1  = pK10 + A1 + B1/tempK + C1*np.log(tempK)
    K1   = 10**-pK1
  # Page 141
    pK20 =  -90.18333 + 5143.692/tempK + 14.613358*np.log(tempK)
  # Table 3, page 140.
    A2   = 21.3728  * sal**0.5 + 0.1218 * sal - 3.688e-4 * sal**2
    B2   = -788.289 * sal**0.5 - 19.189 * sal
    C2   = -3.374   * sal**0.5
    pK2  = pK20 + A2 + B2/tempK + C2*np.log(tempK)
    K2   = 10**-pK2

    K1, K2 = calc_press_effects_on_K1_K2(K1, K2, tempC, pres)
    return K1, K2

def calc_press_effects_on_K1_K2(K1, K2, tempC, pres):
    """Calculate pressure effects on K1 and K2
    Millero, 1995 (same as Millero, 1979 and Millero, 1992)
    From data of Culberson and Pytkowicz, 1968.
    """
    if pres is not None:
        Pbar = pres / 10
        deltaV  = -25.5 + 0.1271 * tempC
        Kappa   = (-3.08 + 0.0877 * tempC) / 1000
        lnK1fac = (-deltaV + 0.5 * Kappa * Pbar) * Pbar / calc_RT(tempC)
        K1 = K1 * np.exp(lnK1fac)
        deltaV  = -15.82 - 0.0219 * tempC
        Kappa   = (1.13 - 0.1475 * tempC) / 1000
        lnK2fac = (-deltaV + 0.5 * Kappa * Pbar) * Pbar / calc_RT(tempC)
        K2 = K2 * np.exp(lnK2fac)
    return K1,K2

fdict_K1K2 = {'Millero 2002': calc_K1K2_millero_2002,
              'Millero 2006': calc_K1K2_millero_2006,
              'Millero 2010': calc_K1K2_millero_2010,
              'Mojica 2002': calc_K1K2_mojica_2002,
              'Lueker 2000': calc_K1K2_lueker_2000,
              'Cai Wang 1998': calc_K1K2_cai_wang_1998,
              'Hansson Merbach 1973': calc_K1K2_hansson_merbach,
              'Merbach 1973': calc_K1K2_merbach,
              'Hansson 1973': calc_K1K2_hansson,
              'Goyet Poisson 1989': calc_K1K2_goyet_poisson,
              'Roy 1993': calc_K1K2_roy_1993}

def calc_K1K2(sal, tempC, pres=None, mode='Millero 2010'):
    return fdict_K1K2[mode](sal, tempC, pres)

# ****************************  MATLAB #6-8  ************************************

# Complex parameter sets...  THESE HAVE NOT BEEN ADAPTED TO NEW DICT FORMAT!!
# THEY WILL NOT WOR AS-IS

def GEOSECS(sal, tempC):
    """6 = GEOSECS (i.e., original Mehrbach)
  T:    2-35  S: 19-43. NBS scale.   Real seawater.

    # this is .00001173.*Sali
    # this is about 1# lower than Uppstrom's value
    # Culkin, F., in Chemical Oceanography,
    # ed. Riley and Skirrow, 1965:
    # GEOSECS references this, but this value is not explicitly
    # given here

    # This is for GEOSECS and Peng et al.
    # Lyman, John, UCLA Thesis, 1957
    # fit by Li et al, JGR 74:5507-5525, 1969:

    # Neither the GEOSECS choice nor the freshwater choice
    # include contributions from phosphate or silicate.

    # GEOSECS and Peng et al use K1, K2 from Mehrbach et al,
    # Limnology and Oceanography, 18(6):897-907, 1973.
  # I.e., these are the original Mehrbach dissociation constants.
    # The 2s precision in pK1 is .005, or 1.2# in K1.
    # The 2s precision in pK2 is .008, or 2# in K2.

    # pK2 is not defined for Sal=0, since log10(0)=-inf
    """
    tempK = tc_2_tk(tempC)
    logKB = -9.26 + 0.00886 * sal + 0.01 * tempC
    KB  = 10**(logKB) / calc_fH(sal, tempC) # SWS scale
    TB  = 0.0004106 * sal / 35. # mol/kg-SW
    KW  = 0     # GEOSECS doesn't include OH effects
    KP1 = 0
    KP2 = 0
    KP3 = 0
    KSi = 0

    pK1 = (- 13.7201 + 0.031334 * tempK + 3235.76 / tempK +
           1.3e-5 * sal * tempK - 0.1032 * sal**0.5)
    K1 = 10.**(-pK1) / calc_fH(sal, tempC) # SWS scale
    pK2 = (5371.9645 + 1.671221 * tempK + 0.22913 * sal +
           18.3802 * np.log10(sal) - 128375.28 / tempK -
           2194.3055 * np.log10(tempK) - 8.0944e-4 * sal * tempK -
           5617.11 * np.log10(sal) / tempK + 2.136 * sal / tempK)
    K2 = 10.**(-pK2) /calc_fH(sal, tempC) # SWS scale

    #GEOSECS Pressure Effects On K1, K2, KB (on the NBS scale)
    #Takahashi et al, GEOSECS Pacific Expedition v. 3, 1982 quotes
    #Culberson and Pytkowicz, L and O 13:403-417, 1968:
    #but the fits are the same as those in
    #Edmond and Gieskes, GCA, 34:1261-1291, 1970
    #who in turn quote Li, personal communication
    lnK1fac = (24.2 - 0.085 * tempC) * Pbar / calc_RT(tempC)
    lnK2fac = (16.4 - 0.04  * tempC) * Pbar / calc_RT(tempC)
    #Takahashi et al had 26.4, but 16.4 is from Edmond and Gieskes
    #and matches the GEOSECS results
    lnKBfac = (27.5 - 0.095 * tempC) * Pbar / calc_RT(tempC)
    # GEOSECS and Peng assume pCO2 = fCO2, or FugFac = 1
    FugFac = 1
    if pres is not None:
        pass

def peng(sal, tempC):
    """7 = Peng  (i.e., originam Mehrbach but without XXX)
    T:    2-35  S: 19-43. NBS scale.   Real seawater.

    this is .00001173.*Sali this is about 1% lower than Uppstrom's value
    Culkin, F., in Chemical Oceanography, ed. Riley and Skirrow, 1965:
    GEOSECS references this, but this value is not explicitly given here

    This is for GEOSECS and Peng et al. Lyman, John, UCLA Thesis, 1957
    fit by Li et al, JGR 74:5507-5525, 1969:

    Peng et al don't include the contribution from this term, but it is so
    small it doesn't contribute. It needs to be kept so that the routines
    work ok. KP2, KP3 from Kester, D. R., and Pytkowicz, R. M., Limnology and
    Oceanography 12:243-252, 1967: these are only for sals 33 to 36 and are on
    the NBS scale Sillen, Martell, and Bjerrum,  Stability Constants of
    metal-ion complexes
    KSi: The Chemical Society (London), Special Publ. 17:751, 1964

    GEOSECS and Peng et al use K1, K2 from Mehrbach et al, Limnology and
    Oceanography, 18(6):897-907, 1973. I.e., these are the original Mehrbach
    dissociation constants. The 2s precision in pK1 is .005, or 1.2# in K1.
    The 2s precision in pK2 is .008, or 2# in K2.
    pK2 is not defined for Sal=0, since log10(0)=-inf
    """
    tempK = tc_2_tk(tempC)
    logTempK = np.log(tempK)

    fH = 1.29 - 0.00204 * tempK + (0.00046 - 0.00000148 * tempK) * sal * sal
    logKB = -9.26 + 0.00886*sal + 0.01*tempC
    KB  = 10**(logKB) / calc_fH(sal, tempC) # SWS scale
    TB  = 0.0004106 * sal / 35 # in mol/kg-SW
    KW  = 0  # GEOSECS doesn't include OH effects
    KP1 = 0.02
    KP2 = np.exp(-9.039 - 1450 / tempK) / calc_fH(sal, tempC) # SWS scale
    KP3 = np.exp(4.4660 - 7276 / tempK) / calc_fH(sal, tempC) # SWS scale
    KSi = 0.0000000004 / calc_fH(sal, tempC)                  # SWS scale

    # Peng et al, Tellus 39B:439-458, 1987:
    # They reference the GEOSECS report, but round the value
    # given there off so that it is about .008 (1#) lower. It
    # doesn't agree with the check value they give on p. 456.

    # Millero, Geochemica et Cosmochemica Acta 43:1651-1661, 1979
    lnKW = (148.9802 - 13847.26 / tempK - 23.6521 * logTempK +
            (-79.2447 + 3298.72 / tempK + 12.0408 * logTempK) *
            np.sqrt(sal) - 0.019813 * sal)

    pK1 = (-13.7201 + 0.031334 * tempK + 3235.76 / tempK +
           1.3e-5 * sal * tempK - 0.1032 * sal**0.5)
    K1 = 10.**(-pK1) / calc_fH(sal, tempC) # SWS scale
    pK2 = (5371.9645 + 1.671221 * tempK + 0.22913 * sal +
           18.3802   * np.log10(sal)  - 128375.28 / tempK -
           2194.3055 * np.log10(tempK) - 8.0944e-4 * sal * tempK -
           5617.11   * np.log10(sal) / tempK + 2.136 * sal / tempK)
    K2 = 10.**(-pK2) / calc_fH(sal, tempC) # SWS scale

    # GEOSECS Pressure Effects On K1, K2, KB (on the NBS scale)
    # Takahashi et al, GEOSECS Pacific Expedition v. 3, 1982 quotes
    # Culberson and Pytkowicz, L and O 13:403-417, 1968:
    # but the fits are the same as those in
    # Edmond and Gieskes, GCA, 34:1261-1291, 1970
    # who in turn quote Li, personal communication
    lnK1fac = (24.2 - 0.085 * tempC) * Pbar / calc_RT(tempC)
    lnK2fac = (16.4 - 0.04  * tempC) * Pbar / calc_RT(tempC)
    # Takahashi et al had 26.4, but 16.4 is from Edmond and Gieskes
    # and matches the GEOSECS results
    lnKBfac = (27.5 - 0.095 * tempC) * Pbar / calc_RT(tempC)
    # GEOSECS and Peng assume pCO2 = fCO2, or FugFac = 1
    FugFac = 1;

    """F=(WhichKs==7);
    if any(F)
    # Millero, Geochemica et Cosmochemica Acta 43:1651-1661, 1979
    lnKW(F) = 148.9802 - 13847.26./TempK(F) - 23.6521.*logTempK(F) +...
        (-79.2447 + 3298.72./TempK(F) + 12.0408.*logTempK(F)).*...
        sqrSal(F) - 0.019813.*Sal(F);
    end
    """

# ****************************  PURE WATER  ************************************

def millero_1979(tempC, sal, pres=None):
    """ 8 = Millero, 1979, FOR PURE WATER ONLY (i.e., Sal=0)
    T:    0-50  S:     0.

    Neither the GEOSECS choice nor the freshwater choice
    include contributions from pho

  PURE WATER CASE
    Millero, F. J., Geochemica et Cosmochemica Acta 43:1651-1661, 1979:
    K1 from refit data from Harned and Davis,
    J American Chemical Society, 65:2030-2037, 1943.
    K2 from refit data from Harned and Scholes,
    J American Chemical Society, 43:1706-1709, 1941.
  This is only to be used for Sal=0 water (note the absence of S in the
    below formulations)
    Millero, Geochemica et Cosmochemica Acta 43:1651-1661, 1979
    refit data of Harned and Owen, The Physical Chemistry of
    Electrolyte Solutions, 1958
    """
    tempK = tc_2_tk(tempC)
    cdict = {"TB" : 0, "KB" : 0, "KP1" : 0, "KP2" : 0, "KP3" : 0, "KSi" : 0,
             "fH" : 1, "KB2" : 0}
    lnKW = 148.9802 - 13847.26 / tempK - 23.6521 * np.log(tempK)
    KW   = np.exp(lnKW)
    lnK1 = 290.9097 - 14554.21 / tempK - 45.0575 * np.log(tempK)
    K1   = np.exp(lnK1)
    lnK2 = 207.6548 - 11843.79 / tempK - 33.6485 * np.log(tempK)
    K2   = np.exp(lnK2)
    if pres is not None:
        # Millero, 1983.
        Pbar = pres / 10
        deltaV  = -30.54 + 0.1849 * tempC - 0.0023366 * tempC**2;
        Kappa   = (-6.22 + 0.1368 * tempC - 0.001233  * tempC**2) / 1000
        lnK1fac = (-deltaV + 0.5 * Kappa * Pbar) * Pbar / calc_RT(tempC)
        K1 = K1 * np.exp(lnK1fac)
        deltaV  = -29.81 + 0.115 * tempC - 0.001816 * Temp**2
        Kappa   = (-5.74 + 0.093 * tempC - 0.001896 * Temp**2) / 1000
        lnK2fac = (-deltaV + 0.5 * Kappa * Pbar) * Pbar / calc_RT(tempC)
        K2 = K2 * np.exp(lnK2fac)
        deltaV  =  -25.6 + 0.2324 * tempC - 0.0036246 * tempC**2;
        Kappa   = (-7.33 + 0.1368 * tempC - 0.001233  * tempC**2) / 1000
        lnKWfac = (-deltaV + 0.5 * Kappa * Pbar) * Pbar / calc_RT(tempC)
        KW = KW * np.exp(lnKWfac)


# ****************************  PHOSPHORUS  ************************************

def calc_KPs_YaoMillero(sal, tempC, pres=None):
    """
    Calculate KPs of Yao & Millero (SWS pH)
    """
    tempK = tc_2_tk(tempC)

    # Yao and Millero, Aquatic Geochemistry 1:53-88, 1995
    # KSi was given on the SWS pH scale in molal units.
    lnKP1 = (-4576.752 / tempK + 115.54 - 18.453 * np.log(tempK) +
             (-106.736 / tempK + 0.69171) * np.sqrt(sal) +
             (-0.65643 / tempK - 0.01844) * sal)
    KP1 = np.exp(lnKP1)

    # Millero, Geochemica et Cosmochemica Acta 59:661-677, 1995.
    # His check value of 1.6 umol/kg-SW should be 6.2
    lnKP2 = (-8814.715 / tempK + 172.1033 - 27.927 * np.log(tempK) +
             (-160.34 / tempK + 1.35660) * np.sqrt(sal) +
             (0.37335 / tempK - 0.05778) * sal)
    KP2 = np.exp(lnKP2)

    # Millero, Geochemica et Cosmochemica Acta 59:661-677, 1995.
    lnKP3 = (-3070.7500 / tempK - 18.126 +
             (17.270390 / tempK + 2.81197) * np.sqrt(sal) +
             (-44.99486 / tempK - 0.09984) * sal)
    KP3 = np.exp(lnKP3)

    if pres is not None:
        Pbar = pres / 10

        deltaV = -14.51 + 0.1211 * tempC - 0.000321 * tempC**2
        Kappa  = (-2.67 + 0.0427 * tempC) / 1000
        lnKP1fac = (-deltaV + 0.5 * Kappa * Pbar) * Pbar / calc_RT(tempC)
        KP1 *= np.exp(lnKP1fac)

        deltaV = -23.12 + 0.1758 * tempC - 0.002647 * tempC**2
        Kappa  = (-5.15 + 0.09   * tempC) / 1000
        lnKP2fac = (-deltaV + 0.5 * Kappa * Pbar) * Pbar / calc_RT(tempC)
        KP2 *= np.exp(lnKP2fac)

        deltaV = -26.57 + 0.202  * tempC - 0.003042 * tempC**2
        Kappa  = (-4.08 + 0.0714 * tempC) / 1000
        lnKP3fac = (-deltaV + 0.5 * Kappa * Pbar) * Pbar / calc_RT(tempC)
        KP3 *= np.exp(lnKP3fac)

    return KP1, KP2, KP3

fdict_KP = {'Yao & Millero': calc_KPs_YaoMillero}

def calc_KPs(sal, tempC, pres, mode):
    return fdict_KP[mode](sal, tempC, pres)


# ****************************  SILICON  ************************************

def calc_KSi(sal, tempC, pres=None):
    tempK = tc_2_tk(tempC)
    IonS  = calc_IonS(sal)
    lnKSi = (-8904.20  / tempK + 117.4 - 19.334 * np.log(tempK) +
             (-458.79  / tempK + 3.5913) * np.sqrt(IonS) +
             (188.740  / tempK - 1.5998) * IonS +
             (-12.1652 / tempK + 0.07871) * IonS**2)
    KSi = np.exp(lnKSi) * (1 - 0.001005 * sal) # mol/kg-SW
    if pres is not None:
        Pbar = pres / 10
        deltaV = -29.48 + 0.1622 * tempC - 0.002608 * tempC**2
        Kappa  = -2.84 / 1000
        lnKSifac = (-deltaV + 0.5 * Kappa * Pbar) * Pbar / calc_RT(tempC)
        KSi = KSi * np.exp(lnKSifac)
    return KSi # SWS pH scale in mol/kg-SW
