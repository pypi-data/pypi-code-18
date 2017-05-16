# -*- coding: utf-8 -*-
from __future__ import division

import numpy as np

from .control import model_setup
from .cp_confocal import threed
from .cp_mix import double_pnum


def CF_Gxyz_gauss_3D3D(parms, tau):
    u""" Two-component three-dimensional free diffusion
        with a Gaussian laser profile.

        particle1 = F₁/( (1+τ/τ₁) * sqrt(1+τ/(τ₁*SP²)))
        particle2 = α²*(1-F₁)/( (1+τ/τ₂) * sqrt(1+τ/(τ₂*SP²)))
        norm = (F₁ + α*(1-F₁))²
        G = 1/n*(particle1 + particle2)/norm + offset

        *parms* - a list of parameters.
        Parameters (parms[i]):
        [0] n       Effective number of particles in confocal volume
                    (n = n₁+n₂)
        [1] τ₁      Diffusion time of particle species 1
        [2] τ₂      Diffusion time of particle species 2
        [3] F₁      Fraction of molecules of species 1 (n₁ = n*F₁)
                    0 <= F₁ <= 1
        [4] SP      SP=z₀/r₀, Structural parameter,
                    describes elongation of the confocal volume
        [5] α       Relative molecular brightness of particle
                    2 compared to particle 1 (α = q₂/q₁)
        [6] offset
        *tau* - lag time
    """
    n=parms[0]
    taud1=parms[1]
    taud2=parms[2]
    F=parms[3]
    SP=parms[4]
    alpha=parms[5]
    off=parms[6]

    g = double_pnum(n=n,
                    F1=F,
                    alpha=alpha,
                    comp1=threed,
                    comp2=threed,
                    kwargs1={"tau":tau,
                             "taudiff":taud1,
                             "SP":SP},
                    kwargs2={"tau":tau,
                             "taudiff":taud2,
                             "SP":SP},
                    )

    G = off + g
    return G

def supplements(parms, countrate=None):
    u"""Supplementary parameters:
        [7]  n₁ = n*F₁     Particle number of species 1
        [8]  n₂ = n*(1-F₁) Particle number of species 2
    """
    # We can only give you the effective particle number
    n = parms[0]
    F1 = parms[3]
    Info = list()
    # The enumeration of these parameters is very important for
    # plotting the normalized curve. Countrate must come out last!
    Info.append([u"n\u2081", n*F1])
    Info.append([u"n\u2082", n*(1.-F1)])
    if countrate is not None:
        # CPP
        cpp = countrate/n
        Info.append(["cpp [kHz]", cpp])
    return Info


parms = [   25,      # n
            5,       # taud1
            1000,    # taud2
            0.5,     # F
            5,       # SP
            1.0,     # alpha
            0.0      # offset
            ] 

## Boundaries
# strictly positive
boundaries = [[0, np.inf]]*len(parms)
# F
boundaries[3] = [0,.9999999999999]
boundaries[-1] = [-np.inf, np.inf]


model_setup(
             modelid=6035,
             name="Separate 3D diffusion (confocal)",
             comp="3D+3D",
             mtype="Confocal (Gaussian)",
             fctn=CF_Gxyz_gauss_3D3D,
             par_labels=[
                            u"n",
                            u"τ"+u"\u2081"+" [ms]",
                            u"τ"+u"\u2082"+" [ms]",
                            u"F"+u"\u2081", 
                            u"SP",
                            u"\u03b1"+" (q"+u"\u2082"+"/q"+u"\u2081"+")", 
                            u"offset"
                            ],
             par_values=parms,
             par_vary=[True, True, True, True, False, False, False],
             par_boundaries=boundaries,
             par_constraints=[[2, ">", 1]],
             supplementary_method=supplements
            )
