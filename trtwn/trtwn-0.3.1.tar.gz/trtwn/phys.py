import numpy as np
import scipy.constants as sc

def spp_dispersion_relation_from_w(w, e_1, e_2):
    return w/sc.c * np.sqrt(e_1 * e_2/(e_1 + e_2))

def bulk_plasmon_dispersion_relation_from_w(w, w_p):
    return np.sqrt((w**2-w_p**2)/sc.c**2)

def bulk_plasmon_dispersion_relation_from_k(k, w_p):
    return np.sqrt(w_p**2 + k**2 * sc.c**2)

def nm_to_eV(nm):
    return sc.h*sc.c/(nm * sc.e * sc.nano)

def eV_to_nm(eV):
    return sc.h*sc.c/(eV * sc.e * sc.nano)
