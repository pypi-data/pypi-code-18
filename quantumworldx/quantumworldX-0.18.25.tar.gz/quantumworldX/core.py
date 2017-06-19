# -*- coding: utf-8 -*-
"""qwX core functions

   Here you can find all the main functions of quantumworldX, the suggested
   way to import this module is

   ``import quantumworldX as qw``

   from there you are able to use all core functions, for example to utilize
   `pib_eigenfunction` you would use ``qw.pib_eigenfunction``.

"""


import numpy as np
import scipy as sp
from scipy import misc
from scipy.special import sph_harm
from scipy.misc import factorial
from scipy.special import genlaguerre, binom, eval_genlaguerre
from scipy.integrate import simps, quad, nquad


def pib_eigenfunction(x, l, n):
    """Particle in the box eigenfunction.

    Give a spatial array x, the length of box L and a harmonic number n, it will
    return the eigenfunction of the 1-D Particle in a box evaluated on the x grid.

    Args:
        x (:obj:`np.array`): 1-D array representing a wavefunction evaluated on a spatial
            grid.
        L (float): length of the box.
        n (int): number of the harmonic of the pib.

    Returns:
        Will return a 1-D :obj:`np.array`.

    """
    psi_x = np.sqrt(2.0 / l) * np.sin(n * np.pi * x / l)
    return psi_x


def prob_density(psi_x):
    """Probability density of a wavefunction.

    Given a wavefuntion represented as a 1-D array, it will compute the
     probability density, which is the square of the wavefuntion.

    Args:
        psi_x (:obj:`np.array`): 1-D array representing a wavefunction evaluated on a spatial
            grid.

    Returns:
        Will return a 1-D real :obj:`np.array`.

    """

    prob = np.conjugate(psi_x) * psi_x
    return prob


def pib_energy(n, L, m=1, h_bar=1):
    """Energy of particle in a box n-th eigenstate.

    Returns energy of the nth eigenstate of the 1D particle in a box.

    Args:
        n (int): The quantum number specifying the eigenstate of the pib.
        L (float): length of the box.
        m (float): mass of the particle. Defaults to 1 (atomic units).
        h_bar (float): value of plank's constant. Defaults to 1 (atomic units).

    Returns:
        Will a float representing the energy

    """
    E_n = (n * h_bar * np.pi) ** 2 / (2.0 * m * L ** 2)
    return E_n


def wfn_norm(x, psi_x):
    """Calculate norm of a wavefuntion.

    Returns the norm of a wavefunction psi_x by getting the pdf and then integrating
    over a spatial grid x.

    Args:
        x (:obj:`np.array`): 1-D array representing a spatial
            grid.
        psi_x (:obj:`np.array`): 1-D array representing a wavefunction evaluated
         on the spatial grid, show be same length as x.

    Returns:
        Will a float representing the norm of the wavefunction.

    """
    pdf = prob_density(psi_x)
    integral_norm = simps(pdf, x)
    return integral_norm


def normalize_wfn(x, psi_x):
    """Normalize a wavefunction

    Will return the wavefunction psi_x normalized, first it calculates the
    probability density function then the norm of the wavefunction and finally
    divides by the square root of the norm.

    Args:
        x (:obj:`np.array`): 1-D array representing a spatial
            grid.
        psi_x (:obj:`np.array`): 1-D array representing a wavefunction evaluated
         on the spatial grid, show be same length as x.

    Returns:
        Will return a 1-D real :obj:`np.array` representing the normalized
        wavefunction of psi_x.

    """
    pdf = prob_density(psi_x)
    integral_norm = simps(pdf, x)
    wf_normed = psi_x / np.sqrt(integral_norm)
    return wf_normed


def cnt_evolve(cn_0, t, En, hbar=1):
    """Coefficient time evolution

    Based on the time evolution equation and the coefficient and energy of a
    wavefunction it will time-propagate this coefficient into a future time t.
    Returning the value of the coefficient at this time.

    Args:
        cn_0 (float): Coefficient of a wavefunction at time zero.
        t (float): The time at which the coefficient will be evolved.
        En (float): Energy of the wavefunction.
        h_bar (float): value of plank's constant. Defaults to 1 (atomic units).

    Returns:
        Will return a float representing the coefficient at time t.

    """
    exponent = -1j * En * t / hbar
    cn_t = cn_0 * np.exp(exponent)
    return cn_t


def finite_diff(y, dx):
    """Finite difference via central differences.

    For a given function (y) evaluated on a uniform spatial grid with spacing
    dx, it will return the finite differences approximation to the derivative.
    Will use forward difference and backward differences for edge cases.

    Args:
        y (:obj `np.array`): 1-D array contains the function evaluated on a uniform grid.
        dx float: The spacing of the spatial grid.
       
    Returns:
        Will return a float representing the coefficient at time t.

    """
    n = len(y)
    grad = np.zeros(len(y))
    grad[0] = (y[1] - y[0]) / dx
    for i in range(1, n - 2):
        grad[i] = (y[i + 1] - y[i - 1]) / 2 * dx
    grad[n - 1] = (y[n - 1] - y[n - 2]) / dx
    return grad


def momentum_operator(psi_x, dx, hbar=1):
    """Momentum operator on wavefunction

    Compute the momentum operator for a given wavefunction psi_x.
    Will use finite differences to compute the derivative.

    Args:
        psi_x (:obj:`np.array`): 1-D array representing a wavefunction on a
        spatial grid.
        dx (float): Spacing for the spatial grid.
        h_bar (float): Value of plank's constant. Defaults to 1 (atomic units).

    Returns:
        Will return a 1-D :obj:`np.array`.

    """
    prefactor = -1j * hbar
    derivative = finite_diff(psi_x, dx)
    return prefactor * derivative


def eval_expectation(x, psi_x, operator_x):
    """ Evaluate expectation value

    Compute the expectation of a wavefunction `psi_x` defined on a grid `x` with respect
    to the quantum operator `operator_x`. First build the integrand and uses
    `scipy.integrate.simps` to integrate and return the expectation value.

    Args:
        x (:obj `np.array`): 1-D array representing a spatial grid.
        psi_x (:obj:`np.array`): 1-D array representing a wavefunction on a
        spatial grid.
        operator_x (:obj:`np.array`): 1-D array representing a operator evaluated on the  wavefunction psi_x.
    Returns:
        Will a complex number.

    """
    integrand = np.conjugate(psi_x) * operator_x
    exp = complex_simps(integrand, x)
    exp = 0.0 if np.abs(exp) < 1e-7 else exp
    return exp


def pib_superposition(x, t, l, n1=1, n2=2):
    """ Particle in a box superposition

    Create a time-evolved superposition of two particle in a Box eigenstates,
    assumes equal contribution in coefficients between each eigenstate.
    Will return a 2-D :obj:`np.array` with each row being a snapshot of
    the time-evolved wavefunction.

    Args:
        x (:obj:`np.array`): 1-D array representing a spatial grid of len `n`.
        t (:obj:`np.array`): 1-D array representing a temporal grid of len `m`.
        l (float): The length of the box of the pib.
        n1 (int): Quantum number for the first eigenstate.
        n2 (int): Quantum number for the second eigenstate.
    Returns:
        Will a 2-D array of shape `(n,m)`.

    """
    c1 = (1.0 / np.sqrt(2))
    c2 = (1.0 / np.sqrt(2))
    E1 = pib_energy(n1, l)
    E2 = pib_energy(n2, l)
    psi1_x = pib_eigenfunction(x, l, n1)
    psi2_x = pib_eigenfunction(x, l, n2)
    psi = np.zeros((len(x), len(t)))

    for indt, ti in enumerate(t):
        c1_t = cnt_evolve(c1, ti, E1)
        c2_t = cnt_evolve(c2, ti, E2)
        psi[:, indt] = c1_t * psi1_x + c2_t * psi2_x

    return psi


def kinetic_operator(x, m=1, h_bar=1):
    """ Kinetic operator in matrix form

    Will build the Kinectc operator T in matrix form. This is typically used
    for building a Hamiltonian. Uses finite differences to compute the double
    derivative.

    Args:
        x (:obj:`np.array`): 1-D array representing a spatial grid of len `n`.
        m (float): mass of the particle. Defaults to 1 (atomic units).
        h_bar (float): value of plank's constant. Defaults to 1 (atomic units).

    Returns:
        Will a 2-D array of shape `(n,n)`.

    """
    dx = x[1] - x[0]
    t = -h_bar**2 / (2.0 * m * dx**2)
    T = np.zeros((len(x), len(x)))
    for i in range(len(x)):
        # diagonal elements
        T[i][i] = -2 * t
        # side diagonal elements
        if i == 0:
            T[i][i + 1] = t
        elif i == len(x) - 1:
            T[i][i - 1] = t
        else:
            T[i][i + 1] = t
            T[i][i - 1] = t
    return T


def build_hamiltonian(x, v_x, m=1, h_bar=1):
    """ Hamiltonian in matrix form

    Will build the Hamiltonian H in matrix form. This is typically used
    along with `sp.linalg.eigh` to compute eigenvalues and eigenfunctions.
    `v_x` will be a potential evaluated on a spatial grid `x`.

    Args:
        x (:obj:`np.array`): 1-D array representing a spatial grid of len `n`.
        v_x (:obj:`np.array`): 1-D array representing a potential function evaluated
        on a spatial grid, also of len `n`.
        m (float): Mass of the particle. Defaults to 1 (atomic units).
        h_bar (float): Value of plank's constant. Defaults to 1 (atomic units).

    Returns:
        Will a 2-D array of shape `(n,n)`.

    """

    T = kinetic_operator(x, h_bar, m)
    V = np.diag(v_x)
    return T + V


def coulomb_double_well(x, r):
    """ Double coulomb-like well potential

    Will create a double well potential, with coulomb-like wells. Assumes the
    wells are each located at -r/2 and r/2, so the potential is centered at 0.
    The potential is constructed iteratively, using the columb function for each site
    after and before the center 0.

    Args:
        x (:obj:`np.array`): 1-D array representing a spatial grid of len `n`.
        on a spatial grid.
        r (float): The distance between the centers of the two wells

    Returns:
        1-D array of length `n`.

    """
    well = np.zeros_like(x)
    x0_1 = -r / 2.0  # the first well
    x0_2 = r / 2.0  # second well
    for i, xi in enumerate(x):
        if xi <= 0:
            well[i] = - 1.0 / np.abs(xi - x0_1)
        else:
            well[i] = - 1.0 / np.abs(xi - x0_2)

    return well


def coulomb_well(x, x0=0.0):
    """ Coulomb-like well potential

    Will create a Coulomb well potential. Assumes the well is located as x0.

    Args:
        x (:obj:`np.array`): 1-D array representing a spatial grid of len `n`.
        on a spatial grid.
        x0 (float):Centers of the well.

    Returns:
        1-D array of length `n`.

    """
    well = - 1.0 / np.abs(x - x0)
    return well

# Isotropic 2D harmonic oscillator


def harmonic_oscillator_2D(xx, yy, l, m, mass=1.0, omega=1.0, hbar=1.0):
    """ 2D Harmonic Oscillator

    Given 2-D coordinate arrays xx and yy, it will evaluate the harmonic oscillator
    on these grids and return another 2-D coordinate array.

    Args:
        xx (:obj:`np.ndarray`): 2-D coordinate array representing a spatial
            grid on the x axis of shape `(n,n)`.
        yy (:obj:`np.ndarray`): 2-D coordinate array representing a spatial
            grid on the y axis of shape `(n,n)`.
        l (int): Quantum number l.
        m (int): Quantum number m.
        mass (float): Mass of the Oscillator. Defaults to 1 (atomic units).
        omega (float): Frequency of the Oscillator. Defaults to 1 (atomic units).
        h_bar (float): Value of plank's constant. Defaults to 1 (atomic units).

    Returns:
        Will a 2-D ndarray of shape `(n,n)`.

    """

    # This is related to how the function np.polynomail.hermite.hermval
    # works.
    coeff_l = np.zeros((l + 1, ))
    coeff_l[l] = 1.0
    coeff_m = np.zeros((m + 1, ))
    coeff_m[m] = 1.0
    # Hermite polynomials required for the HO eigenfunctions
    hermite_l = np.polynomial.hermite.hermval(
        np.sqrt(mass * omega / hbar) * xx, coeff_l)
    hermite_m = np.polynomial.hermite.hermval(
        np.sqrt(mass * omega / hbar) * yy, coeff_m)
    # This is the prefactors in the expression for the HO eigenfucntions
    prefactor = (mass * omega / (np.pi * hbar)) ** (1.0 / 2.0) / \
        (np.sqrt(2 ** l * 2 ** m * misc.factorial(l) * misc.factorial(m)))
    # And the gaussians in the expression for the HO eigenfunctions
    gaussian = np.exp(-(mass * omega * (xx ** 2 + yy ** 2)) / (2.0 * hbar))
    # The eigenfunction is the product of all of the above.
    return prefactor * gaussian * hermite_l * hermite_m


def harmonic_oscillator_wfn(x, n, m=1.0, omega=1.0, hbar=1.0):
    """ 1D Harmonic Oscillator wavefunction.

    Will return the harmonic oscillator wavefunction evaluted on the spatial grid
    x acoording to the parameters.

    Args:
        x (:obj:`np.array`): 1-D array representing a spatial grid of length `n`.
        n (int): Quantum number n.
        m (float): Mass of the Oscillator. Defaults to 1 (atomic units).
        omega (float): Frequency of the Oscillator. Defaults to 1 (atomic units).
        h_bar (float): Value of plank's constant. Defaults to 1 (atomic units).

    Returns:
        Will a 1-D array of length `(n)`.

    """
    coeff = np.zeros((n + 1, ))
    coeff[n] = 1.0
    prefactor = 1.0 / (np.sqrt(2 ** n * misc.factorial(n))) * \
        (m * omega / (np.pi * hbar)) ** (1.0 / 4.0)
    gaussian = np.exp(-(m * omega * x * x) / (2.0 * hbar))
    hermite = np.polynomial.hermite.hermval(
        np.sqrt(m * omega / hbar) * x, coeff)
    return prefactor * gaussian * hermite


def time_dependent_psi(x, t, omega_f, omega_0=1, lam=1, E_0=1, m=1, hbar=1):

    psi_0 = harmonic_oscillator_wfn(x, 0)
    term1 = 1j * E_0 * (2 * np.pi / lam) / \
        (2 * np.sqrt(2 * m * hbar * omega_0))
    term2 = (np.exp(-1j * (omega_0 - omega_f) * t) - 1) / (omega_0 - omega_f) + \
        (np.exp(1j * (omega_0 + omega_f) * t) - 1) / (omega_0 + omega_f)
    psi_1 = harmonic_oscillator_wfn(x, 1)
    psi_x_t = psi_0 + term1 * term2 * psi_1
    return psi_x_t


def excited_overlap(t, omega_f, omega_0=1, lam=1, E_0=0.1, m=1, hbar=1):

    term1 = 1j * E_0 * (2 * np.pi / lam) / \
        (2 * np.sqrt(2 * m * hbar * omega_0))
    term2 = (np.exp(-1j * (omega_0 - omega_f) * t) - 1) / (omega_0 - omega_f) + \
        (np.exp(1j * (omega_0 + omega_f) * t) - 1) / (omega_0 + omega_f)
    return term1 * term2


def HO_wigner(x, p, w, m=1.0, hbar=1.0):
    """ Harmonic Oscillator wigner representation.

    Returns the Wigner representation of a gaussian in a harmonic oscillator
    potential.


    Args:
        x (:obj:`np.array`): 1-D array representing a spatial grid of length `n`.
        p (:obj:`np.array`): 1-D array representing a momentum space grid of length `m`.
        w (float): Frequency of the Oscillator. Defaults to 1 (atomic units).
        m (float): Mass of the Oscillator. Defaults to 1 (atomic units).
        h_bar (float): Value of plank's constant. Defaults to 1 (atomic units).

    Returns:
        Will a 1-D array of length `(n)`.

    """
    position = np.exp(-m * w / hbar * (x)**2)
    momentum = np.exp(-(p)**2 / (m * w * hbar))
    return position * momentum / (np.pi * hbar)


def plane_wave(x, energy, m=1, hbar=1):
    energy = 10
    k = np.sqrt(2 * m * energy / hbar**2)
    psi = np.zeros(len(x), dtype=np.dtype(complex))
    psi = np.exp(-1j * k * x)
    return psi


def square_barrier(x, l=1, h=9, x0=4):
    v_x = np.zeros_like(x)
    for i in range(len(x)):
        if x[i] < x0:
            v_x[i] = 0
        elif x[i] < x0 + l:
            v_x[i] = h
        else:
            v_x[i] = 0
    return v_x


def tunnel_findiff_propagate(x, psi_x, v_x, E):
    dx = x[1] - x[0]
    new_psi = np.copy(psi_x)
    for i in range(1, len(x) - 1):
        new_psi[i + 1] = (2 + 2 * (v_x[i] - E) * dx**2) * \
            new_psi[i] - new_psi[i - 1]
    return new_psi


def transmission_probability(pdf, n_cutoff=300):
    p_avg = np.mean(pdf[-n_cutoff:])
    t_p = 2.0 / (1 + p_avg)
    return t_p


def dipole_moment_integrand(phi, theta, mu, l1, m1, l2, m2):
    """ INPUTS:
    phi: real value in [0,2pi]
    theta: real value in [0,pi]
    mu: dipole moment of the molecule
    l1, m1: quantum numbers for the first spherical harmonic
    l2, m2: quantum numbers for the second spherical harmonic
    OUTPUT:
    Integrand evaluated at (phi,theta)
    """
    mu_operator = mu * (np.sin(theta) * np.cos(phi) +
                        np.sin(theta) * np.sin(phi) + np.cos(theta))
    Y_lm_1 = sph_harm(m1, l1, phi, theta)
    Y_lm_2 = sph_harm(m2, l2, phi, theta)
    dV = np.sin(theta)
    integrand = np.conjugate(Y_lm_1) * mu_operator * Y_lm_2 * dV
    return integrand


def hydrogen_radial_wfn(r, n, l, a0=1.0, z=1.0):
    """
    This method will return the radial part of the wave function. I've gone ahead and defined the normalization factor but you
    will need to implement the rest.

    INPUT
    r: Array of points to return the value of the wavefunction on
    n: principle quantum number
    l: angular quantum number

    OUTPUT
    wf: Array of points to return the wavefunction
    """
    rho = 2.0 * z * r / (n * a0)
    subscript = n - l - 1.0
    superscript = 2.0 * l + 1.0
    normFactor = np.sqrt((2.0 * z / (n * a0))**3 *
                         factorial(subscript) / (2.0 * n * factorial(n + l)))

    # Fill this line in
    wf = rho**l * np.exp(-rho / 2.0) * \
        eval_genlaguerre(subscript, superscript, rho)
    return wf * normFactor


def dipole_moment_integrand_superposition(phi, theta, mu, c1, c2, l1, m1, l2, m2):
    """INPUTS:
    phi: real value in [0,2pi]
    theta: real value in [0,pi]
    mu: dipole moment of the molecule
    c1, c2: normalized coefficients for the superposition
    l1, m1: quantum numbers for the first spherical harmonic
    l2, m2: quantum numbers for the second spherical harmonic
    OUTPUT:
    Integrand evaluated at (phi,theta) for the superposition
    Y=c_1 Y^l1_m1 + c_2 Y^l2_m2"""
    mu_operator = mu * (np.sin(theta) * np.cos(phi) +
                        np.sin(theta) * np.sin(phi) + np.cos(theta))
    Y_lm_1 = sph_harm(m1, l1, phi, theta)
    Y_lm_2 = sph_harm(m2, l2, phi, theta)
    Y_lm = c1 * Y_lm_1 + c2 * Y_lm_2
    dV = np.sin(theta)
    integrand = np.conjugate(Y_lm) * mu_operator * Y_lm * dV
    return integrand


def dipole_moment_integrand_superposition(phi, theta, mu, c1, c2, l1, m1, l2, m2):
    """INPUTS:
    phi: real value in [0,2pi]
    theta: real value in [0,pi]
    mu: dipole moment of the molecule
    c1, c2: normalized coefficients for the superposition
    l1, m1: quantum numbers for the first spherical harmonic
    l2, m2: quantum numbers for the second spherical harmonic
    OUTPUT:
    Integrand evaluated at (phi,theta) for the superposition
    Y=c_1 Y^l1_m1 + c_2 Y^l2_m2"""
    mu_operator = mu * (np.sin(theta) * np.cos(phi) +
                        np.sin(theta) * np.sin(phi) + np.cos(theta))
    Y_lm_1 = sph_harm(m1, l1, phi, theta)
    Y_lm_2 = sph_harm(m2, l2, phi, theta)
    Y_lm = c1 * Y_lm_1 + c2 * Y_lm_2
    dV = np.sin(theta)
    integrand = np.conjugate(Y_lm) * mu_operator * Y_lm * dV
    return integrand

# This class allows us to do various energy manipulations.
# It's not really important to know how it works, just use it as a black box


class EnergyTuple:

    def __init__(self, name=None, energy=1.0, quantumNumbers=[], efunc=None, **kwds):
        '''
        Init function. You should almost certainly pass in the quantum numbers dictionary and energy function to actually
        get any use
        '''
        self.energy = energy  # sets energy to default value
        self.qn = quantumNumbers  # sets quantum number dictionary, qn, to what was passed in
        if name != None:  # sets name of the state to the given one, if one is passed in
            self.name = name
        else:  # Other wise, name the state according to the the quantum numbers passed in
            string = ""
            for key in self.qn:
                string += key + " = " + str(self.qn[key]) + ", "
            self.name = string[:-2]  # Trim off the last comma
        if efunc != None:  # Sets the energy to the proper value, if the energy function was defined
            self.efunc = efunc
            self.populateEnergy()
        else:
            self.energy = 1.0
        self.__dict__.update(kwds)

    def populateEnergy(self):
        # Sets the energy
        self.energy = self.efunc(self.qn)

    def energyInWavenumbers(self):
        # Returns the energy converted from hartrees to wavenumbers [cm^-1]
        return self.energy * 2.1947e5

    def wavelength(self):
        # Returns the wavelength associated with the energy
        return np.abs(45.56 * 1.0 / self.energy)

    def colour_string(self):
        return '#%02x%02x%02x' % self.colour()

    def colour(self, n1=2.0):
        # Returns the colour. Don't worry about this, it's just interpolation
        # stuff.
        w = self.wavelength()
        # colour
        if w >= 380 and w < 440:
            R = -(w - 440.) / (440. - 350.)
            G = 0.0
            B = 1.0
        elif w >= 440 and w < 490:
            R = 0.0
            G = (w - 440.) / (490. - 440.)
            B = 1.0
        elif w >= 490 and w < 510:
            R = 0.0
            G = 1.0
            B = -(w - 510.) / (510. - 490.)
        elif w >= 510 and w < 580:
            R = (w - 510.) / (580. - 510.)
            G = 1.0
            B = 0.0
        elif w >= 580 and w < 645:
            R = 1.0
            G = -(w - 645.) / (645. - 580.)
            B = 0.0
        elif w >= 645 and w <= 780:
            R = 1.0
            G = 0.0
            B = 0.0
        else:
            R = 0.0
            G = 0.0
            B = 0.0

        # intensity correction
        if w >= 380 and w < 420:
            SSS = 0.3 + 0.7 * (w - 350) / (420 - 350)
        elif w >= 420 and w <= 700:
            SSS = 1.0
        elif w > 700 and w <= 780:
            SSS = 0.3 + 0.7 * (780 - w) / (780 - 700)
        else:
            SSS = 0.0
        SSS *= 255

        return (int(SSS * R), int(SSS * G), int(SSS * B))


def L(rho, alpha, n):
    """
    This method returns the generalized laguerre polynomial with subscript n
    # and superscript alpha for points rho
    This is a giant pain to get all the factors just right. Don't do it.

    rho: Array of points to return the value of the polynomial on
    alpha: Superscript parameter
    n: Subscript parameter


    poly: Array with the discrete values of the specified Laguerre polynomial
    """
    poly = np.zeros_like(rho)
    for i in range(0, int(n) + 1):
        coeff = binom(n + alpha, n - i) * (-1)**i / (factorial(i))
        poly += coeff * np.power(rho, i)
    return poly


def r_expectation(r, n, l, a0=1.0, z=1.0):
    wf = hydrogen_radial_wfn(r, n, l, a0=1.0, z=1.0)
    r_expectation = np.conjugate(wf) * r**3.0 * wf
    return r_expectation


def harmonic_time_independent(x, n, l):
    """ 1D time-dependent component of the wave solution for a standing wave.

    Will return the time-independent solution to the wave equation for a wave on 
    a string, evaluted on the spatial grid x acoording to the parameters.

    Args:
        x (:obj:`np.array`): 1-D array representing a spatial grid of length `xn`.
        n (int): Harmonic n.
        l (float): Length of the box for the HO.

    Returns:
        Will a 1-D array of length `(xn)`. Can also return a float.

    """
    amplitude = np.sin(n * np.pi * x / l)
    return amplitude


def harmonic_time_dependent(t, c, n, l):
    """ 1D time-dependent component of the wave solution for a standing wave.

    Will return the time-dependent solution to the wave equation for a wave on 
    a string, evaluted on the spatial grid x acoording to the parameters.

    Args:
        x (:obj:`np.array`): 1-D array representing a spatial grid of length `xn`.
        c (int): String constant for the standing wave.
        n (int): Harmonic n.
        l (float): Length of the box for the HO.

    Returns:
        Will a 1-D array of length `(xn)`. Can also return a float.

    """
    amplitude = np.cos(n * np.pi * c * t / l)
    return amplitude


def wave_solution(x, t, c, n, l):
    """ 1D wave solution for a standing wave.

    Will return the time-depdant solution to the wave equation for a wave on 
    a string, evaluted on the spatial grid x and temporal grid t
    acoording to the parameters.

    Args:
        x (:obj:`np.array`): 1-D array representing a spatial grid of length `xn`.
        t (:obj:`np.array`): 1-D array representing a spatial grid of length `tn`.
        c (int): String constant for the standing wave.
        n (int): Harmonic n.
        l (float): Length of the box for the HO.

    Returns:
        Will a 2-D array of shape `(xn,tn)`.

    """
    amp_x = harmonic_time_independent(x, n, l)
    amp_t = harmonic_time_dependent(t, c, n, l)
    return amp_x * amp_t


def complex_quad(func, a, b, **kwargs):
    """ Complex version of scipy's quad

    Will return integral of a complex function over a range (a,b). 
    Uses same arguments as scipy.integrate.quad.

    Args:
        func (:obj:`function`): Callable function to integrate.
        a (float): Start point of integration range.
        b (float): End point of integration range.
        **kwargs : For additional arguments look up documentation
                   on the scipy.integrate.quad function.

    Returns:
        Will a tuples of (real,imaginary) values.

    """
    def real_func(x):
        return sp.real(func(x))

    def imag_func(x):
        return sp.imag(func(x))

    real_integral = quad(real_func, a, b, **kwargs)
    imag_integral = quad(imag_func, a, b, **kwargs)
    return (real_integral[0] + 1j * imag_integral[0],
            real_integral[1:], imag_integral[1:])


def complex_simps(y, x):
    """ Complex version of scipy's simps

    Will return integral of a complex function y over a numerical grid x.

    Args:
        y (:obj:`np.array`): A 1-D complex-valued array of size n.
        x (float): A 1-D real-valued array of size n.

    Returns:
        A 1-D complex-valued array of size n.

    """
    real_integral = simps(y.real, x)
    imag_integral = simps(y.imag, x)
    return real_integral + 1j * imag_integral

if __name__ == "__main__":
    print("Load me as a module please")
