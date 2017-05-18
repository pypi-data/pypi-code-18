#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'ByStudent'
from .RSA_Wiener_ContinuedFractions import *
from .RSA_Wiener_Arithmetic import *
import sys
sys.setrecursionlimit(1000000)
def RSA_Wiener(e,n):
    '''
    Finds d knowing (e,n)
    applying the Wiener continued fraction attack
    '''
    frac = rational_to_contfrac(e, n)
    convergents = convergents_from_contfrac(frac)

    for (k,d) in convergents:

        # check if d is actually the key
        if k!=0 and (e*d-1)%k == 0:
            phi = (e*d-1)//k
            s = n - phi + 1
            discr = s*s - 4*n
            if(discr >= 0):
                t = is_perfect_square(discr)
                if t!=-1 and (s+t)%2==0:
                    return "d = " + str(d)





