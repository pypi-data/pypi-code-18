#! /usr/bin/python3

import math
import numpy as np
import pdb
import os

import matplotlib.pyplot as plt
from scipy.interpolate import griddata

from gfa.field_analysis import geometry as geo
from gfa.field_analysis import field
from gfa.field_analysis.fun_fig import vorticity_figure
from gfa.load_param import Config


def main():
    # cargar malla
    dir_path = os.path.dirname(os.path.realpath(__file__))
    path_node = "{}/../example_files/malla.node".format(dir_path)
    path_ele = "{}/../example_files/malla.ele".format(dir_path)
    x_triangulos = np.loadtxt(path_node, usecols=[1], skiprows=1)
    y_triangulos = np.loadtxt(path_node, usecols=[2], skiprows=1)
    origen = [-76, -46]

    # cargar los datos
    dataset = '{}/../example_files/vect2007_2010'.format(dir_path)
    lon_gps = np.loadtxt(dataset, usecols=[1])
    lat_gps = np.loadtxt(dataset, usecols=[2])
    v_n_gps = np.loadtxt(dataset, usecols=[4])
    v_e_gps = np.loadtxt(dataset, usecols=[3])

    # conversion mm/año a m/año
    v_e_gps = v_e_gps/1000
    v_n_gps = v_n_gps/1000

    # proyectar malla y puntos gps
    malla_proj = geo.geo2proj(x_triangulos, y_triangulos, origen[0], origen[1])
    gps_proj = geo.geo2proj(lon_gps, lat_gps, origen[0], origen[1])

    # interpolar en puntos de malla triangular
    vy_tri = griddata(gps_proj, v_n_gps, malla_proj, method='cubic')
    vx_tri = griddata(gps_proj, v_e_gps, malla_proj, method='cubic')

    # cardozo&allmendinger strain
    u = np.reshape([v_e_gps, v_n_gps], 2*len(v_e_gps), order='F')
    gradiente = field.distance_weigthed2d(u, lon_gps, lat_gps, alfa=100000)
    # tensor calculations
    S, W = field.velocitytensor_2d(gradiente[0], gradiente[1],
                                   gradiente[2], gradiente[3])
    wz = field.vertical_vorticity2d(W)
    # ############################################################################
    # Graficar
    # ############################################################################ht
    fig = vorticity_figure(lon_gps, lat_gps, wz)
    fname = "{}/../example_files/vorticity_weight.png".format(dir_path)
    plt.savefig(fname, dpi=500, edgecolor='k', orientation='portrait',
                bbox_inches=None, pad_inches=0.1)

    print('end function')


main()
