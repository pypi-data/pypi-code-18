"""
Tools for extreme value statistics on discharge measurements.

"""
from hydrobox.utils.decorators import accept
from matplotlib.axes import SubplotBase
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import rankdata


@accept(x=np.ndarray,log=bool, plot=bool, non_exceeding=bool, ax=('None', SubplotBase))
def flow_duration_curve(x, log=True, plot=True, non_exceeding=True, ax=None, **kwargs):
    """
    Calculate and draw a flow duration curve from the discharge measurements.

    All oberservations will be ordered and the Weibull empirical probability will be calculated.
    The ordered probabilities are plotted as a flow duration curve.

    In case x.ndim > 1, the function will be called iterativly along axis 0.

    :param x:   numpy.ndarray of discharge measurements
    :param log:  bool, if True plot on loglog axis, ignored when plot is False
    :param plot: bool, if False not plotting, returning the result instead
    :param non_exceeding: bool, if true use non-exceeding probalilities
    :param ax: matplotlib Subplot object, if not None, will plot into that instance
    :param kwargs: will be passed to the matplotlib.pyplot.plot function
    :return:
    """
    if x.ndim > 1:
        raise NotImplementedError('This is not implemented yet.')

    # calculate the ranks
    ranks = rankdata(x, method='average')

    # calculate weibull pdf
    N = x.size

    # calculate probabilities
    p = np.fromiter(map(lambda r: r / (N + 1), ranks), dtype=np.float)

    # create sorting index
    if non_exceeding:
        index = np.argsort(p)
    else:
        index = np.argsort(p)[::-1]

    if not plot:
        return p[index]

    # generate an Axes, if ax is None
    if ax is None:
        fig, ax = plt.subplots(1,1)

    # plot
    # set some defaults
    kwargs.setdefault('linestyle', '-')
    kwargs.setdefault('color', 'b')
    ax.plot(x[index], p[index], **kwargs)
    #label
    ax.set_xlabel('discharge [m3/s]')
    ax.set_ylabel('%sexceeding prob.' % ('non-' if non_exceeding else ''))
    # handle loglog
    if log:
        ax.loglog()
    else:
        ax.set_ylim((-0.05, 1.1))
        ax.set_xlim(np.nanmin(x) *0.98, np.nanmax(x) * 1.02)
    ax.set_title('%sFDC' % ('loglog ' if log else ''))
    ax.grid(which='both' if log else 'major')

    return ax

