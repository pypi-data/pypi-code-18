import scipy.special as sp
import numpy as np
#from _registry import *

RGAS = 8.314472

tnatrt=0.000001385
unatrt=0.00725268
U238_DECAYCT=1.55125e-10
U235_DECAYCT=9.8485e-10
TH232_DECAYCT=4.9475e-11
TH230_DECAYCT=9.24196229e-6


stdtrue235238=0.9997
stdtrue235238sg=0.0009997
avogadro=6.02214129e23


S238=18.81e-6
S235=21.80e-6
S232=22.25e-6
SUMEAN=18.83e-6

POLA238=-5.31
POLB238=6.78
POLA235=-5.9
POLB235=8.99
POLA232=-5.9
POLB232=8.99
POLAMEAN=-5.31
POLBMEAN=6.84

U238_ATOM_MASS=238.0289
U235_ATOM_MASS=235.0439
TH230_ATOM_MASS=230.0331
TH232_ATOM_MASS=232.0381
HE4_ATOM_MASS=4.003
ap_density = 3200

yr = 31556926 # Seconds in year
tau_e = 1.e6 * yr

ALPHA = sp.jn_zeros(0,300)

BesJ1 = sp.j1
BesJ0 = sp.j0
isotop = np.array([8,7,6])


lsoda_defaults = {"atol": 1e-10, 
                  "rtol": 1e-13}
dopri5_defaults = {"atol": 1e-8, 
                  "rtol": 1e-12}
vode_defaults = {"atol": 1e-8, 
                  "rtol": 1e-12}
zvode_defaults = {"atol": 1e-8, 
                  "rtol": 1e-12}
dop853_defaults = {"atol": 1e-8, 
                  "rtol": 1e-12}
