#!/usr/bin/env python3


#This script deals with optimizations.
#
#copyright (C) 2017  Martin Engqvist | martin_engqvist@hotmail.com
#
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#LICENSE:
#
#This script is free software; you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation; either version 3 of the License, or
#(at your option) any later version.
#
#This script is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU Library General Public License for more details.
#
#You should have received a copy of the GNU General Public License
#along with this program; if not, write to the Free Software Foundation,
#Inc., 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301  USA
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#



def calculate_linear_bezier(points, t):
    '''
    Points is a list of two points, P0 and P1, in that order
    '''
    #assign values to variables
    P0, P1 = points

    #calculate value of bezier curve at the given t
    Bt = P0 + t*(P1 - P0)

    return Bt



def calculate_quadratic_bezier(points, t):
    '''
    Points is a list of three points, P0, P1 and P2, in that order
    '''
    #assign values to variables
    P0, P1, P2 = points

    #calculate value of bezier curve at the given t
    Bt = (1-t)*( (1-t)*P0 + t*P1 ) + t*( (1-t)*P1 + t*P2 )

    return Bt



def calculate_cubic_bezier(points, t):
    '''
    Points is a list of four points, P0, P1, P2 and P3, in that order
    '''
    #assign values to variables
    P0, P1, P2, P3 = points

    #calculate value of bezier curve at the given t
    Bt = (1-t)**3 * P0 + 3*(1-t)**2 * t * P1 + 3*(1-t) * t**2 * P2 + t**3 * P3

    return Bt
