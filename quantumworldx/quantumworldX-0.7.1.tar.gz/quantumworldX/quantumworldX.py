import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
from scipy.integrate import simps
from scipy import misc

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


def build_H_matrix(x, v, m=1, h_bar=1):
    ''' this function builds the matrix representation of H,
    given x, the position array, and V_x as input
    '''
    a = x[1] - x[0]  # x is the dx of the grid.  We can get it by taking the diff of the first two
    # entries in x
    t = h_bar ** 2 / (2 * m * a ** 2)  # the parameter t, as defined by schrier

    # initialize H_matrix as a matrix of zeros, with appropriate size.
    H_matrix = np.zeros((len(x), len(x)))
    # Start adding the appropriate elements to the matrix
    for i in range(len(x)):
        # (ONE LINE)
        # Assignt to H_matrix[i][i],the diagonal elements of H
        # The appropriate values
        H_matrix[i][i] = 2 * t + v(x[i])
        #########
        # special case, first row of H
        if i == 0:
            # Assignt to H_matrix[i][i+1],the off-diagonal elements of H
            # The appropriate values, for the first row
            H_matrix[i][i + 1] = -t
        elif i == len(x) - 1:  # special case, last row of H
            H_matrix[i][i - 1] = -t
        else:  # for all the other rows
            # (TWO LINE)
            # Assignt to H_matrix[i][i+1], and H_matrix[i][i-1]
            # the off-diagonal elements of H, the appropriate value, -t
            H_matrix[i][i + 1] = -t
            H_matrix[i][i - 1] = -t
            ################
    return H_matrix

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


def normalize_wf(x, psi_x):
    '''this function normalizes a wave function
    Input -->
            x, numpy array of position vectors
            psi_x, numpy array representing wave function, same length as x
            dvr, boolean, while normalize differently if wavefunction is in dvr space
    Output:
            wf_norm --> normalized wave function
    '''
    #########
    # 1. Get integral_norm
    integral_norm = norm_wf(psi_x, x)
    # 2. normalize the wavefunction by dividing psi_x by the square root of integral norm.
    # Assign to wf_norm
    wf_norm = psi_x * np.sqrt(1.0 / integral_norm)
    ############
    return wf_norm


def norm_wf(psi_x, x):
    '''this function returns the norm of a wave function
    Input --> psi_x, numpy array representing wave function, same length as x
            x, numpy array of position vectors
            dvr, boolean, while normalize differently if wavefunction is in dvr space
    Output:
            values --> norm of a wave function
    '''
    integral_norm = 0.0

    pdf = probabilityDensity(psi_x)
    integral_norm = simps(pdf, x)

    return integral_norm


def probabilityDensity(psi_x):
    prob = np.conjugate(psi_x) * psi_x
    return prob


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

if __name__ == "__main__":
    print("Load me as a module please")
