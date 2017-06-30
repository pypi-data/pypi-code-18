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


     
def divide_and_conquer(min_bound, max_bound, data, target, func, tolerance=0.0001):
    '''
    min_bound is the minimum bound of the variable which are being optimized
    max_bound is the maximum bound of the variable which are being optimized
    data is a list of values which are needed to evaluate the variable estimate
    func is a function which is used to evaluate the variable estimate, it must take a list conaining data and the estimate
    target is the target value for which we wish to find a corresponding variable value
    tolerance is how close the answer must be
    '''   
    
    # determine the halfpoint between min and max bound   
    midpoint = min_bound + (max_bound - min_bound)/2.0
    
    # calculate an estimated value
    est = func(data, midpoint)

    # if the guess is close enough, return the estimate
    if abs(est - target) <= tolerance:
        return midpoint
    
    # if target is smaller than the estimate
    elif target < est:
        return divide_and_conquer(min_bound, midpoint, data, target, func, tolerance)

    # if target is larger han the estimate
    elif target > est:    
        return divide_and_conquer(midpoint, max_bound, data, target, func, tolerance)
    
   
