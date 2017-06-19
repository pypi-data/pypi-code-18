# -*- coding: utf-8 -*-
"""qwX plotting functions

   Anything plotting related goes here, these functions are imported with
   ``import quantumworldX as qw`` from there you are able to use all plot functions,
   for example to utilize `time_plot` you would use ``qw.time_plot``.

"""


import numpy as np
from matplotlib import pyplot as plt
import matplotlib as mpl
from scipy import misc
import mpl_toolkits.mplot3d.axes3d as axes3d
from scipy.special import sph_harm
from scipy.misc import factorial
from cycler import cycler
from mpl_toolkits import axes_grid1

# global variables
COLOR_MAP = 'viridis'


def plot_settings():
    params = {'legend.fontsize': 'small',
              'axes.labelsize': 'large',
              'axes.titlesize': 'medium',
              'image.cmap': COLOR_MAP,
              'lines.linewidth': 2,
              'axes.prop_cycle': cycler('color', ['#1f77b4', '#ff7f0e',
                                                  '#2ca02c', '#d62728',
                                                  '#9467bd', '#8c564b',
                                                  '#e377c2', '#7f7f7f',
                                                  '#bcbd22', '#17becf'])
              }
    mpl.rcParams.update(params)
    return


def _extend_range(v, percent=0.05):
    vmin, vmax = np.min(v), np.max(v)
    vdiff = (vmax - vmin)
    vmin -= vdiff * percent
    vmax += vdiff * percent
    return vmin, vmax


def _time_colormap(t):
    cmap = mpl.cm.get_cmap(COLOR_MAP)
    norm = mpl.colors.Normalize(vmin=np.min(t), vmax=np.max(t))

    def color_map(v):
        return cmap(norm(v))

    return color_map


def _time_colorbar(t):
    cmap = mpl.cm.get_cmap(COLOR_MAP)
    norm = mpl.colors.Normalize(vmin=np.min(t), vmax=np.max(t))
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    # fake up the array of the scalar mappable
    sm._A = []
    return sm


def time_plot(x, y, t, t_step=1):
    """Plot several plots overlaid across time

    Utility plotting function that will setup plots of several snapshots in
    time (t) of a function (y) over a spatial grid (x). You can control the
    frequency of these plots with t_step, with a higher value indicating less
    frequent plots across time. At some moment after use, `plt.show` should
    be utilized to display the figure.

    Args:
        x (:obj:`np.array`): 1-D array of shape `(n)` representing a spatial
            grid
        y (:obj:`np.array`): 2-D array of shape `(n,m)` representing several
            snapshots across time of a function on a spatial grid
        t (:obj:`np.array`): 1-D array of shape `(m)` representing a time grid
        t_step (int): integer indicating how many frames to skip for plotting,
            for example, t_step=10, means it will plot every 10 frame of t,
            while t_step=1, will plot every frame possible.

    Returns:
        Does not return anything, will have a plot already loaded to be
        use along with matplotlib.pyplot (`plt.show`).

    """
    cmap = _time_colormap(t)

    for indt in range(0, len(t), t_step):
        ti = t[indt]
        plt.plot(x, y[:, indt], c=cmap(ti))

    plt.xlim(_extend_range(x))
    plt.ylim(_extend_range(y))
    plt.xlabel('$x$')
    plt.ylabel('$y$')

    plt.colorbar(_time_colorbar(t), label='time ($t$)',
                 orientation='horizontal')
    return


def time_plot1D(x, t, t_step=1):
    """Plot several plots overlaid across time for a 1-D particle.

    Utility plotting function that will setup plots of several snapshots in
    time (t) of a the position of a 1-D particle(x). You can control the
    frequency of these plots with t_step, with a higher value indicating less
    frequent plots across time. At some moment after use, `plt.show` should
    be utilized to display the figure.

    Args:
        x (:obj:`np.array`): 1-D array of shape `(n)` representing a spatial
            grid.
        t (:obj:`np.array`): 1-D array of shape `(m)` representing a time grid.
        t_step (int): integer indicating how many frames to skip for plotting,
            for example, t_step=10, means it will plot every 10 frame of t,
            while t_step=1, will plot every frame possible.

    Returns:
        Does not return anything, will have a plot already loaded to be
        use along with matplotlib.pyplot (`plt.show`).

    """
    cmap = _time_colormap(t)
    if not isinstance(x, list):
        x = [x]
    for x_arr in x:
        for indx in range(0, len(t), t_step):
            ti = t[indx]
            xi = x_arr[indx]
            plt.scatter(ti, xi, c=cmap(ti), s=100)

    plt.xlim([np.min(t), np.max(t)])
    plt.ylim(_extend_range(x))
    plt.xlabel('$t$')
    plt.ylabel('$x$')

    plt.colorbar(_time_colorbar(t), label='time ($t$)',
                 orientation='horizontal')
    return


def plot_3d_surface(xx, yy, zz):
    """Plot a 3D surface.

    Based on three `numpy.ndarray` objects xx,yy and zz of the same shape, it will plot
    the surface represented by z on the axis x and y. Typically xx and yy are
    constructed via `np.meshgrid` and then zz by a function evaluation on these
    grids.

    Args:
        xx (:obj:`np.ndarray`): 2-D coordinate array representing a spatial
            grid on the x axis.
        yy (:obj:`np.ndarray`): 2-D coordinate array representing a spatial
            grid on the y axis.
        zz (:obj:`np.ndarray`): 2-D coordinate array representing a spatial
                    grid on the z axis.

    Returns:
        Does not return anything, will have a plot already loaded to be
        use along with matplotlib.pyplot (`plt.show`).

    """
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


def plot_contours(xx, yy, zz, vmin=None, vmax=None):
    """Plot a heatmap and level set contours of a 3d surface.

    Based on three `numpy.ndarray` objects xx,yy and zz of the same shape, it will plot
    a heatmap, a 2D colored image representing values of z across x and y, along
    with several contour level sets, curves where z is constant. Both visualizations
    provide an alternative way of looking at 3-D surfaces in a 2-D projection.

    Args:
        xx (:obj:`np.ndarray`): 2-D coordinate array representing a spatial
            grid on the x axis.
        yy (:obj:`np.ndarray`): 2-D coordinate array representing a spatial
            grid on the y axis.
        zz (:obj:`np.ndarray`): 2-D coordinate array representing a spatial
                    grid on the z axis.
        vmin (float): Mainimum value of z, used to anchor the colormap. 
                      Defaults to None, which means it will calculate it dynamically.
        vmax (float): Maximum value of z, used to anchor the colormap.
                      Defaults to None, which means it will calculate it dynamically.

    Returns:
        Does not return anything, will have a plot already loaded to be
        use along with matplotlib.pyplot (`plt.show`).

    """
    cmap = mpl.cm.get_cmap(COLOR_MAP)
    plt.contour(xx, yy, zz, linewidths=3.0, cmap=cmap)
    CS = plt.contour(xx, yy, zz, colors='k', linewidths=0.5)
    im = plt.imshow(zz, interpolation='nearest', extent=[
        xx.min(), xx.max(), yy.min(), yy.max()], vmin=vmin, vmax=vmax)
    plt.clabel(CS, fontsize='x-small', inline=1)
    _add_colorbar(im, label='z')
    # plt.colorbar()
    plt.xlabel('x')
    plt.ylabel('y')
    return


def _add_colorbar(im, aspect=20, pad_fraction=0.5, **kwargs):
    """Add a vertical color bar to an image plot."""
    divider = axes_grid1.make_axes_locatable(im.axes)
    width = axes_grid1.axes_size.AxesY(im.axes, aspect=1. / aspect)
    pad = axes_grid1.axes_size.Fraction(pad_fraction, width)
    current_ax = plt.gca()
    cax = divider.append_axes("right", size=width, pad=pad)
    plt.sca(current_ax)
    return im.axes.figure.colorbar(im, cax=cax, **kwargs)


def plot_energy_diagram(energy_list):
    """Plot a typical energy diagram based

    Will plot the representation of several energy levels and their associated
    quantum numbers in a energy diagram. It uses as input a list of Energy tuples.

    Args:
        energy_list (:obj:`list`): A list of energy tuples.

    Returns:
        Does not return anything, will have a plot already loaded to be
        use along with matplotlib.pyplot (`plt.show`).

    """
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
        ax.annotate(et.name, xy=(xmin, y - 0.13))
        eprev = et.energy
    return

if __name__ == "__main__":
    print("Load me as a module please")
