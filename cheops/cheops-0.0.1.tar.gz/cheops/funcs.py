"""
funcs
=====
Functions relating observable properties of binary stars and exoplanet 
systems to their fundamental properties, and vice versa.

Parameters
----------
Functions are defined in terms of the following parameters. [1]

* a          - orbital semi-major axis in solar radii = a_1 + a_2 
* P          - orbital period in mean solar days
* M          - total system mass in solar masses, M = m_1 + m_2
* e          - orbital eccentricity
* sini       - sine of the orbital inclination 
* K          - 2.pi.a.sini/(P.sqrt(1-e^2)) = K_1 + K_2
* K_1, K_2   - orbital semi-amplitudes in km/s
* q          - mass ratio = m_2/m_1 = K_1/K_2 = a_1/a_2
* f_m        - mass function = m_2^3.sini^3/(m_1+m_2)^2 in solar masses 
                             = K_1^3.P/(2.pi.G).(1-e^2)^(3/2)
* r_1        - radius of star 1 in units of the semi-major axis, r_1 = R_*/a
* rho_1      - mean stellar density = 3.pi/(GP^2(1+q)r_1^3)
  
.. rubric References
.. [1] Hilditch, R.W., An Introduction to Close Binary Stars, CUP 2001.


Functions 
---------

"""

from __future__ import (absolute_import, division, print_function,
                                unicode_literals)
from .constants import *
from numpy import roots, imag, real, vectorize, isscalar, arcsin, sqrt, pi

__all__ = [ 'a_rsun','f_m','m1sin3i','m2sin3i','asini','rhostar',
        'K_kms','m_comp','transit_width']

_arsun   = (GM_SunN*mean_solar_day**2/(4*pi**2))**(1/3.)/R_SunN
_f_m     = mean_solar_day*1e9/(2*pi)/GM_SunN
_asini   = mean_solar_day*1e3/2/pi/R_SunN
_rhostar = 3*pi*V_SunN/(GM_SunN*mean_solar_day**2)

def a_rsun(P, M):
    """
    Semi-major axis in solar radii

    :param P: orbital period in mean solar days
    :param M: total mass in solar masses

    :returns: a = (G.M.P^2/(4.pi^2))^(1/3) in solar radii
    
    """

    return _arsun * P**(2/3.) * M**(1/3.)

def f_m(P, K, e=0):
    """
    Mass function in solar masses

    :param P: orbital period in mean solar days
    :param K: semi-amplitude of the spectroscopic orbit in km/s
    :param e: orbital eccentricity

    :returns: f_m =  m_2^3.sini^3/(m_1+m_2)^2  in solar masses
    """
    return _f_m * K**3 * P * (1 - e**2)**1.5

def m1sin3i(P, K_1, K_2, e=0):
    """
     Reduced mass of star 1 in solar masses

     :param K_1: semi-amplitude of star 1 in km/s
     :param K_2: semi-amplitude of star 2 in km/s
     :param P: orbital period in mean solar days
     :param e:  orbital eccentricity

     :returns: m_1.sini^3 in solar masses 
    """
    return _f_m * K_2 * (K_1 + K_2)**2 * P * (1 - e**2)**1.5

def m2sin3i(P, K_1, K_2, e=0):
    """
     Reduced mass of star 2 in solar masses

     :param K_1:  semi-amplitude of star 1 in km/s
     :param K_2:  semi-amplitude of star 2 in km/s
     :param P:   orbital period in mean solar days
     :param e:   orbital eccentricity

     :returns: m_2.sini^3 in solar masses 
    """
    return _f_m * K_1 * (K_1 + K_2)**2 * P * (1 - e**2)**1.5

def asini(K, P, e=0):
    """
     a.sini in solar radii

     :param K: semi-amplitude of the spectroscopic orbit in km/s
     :param P: orbital period in mean solar days

     :returns: a.sin(i) in solar radii

    """
    return _asini * K * P 

def rhostar(r_1, P, q=0):
    """ 
    Mean stellar density in solar masses

    :param r_1: radius of star in units of the semi-major axis, r_1 = R_*/a
    :param P: orbital period in mean solar days
    :param q: mass ratio, m_2/m_1

    :returns: Mean stellar density in solar masses

    """
    return _rhostar/(P**2*(1+q)*r_1**3)

def K_kms(m_1, m_2, P, sini, e):
    """
    Semi-amplitudes of the spectroscopic orbits in km/s
     - K = 2.pi.a.sini/(P.sqrt(1-e^2))
     - K_1 = K * m_2/(m_1+m_2)
     - K_2 = K * m_1/(m_1+m_2)

    :param m_1:  mass of star 1 in solar masses
    :param m_2:  mass of star 2 in solar masses
    :param P:  orbital period in mean solar days
    :param sini:  sine of the orbital inclination
    :param e:  orbital eccentrcity

    :returns: K_1, K_2 -- semi-amplitudes in km/s
    """
    M = m_1 + m_2
    a = a_rsun(P, M)
    K = 2*pi*a*R_SunN*sini/(P*mean_solar_day*sqrt(1-e**2))/1000
    K_1 = K * m_2/M
    K_2 = K * m_1/M
    return K_1, K_2

#---------------

def m_comp(f_m, m_1, sini):
    """
    Companion mass in solar masses given mass function and stellar mass

    :param f_m: = K_1^3.P/(2.pi.G).(1-e^2)^(3/2) in solar masses
    :param m_1: mass of star 1 in solar masses
    :param sini: sine of orbital inclination

    :returns: m_2 = mass of companion to star 1 in solar masses

    """

    def _m_comp_scalar(f_m, m_1, sini):
        for r in roots([sini**3, -f_m,-2*f_m*m_1, -f_m*m_1**2]):
            if imag(r) == 0:
                return real(r)
        raise ValueError("No finite companion mass for input values.")

    _m_comp_vector = vectorize(_m_comp_scalar )

    if isscalar(f_m) & isscalar(m_1) & isscalar(sini):
        return float(_m_comp_scalar(f_m, m_1, sini))
    else:
        return _m_comp_vector(f_m, m_1, sini)

#---------------

def transit_width(r, k, b, p=1):
    """
    Total transit duration.

    See equation (3) from Seager and Malen-Ornelas, 2003ApJ...585.1038S.

    :param r: R_star/a
    :param k: R_planet/R_star
    :param b: impact parameter = a.cos(i)/R_star
    :param p: orbital period (optional, default=1)

    :returns: Total transit duration in the same units as p.

    """

    return p*arcsin(r*sqrt( ((1+k)**2-b**2) / (1-b**2*r**2) ))/pi
