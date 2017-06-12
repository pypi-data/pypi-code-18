from constants import *
from math import *
import numpy as np
from numba import jit

def cylinderModeOde(t, C_in, n, m, cooker, grain):        
    beta = grain.beta
    gamma = grain.gamma
    delta = cooker.delta
    tau = cooker.tau
    theta = cooker.theta
    l = grain.l
    tf = cooker.tf

    lbda = cooker.lbda
    d_i = grain.d_i
    cif = grain.cif
   
    temp = cooker._interpolateTemp(t)

    part2 = (lbda*isotop*np.exp(lbda*(tf-t))*cif*((1-(-1)**n)*
             (2+ALPHA[m-1]**2*d_i**2)*(8*l**2+n**2*pi**2*d_i**2)) / 
             (n*pi*ALPHA[m-1]*BesJ1(ALPHA[m-1])*(4*l**2+pi**2*n**2*d_i**2) * 
             (1+d_i**2*(ALPHA[m-1])**2)))
    C_out = (-beta * (ALPHA[m-1]**2 + (n*pi/l)**2)*C_in*np.exp((-1.0*gamma*temp)/((1.0)-delta*temp))
            + sum(part2))
    return C_out

def cylinderModeOdeint(C_in, t, n, m, cooker, grain):        
    beta = grain._get_beta(t)
    gamma = grain._get_gamma(t)
    delta = cooker.delta
    tau = cooker.tau
    theta = cooker.theta
    l = grain.l
    tf = cooker.tf

    lbda = cooker.lbda
    d_i = grain.d_i
    cif = grain.cif
   
    temp = cooker._interpolateTemp(t)

    part2 = (lbda*isotop*np.exp(lbda*(tf-t))*cif*((1-(-1)**n)*
             (2+ALPHA[m-1]**2*d_i**2)*(8*l**2+n**2*pi**2*d_i**2)) / 
             (n*pi*ALPHA[m-1]*BesJ1(ALPHA[m-1])*(4*l**2+pi**2*n**2*d_i**2) * 
             (1+d_i**2*(ALPHA[m-1])**2)))
    C_out = (-beta * (ALPHA[m-1]**2 + (n*pi/l)**2)*C_in*np.exp((-1.0*gamma*temp)/((1.0)-delta*temp))
            + sum(part2))
    return C_out
