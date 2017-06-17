import numpy as np
from scipy import stats
from .annealing import lengthToDensity
from .thermal_histories import Thermal_history 
import random
import sys


def drawbinom(I, prob):
    # Look at scipy.stats.binom...option binom.rvs
    """Random draw from binomial distribution

    Utility function:
    Draw from a binomial distribution:
    Only return if the draw is different than 0
    """
    Ns = 0
    while Ns == 0:
        A = np.random.RandomState()
        Ns = A.binomial(I, prob)
    return Ns


def create_distribution(xk, pk, name="TLD"):
    return stats.rv_discrete(name=name, values=(xk, pk))


def draw_from_distrib(vals, pdf, size=1):
    """Random Draw from given distribution
    """
    vals = np.array(vals)
    distrib = stats.rv_discrete(values=(range(len(vals)), pdf))
    return vals[distrib.rvs(size=size)]

def AdjustTTHistory(time, temp):
    """Calculate adjusted thermal history

    Useful when one needs to calculate thermal history 
    in a borehole when some of the sample reaches
    surface temperature
    """

    def zerointersect(pt1, pt2):
        x1, y1 = pt1
        x2, y2 = pt2

        xmax = max(x1, x2)
        xmin = min(x1, x2)

        x = np.array([[x1, 1.0], [x2, 1.0]])
        y = np.array([y1, y2])
        A, B = np.linalg.solve(x, y)
        X, Y = -B/A, 0.0
        if(X > xmin and X < xmax):
            return X, Y
        else:
            return None, None

    if(len(time) != len(temp)):
            return "Error"

    TT = [[time[i], temp[i]] for i in range(0, len(time))]

    newTT = []
    for i in range(0, len(TT)-1):
        pt1 = TT[i]
        pt2 = TT[i+1]
        X, Y = zerointersect(pt1, pt2)
        if(X is not None):
            newTT.append([X, Y])

    TT.extend(newTT)
    newTT = []
    for elem in TT:
        if(elem[1] >= 0.0):
            newTT.append(elem)

    newTT.sort()
    newTT.reverse()
    time = [elem[0] for elem in newTT]
    temp = [elem[1] for elem in newTT]
    return time, temp


def initial_track_length():
    """
    Return the initial track length for the population based on 
    the apatite kinetics.
    """
    return


def interpolate_history_as_isothermal_intervals(tTpath):
    """Takes the time-temperature path specification and subdivides it for
    calculation in isothermal intervals.
    
    Does it based on model of Ketcham et al., in review.
    It is calibrated to facilitate 0.5% accuracy for end-member F-apatite by
    having a maximum temperature step of 3.5 degrees C when the model
    temperature is within 10 C of the total annealing temperature.  Before this
    cutoff the maximum temperature step required is 8 C.  If the overall model
    time steps are too large, these more distant requirements may not be met.
    """
    total_time = tTpath.totaltime 
    rate = tTpath.rate
    abs_rate = abs(rate)
    def_timestep = total_time / 100.0

    return tTpath


def calculate_reduced_standard_deviation(redLength, project=True):
    """Calculates the reduced standard deviation.
    
    Parameters:
    -----------
    redLength -- reduced length (Line segment theory; Parker and Cowan, 1976
                 Laslett et al, 1982.
    project -- Use projected track length (Default: True)

    Calculates the reduced standard deviation of a track population length
    from the reduced mean length.  Based on Carlson and Donelick (unpub.
    data).
    """
    if project:
        return 0.1081 - 0.1642 * redLength + 0.1052 * redLength * redLength
    else:
        return 0.4572 - 0.8815 * redLength + 0.4947 * redLength * redLength


def calculate_track_length_distribution1(tTPath, kinpar, kinetic="Etch pit length"):
    """Calculates the model track length distribution for a given time-
    temperature history based on the calibration of Ketcham et al.

    c-axis-parallel length (Rcmod).
    """
    def etch_pit_length(kinpar):
        if kinpar <= 1.75:
            return 0.84
        elif kinpar >= 4.58:
            return 0.0
        else:
            return 1.0 - np.exp(0.647 * (kinpar - 1.75) - 1.834)
    
    def cl_pfu(kinpar):
        if(abs(kinpar - 1.0) <= 0.130):
            return 0.0
        else:
            return 1.0 - np.exp(2.107 * (1.0 - abs(kinpar - 1.0)) - 1.834)

    def oh_pfu(kinpar):
        return 0.84 * (1.0 - pow(1.0 - (kinpar - 1.0), 4.5))


    options = {"Etch pit length": etch_pit_length, "CL PFU": cl_pfu,
            "OH PFU": oh_pfu}

    # Calculate rmr0 according to kinetic parameter
    f = option[kinetic]
    rmr0 = f(kinpar)
    k = 1.0 - rmr0
    # equivTotAnnLen is the length of the more resistant apatite
    # at the length of total annealing for the less resistant
    # apatite we're modeling.   
    # In the future, if this routine is adapted to solve for
    # many different apatite kinetic populations at once, 
    # we would use the rmr0 and k values for the most
    # resistant apatite being modeled.
    totAnnealLen = MIN_OBD_RCMOD
    equivTotAnnLen = pow(totAnnealLen, 1.0 / k) * (1.0 - rmr0) + rmr0

    # Import annealing model


    return


def calculate_track_length_distribution2():
    """Calculates the model track length distribution for the given time-
    temperature history.  For each T-t segment, it finds the reduced
    mean and standard deviation for the population of track lengths based
    on the model of Laslett et al. (1987).  The tiq calculation uses
    Goswami et al. (1984) and Duddy et al. (1988).
    """
    return


def conversion_length_to_density(cparlen):
    """Does the conversion from length to density for the
    Ketcham et al., 1999 model.

    Parameter:
    ----------

    cparlen -- c-axis-projected length 
    Assumes we're passing in a c-axis-projected length
    """

    if cparlen > 0.757:
        return 1.600 * cparlen - 0.599
    if cparlen >= MIN_OBS_RCMOD:
        return 9.205 * cparlen * cparlen - 9.157 * cparlen + 2.269
    return 0.0

def sum_populations():
    """Sums the individual model track length populations into an overall
    population, and normalizes.  Takes care of conversion from mean to projected
    lengths and finding the standard deviation of the population distribution.
    """

def get_tracklengths_stats():
    """Return statistics of the model track length distribution."""


    stDev = 0.0
    skewness = 0.0
    kurtosis = 0.0
    mean = 0.0
    stderror = 0.0
    return {"Mean Track Length": mean, "Standard Deviation": stDev,
            "Standard Error": stderror, "Skewness": skewness,
            "Kurtosis": kurtosis}



###### THE FOLLOWING 2 DO THE SAME THING


def get_age_correction(redLength, projected=False):
    """Estimates the correction in the fission track age caused by length
    reduction over a time interval.  If orientation is ignored, the
    appropriate answer is to follow the relationship of track length
    reduction to track density reduction (Green, 1988; Willett, 1992).
    If we project track lengths, we can simply use the reduced track
    length.
    
    Basically, the probability of a population being observed relative to
    the probability of the longest population of tracks.  For mean length
    models, this the probability is simply the reduced length (Line segment
    theory; Parker and Cowan, 1976; Laslett et al., 1982).

    Actually, this should take into account loss of some
    tracks to total annealing.  The closest thing we have so far is the
    relationship between observed length and observed density.
    
    Parameter:
    ----------
    
    redLength -- reduced length (Line segment theory; Parker and Cowan, 1976
                 Laslett et al, 1982.
    projected -- Boolean (default is False) indicates if tracks are projected.
    """
    if projected:
        return redLength

    return LengthToDensity.getval(redLength)

# Alias to above function
get_observational_bias = get_age_correction

def calculate_model_ages():
    """Calculates the estimated age
    
    Calculate the estimated age which would be measured from the model
    fission track population.  Each time interval added in, and
    corrected by the amount of density reduction expected given the
    length reduction.
    """




