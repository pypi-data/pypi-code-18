# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 10:01:19 2017

@author: danaukes
"""
import pygmsh as pg
import numpy

def gen_verts(polygon):
    poly4= list(polygon.coords)
    poly4 = poly4[:-1]
    poly4 = numpy.r_[poly4]
    poly4 = numpy.c_[poly4,poly4[:,0]*0]
    return poly4

def shapely_to_pygmsh(poly,lcar = 1e-1):
    geom = pg.Geometry()
    
    holes = []
    for interior in poly.interiors:
        hole = geom.add_polygon(gen_verts(interior)[::1], lcar,make_surface=False)
        holes.append(hole.line_loop)
    
    poly = geom.add_polygon(gen_verts(poly.exterior)[::-1],lcar,holes=holes)    
    
    return geom,poly