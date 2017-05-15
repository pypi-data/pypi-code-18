#! /usr/bin/python

import numpy as np

from optparse      import OptionParser
from copy          import deepcopy
from scipy.special import erf

import pysolvertools

SIGMA         = 0.1
N_GRID_1D     = 1024
N_GRID_2D     = 512
N_GRID_3D     = 128
SYSTEM_LENGTH = 2.0

N_grid        = None

def parseOptions():
    """
    Parse the options given in command line and return them.
    """

    usage = "usage: %prog [options] file"
    parser = OptionParser(usage=usage)

    parser.add_option("--dim",
                      action  = "store",
                      dest    = "dim",
                      type    = int,
                      default = 1,
                      help    = "Number of dimension",
                      metavar = " INT")

    parser.add_option("--periodic",
                      action  = "store",
                      dest    = "periodic",
                      type    = int,
                      default = 1,
                      help    = "Test periodic case",
                      metavar = " INT")
    
    parser.add_option("--epsilon",
                      "--eps",
                      action  = "store",
                      dest    = "eps",
                      type    = float,
                      default = 5e-2,
                      help    = "Error thresold to fail the test",
                      metavar = " FLOAT")

    parser.add_option("--dev",
                      action  = "store_true",
                      dest    = "dev",
                      default = False)

    (options, args) = parser.parse_args()

    return options


def updateNgrid(dim):
    global N_grid
    if dim == 1:
        N_grid = N_GRID_1D
    elif dim == 2:
        N_grid = N_GRID_2D
    elif dim == 3:
        N_grid = N_GRID_3D
    else:
        raise ValueError("Please reduce the number of dimensions (<=3)")        

    
def generateNeumannCondition(dim):
    """
    Generate the initial condition and the analytical solution for
    the periodic case.
    :returns: Dictionnary containing 'density' and 'potential'
    """
    # few constant
    L = SYSTEM_LENGTH
    x = np.linspace(0,L,N_grid)
    
    scaling = -4*np.pi**2/L**2

    # dimensional cases
    if dim == 1:
        rho = np.cos(2*np.pi*x/L)
        pot = deepcopy(rho) / scaling
    elif dim == 2:
        X,Y = np.meshgrid(x,x,indexing='ij')

        rho = ( np.sin(2*np.pi*X/L)
              + np.cos(2*np.pi*Y/L) )

        pot = deepcopy(rho) / scaling
    elif dim == 3:
        X,Y,Z = np.meshgrid(x,x,x,indexing='ij')

        rho   = ( np.sin(2*np.pi*X/L)
                + np.cos(2*np.pi*Y/L)
                + np.sin(2*np.pi*Z/L) )

        pot   = deepcopy(rho) / scaling
    else:
        raise ValueError(
            "Please reduce the number of dimensions (<=3)")
    
    return {"density"   : rho.astype(np.float32),
            "potential" : pot.astype(np.float32)}

def generateDirichletCondition(dim):
    """
    Generate the initial condition and the analytical solution for
    the non-periodic case.
    :returns: Dictionnary containing 'density' and 'potential'
    """
    # few constant
    L     = SYSTEM_LENGTH
    x     = np.linspace(0,L,N_grid)

    # dimensional cases
    if dim == 1:
        pot  = np.exp( -0.5*(x-L/2.0)**2 / SIGMA**2 )
        rho  = deepcopy(pot)
        rho *= ( ( x-L/2.0 )**2 - SIGMA**2 ) / SIGMA**4
    elif dim == 2:
        X,Y  = np.meshgrid(x,x,indexing='ij')
        pot  = np.exp(-0.5*((X-L/2.0)**2
                          + (Y-L/2.0)**2) / SIGMA**2)
        rho  = deepcopy(pot)
        rho *= ( (X-L/2.0)**2
               + (Y-L/2.0)**2
               - 2*SIGMA**2   ) / SIGMA**4
    elif dim == 3:
        X,Y,Z = np.meshgrid(x,x,x,indexing='ij')
        pot   = np.exp(-0.5*( (X-L/2.0)**2
                            + (Y-L/2.0)**2
                            + (Z-L/2.0)**2 )/SIGMA**2)
        rho   = deepcopy(pot)
        rho  *= ( (X-L/2.0)**2
                + (Y-L/2.0)**2
                + (Z-L/2.0)**2
                - 3*SIGMA**2  )/SIGMA**4
    else:
        raise ValueError("Please reduce the number of dimensions (<=3)")        

    return {"density"   : rho.astype(np.float32),
            "potential" : pot.astype(np.float32)}


def plotSolutions(sol, pot, dim):
    import matplotlib.pyplot as plt
    if dim == 1:
        plt.plot(pot)
        plt.plot(sol)
    elif dim == 2:
        plt.figure()
        plt.title("Diff")
        plt.contourf(pot-sol)
        plt.colorbar()
        plt.figure()
        plt.title("Density")
        plt.contourf(pot)
        plt.colorbar()
        plt.figure()
        plt.title("Num Sol")
        plt.contourf(sol)
        plt.colorbar()
    elif dim == 3:
        plt.figure("Diff XY")
        N = int( N_grid/2 )
        plt.contourf(sol[:,:,N]-pot[:,:,N])
        plt.colorbar()
        plt.figure("Pot XY")
        N = int( N_grid/2 )
        plt.contourf(pot[:,:,N])
        plt.colorbar()
        plt.figure("Num XY")
        N = int( N_grid/2 )
        plt.contourf(sol[:,:,N])
        plt.colorbar()
    plt.show()

    
def testPoisson(periodic, dim, dev=False):
    """
    Compute the potential of a distribution with an analytical
    solution and then compare the two.
    :param int periodic: Are the boundaires periodic
    :param int dim: Number of dimensions
    :returns: Relative error
    """
    updateNgrid(dim)
    L  = [SYSTEM_LENGTH]*dim

    # generate initial condition
    if periodic:
        tmp = generateNeumannCondition(dim)
    else:
        tmp = generateDirichletCondition(dim)

    rho = tmp["density"]
    pot = tmp["potential"]

    # compute the solution and its error
    sol = pysolvertools.poissonSolver(rho, L, periodic)
    err = np.sqrt((np.sum((sol-pot)**2) / np.sum(pot**2)))

    if dev:
        plotSolutions(sol,pot,dim)

    return err

        
if __name__ == "__main__":

    # Parse the options
    opt = parseOptions()

    # print informations
    if opt.periodic == 1:
        txt = "periodic"
    elif opt.periodic == 0:
        txt = "non-periodic"
    else:
        raise ValueError("Periodic boundaries boolean set to %i" % periodic)
    print "Testing deposit function in %iD with %s boundaries" % (opt.dim, txt)
    

    # Compute the relative error
    err = testPoisson(opt.periodic, opt.dim, opt.dev)

    # test the error
    if err < opt.eps:
        print "Test: Deposit in %iD with %s boundaries passed" % (opt.dim, txt)
        print "Accuracy: %g" % err
    else:
        print "Test: Deposit in %iD with %s boundaries FAILED" % (opt.dim, txt)
        raise ValueError("Test FAILED with an error of %g" % err)
