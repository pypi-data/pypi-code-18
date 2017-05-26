import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
from scipy import misc
import mpl_toolkits.mplot3d.axes3d as axes3d
from scipy.special import sph_harm
from scipy.misc import factorial
from scipy.special import genlaguerre, binom, eval_genlaguerre
from scipy.integrate import simps, quad, nquad

# global variables
COLOR_MAP = 'viridis'

# math utilities


def extend_range(v, percent=0.05):
    vmin, vmax = np.min(v), np.max(v)
    vdiff = (vmax - vmin)
    vmin -= vdiff * percent
    vmax += vdiff * percent
    return vmin, vmax

# time based plotting utilities


def time_colormap(t):
    cmap = mpl.cm.get_cmap(COLOR_MAP)
    norm = mpl.colors.Normalize(vmin=np.min(t), vmax=np.max(t))

    def color_map(v):
        return cmap(norm(v))

    return color_map


def time_colorbar(t):
    cmap = mpl.cm.get_cmap(COLOR_MAP)
    norm = mpl.colors.Normalize(vmin=np.min(t), vmax=np.max(t))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    # fake up the array of the scalar mappable
    sm._A = []
    return sm


def time_plot(x, y, t, t_step=1):

    cmap = time_colormap(t)

    for indt in range(0, len(t), t_step):
        ti = t[indt]
        plt.plot(x, y[:, indt], c=cmap(ti))

    plt.xlim(extend_range(x))
    plt.ylim(extend_range(y))
    plt.xlabel('$x$')
    plt.ylabel('$y$')

    plt.colorbar(time_colorbar(t), label='time ($t$)',
                 orientation='horizontal')
    return


def time_plot1D(x, t, t_step=1):
    '''This function plots 
    Input:
        -- x : spatial array with positions of a 1-D particle.
        -- t : time array.
        -- t_step : how many value of t to skip for each plot.
    '''
    cmap = time_colormap(t)

    for indx in range(0, len(t), t_step):
        ti = t[indx]
        xi = x[indx]
        plt.scatter(ti, xi, c=cmap(ti), s=100)

    plt.xlim([np.min(t), np.max(t)])
    plt.ylim(extend_range(x))
    plt.xlabel('$t$')
    plt.ylabel('$x$')

    # plt.gca().get_yaxis().set_visible(False)

    plt.colorbar(time_colorbar(t), label='time ($t$)',
                 orientation='horizontal')
    return

# quantum objects


def pib_eigenfunction(x, L, n):
    '''given x, L, and n returns an eigenfunction for the 1D particle in a box
    Inputs: x -- numpy array.
            L -- scalar, length of the box.
            n -- intenger
    '''
    psi_x = np.sqrt(2.0 / L) * np.sin(n * np.pi * x / L)
    return psi_x


def prob_density(psi_x):
    ''' get probability density function associated to the wavefunction psi_x
    Input: psi_x --> an array, representing a values of a wavefunction
    '''
    prob = np.conjugate(psi_x) * psi_x
    return prob


def pib_energy(n, L, h_bar=1, m=1):
    '''This function returns energy of the nth eigenstate
    of the 1D particle in a box.
    Input:
        -- n : quantum number specifying which eigenstate
        -- L, length of the box
    '''
    E_n = (n * h_bar * np.pi) ** 2 / (2.0 * m * L ** 2)
    return E_n


def pib_eigenfunction(x, l, n):
    psi_x = np.sqrt(2.0 / l) * np.sin(n * np.pi * x / l)
    return psi_x


def prob_density(psi_x):
    prob = np.conjugate(psi_x) * psi_x
    return prob


def prob_density(psi_x):
    prob = np.conjugate(psi_x) * psi_x
    return prob
#


def wfn_norm(x, psi_x):
    pdf = prob_density(psi_x)
    integral_norm = simps(pdf, x)
    return integral_norm


def normalize_wfn(x, psi_x):
    pdf = prob_density(psi_x)
    integral_norm = simps(pdf, x)
    wf_normed = psi_x / np.sqrt(integral_norm)
    return wf_normed


def cnt_evolve(cn_0, t, E_n, hbar=1):
    exponent = -1j * E_n * t / hbar
    cn_t = cn_0 * np.exp(exponent)
    return cn_t


def finite_diff(y, dx):
    n = len(y)
    grad = np.zeros(len(y))
    grad[0] = (y[1] - y[0]) / dx
    for i in range(1, n - 2):
        grad[i] = (y[i + 1] - y[i - 1]) / 2 * dx
    grad[n - 1] = (y[n - 1] - y[n - 2]) / dx
    return grad


def momentum_operator(psi_x, dx, hbar=1):
    prefactor = -1j * hbar
    derivative = finite_diff(psi_x, dx)
    return prefactor * derivative


def eval_expectation(x, psi_x, operator_x):
    integrand = np.conjugate(psi_x) * operator_x * psi_x
    exp = simps(integrand, x)
    exp = 0.0 if np.abs(exp) < 1e-7 else exp
    return exp


def psi_pib_superposition(x, t, L, n1=1, n2=2):
    c1 = (1.0 / np.sqrt(2))
    c2 = (1.0 / np.sqrt(2))
    E1 = pib_energy(n1, L)
    E2 = pib_energy(n2, L)
    psi1_x = pib_eigenfunction(x, L, n1)
    psi2_x = pib_eigenfunction(x, L, n2)
    psi = np.zeros((len(x), len(t)))

    for indt, ti in enumerate(t):
        c1_t = cnt_evolve(c1, ti, E1)
        c2_t = cnt_evolve(c2, ti, E2)
        psi[:, indt] = c1_t * psi1_x + c2_t * psi2_x

    return psi


def kinetic_operator(x, h_bar=1, m=1):
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
    ''' this function builds the matrix representation of H,
    given x, the position array, and V_x as input
    '''
    T = kinetic_operator(x, h_bar=1, m=1)
    V = np.diag(v_x)
    return T + V


def coulomb_double_well(x, r):
    '''Create a double well, coulomb-like potential.
    Inputs:
    x --> numpy array of positions
    R --> the distance between the centers of the two wells
    '''
    x0_1 = -r / 2.0  # the first well
    well_1 = - 1.0 / np.abs(x - x0_1)
    x0_2 = r / 2.0  # center of the second well
    well_2 = - 1.0 / np.abs(x - x0_2)
    return (well_1 + well_2) / 2.0


# Isotropic 2D harmonic oscillator


def harmonic_oscillator_2D(xx, yy, l, m, mass=1.0, omega=1.0, hbar=1.0):
    '''Returns the wavefunction for the 1D Harmonic Oscillator, given the following inputs:
    INPUTS:
        xx --> x-axis values for a 2D grid
        yy --> y-axis values for a 2D grid
        l --> l quantum number
        m --> m quantum number
        mass --> mass (defaults to atomic units)
        omega --> oscillator frequency, defaults to atomic units.
        hbar --> planck's constant divided by 2*pi
    '''
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


def plot_3d_surface(xx, yy, zz):
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    # Plot as a surface
    ax.plot_surface(xx, yy, zz, rstride=8, cstride=8, alpha=0.25)
    # This sets the angle at which we view the plot
    ax.view_init(30, -60)
    # THIS IS FANCY BUT USELESS: Plots the projections onto the xy, xz, yz
    # planes
    ax.contour(xx, yy, zz, zdir='z')
    # label axes and add title
    plt.xlabel('x')
    plt.ylabel('y')
    return


def plot_contours(xx, yy, zz):
    plt.contour(xx, yy, zz, linewidths=3)
    CS = plt.contour(xx, yy, zz, colors='k', linewidths=0.5)
    plt.pcolor(xx, yy, zz)
    plt.clabel(CS, inline=1)
    plt.colorbar(label='z')
    plt.xlabel('x')
    plt.ylabel('y')
    return


def harmonic_oscillator_wf(x, n, m=1.0, omega=1.0, hbar=1.0):
    '''Returns the wavefunction for the 1D Harmonic Oscillator,
    given the following inputs:
    INPUTS:
        x --> a numpy array
        n --> quantum number, an intenger
        m --> mass (defaults to atomic units)
        omega --> oscillator frequency, defaults to atomic units.
        hbar --> planck's constant divided by 2*pi
    '''
    coeff = np.zeros((n + 1, ))
    coeff[n] = 1.0
    prefactor = 1.0 / (np.sqrt(2 ** n * misc.factorial(n))) * \
        (m * omega / (np.pi * hbar)) ** (1.0 / 4.0)
    gaussian = np.exp(-(m * omega * x * x) / (2.0 * hbar))
    hermite = np.polynomial.hermite.hermval(
        np.sqrt(m * omega / hbar) * x, coeff)
    return prefactor * gaussian * hermite


def harmonic_oscillator_wfn(x, n, m=1.0, omega=1.0, hbar=1.0):
    '''Returns the wavefunction for the 1D Harmonic Oscillator,
    given the following inputs:
    INPUTS:
        x --> a numpy array
        n --> quantum number, an intenger
        m --> mass (defaults to atomic units)
        omega --> oscillator frequency, defaults to atomic units.
        hbar --> planck's constant divided by 2*pi
    '''
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
    '''
    Returns the wigner representation of a gaussian in a harmonic oscillator potential
    INPUT
    -------------------
    x: scalar or matrix of positions to compute the wigner density on
    p: scalar of matrix of momenta to compute the wigner density on
    w: scalar for the frequency

    OUTPUT
    -------------------
    returns the wigner density
    '''
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
    '''
    This method will return the radial part of the wave function. I've gone ahead and defined the normalization factor but you
    will need to implement the rest.

    INPUT
    --------------------
    r: Array of points to return the value of the wavefunction on
    n: principle quantum number
    l: angular quantum number

    OUTPUT
    --------------------
    wf: Array of points to return the wavefunction
    '''
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

    def __init__(self, name=None, energy=1.0, quantumNumbers=[],  efunc=None, **kwds):
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


def energy_diagram_plot(energy_list):
    linewidth = 200.0
    offset_to_add = 240.0
    fig = plt.figure(figsize=(14, 3))
    ax = fig.add_subplot(111)
    plt.xlim([-linewidth / 2.0 - 5.0, 2000.0])
    plt.ylim([-0.6, 0.0])

    eprev = 0.0
    offset = 0.0
    for et in energy_list:
        if eprev == et.energy:
            offset += offset_to_add
        else:
            offset = 0.0
        xmin = -linewidth / 2.0 + offset
        xmax = linewidth / 2.0 + offset
        y = et.energy
        plt.hlines(y, xmin, xmax, linewidth=2)
        ax.annotate(et.name, xy=(xmin, y - 0.013))
        fig.set_size_inches(18.5, 10.5)
        eprev = et.energy
    return


def L(rho, alpha, n):
    '''
    This method returns the generalized laguerre polynomial with subscript n
    # and superscript alpha for points rho
    This is a giant pain to get all the factors just right. Don't do it.

    INPUT
    --------------------
    rho: Array of points to return the value of the polynomial on
    alpha: Superscript parameter
    n: Subscript parameter

    OUTPUT
    --------------------
    poly: Array with the discrete values of the specified Laguerre polynomial
    '''
    poly = np.zeros_like(rho)
    for i in range(0, int(n) + 1):
        coeff = binom(n + alpha, n - i) * (-1)**i / (factorial(i))
        poly += coeff * np.power(rho, i)
    return poly


def r_expectation(r, n, l, a0=1.0, z=1.0):
    wf = hydrogen_radial_wfn(r, n, l, a0=1.0, z=1.0)
    r_expectation = np.conjugate(wf) * r**3.0 * wf
    return r_expectation

if __name__ == "__main__":
    print("Load me as a module please")
