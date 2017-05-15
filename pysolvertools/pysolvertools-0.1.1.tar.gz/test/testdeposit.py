#! /usr/bin/python
import numpy as np

from optparse      import OptionParser
from copy          import deepcopy
from scipy.special import erf

import pysolvertools

SIGMA         = 0.1
N_GRID_1D     = 256
N_GRID_2D     = 128
N_GRID_3D     = 32
SYSTEM_LENGTH = 2.0
N_PARTICLES   = int(1e7)

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


def generateNeumannCondition(dim):
    """
    Generate the initial condition and the analytical solution for
    the periodic case.
    :returns: Dictionnary containing 'solution', 'position' and 'weight'
    """
    L = SYSTEM_LENGTH
    
    # Compute the analytical solution
    x = np.linspace(0,SYSTEM_LENGTH,N_grid)
    if dim == 1:
        rho  = np.exp( -0.5*(x-L/2.0)**2/SIGMA**2 ) / (2*SIGMA**2*np.pi)**0.5
    elif dim == 2:
        X, Y = np.meshgrid(x,x,indexing='ij')
        rho  = np.exp( -0.5*(X-L/2.0)**2/SIGMA**2 ) / (2*SIGMA**2*np.pi)
        rho *= np.exp( -0.5*(Y-L/2.0)**2/SIGMA**2 )
    elif dim == 3:
        X, Y, Z = np.meshgrid(x,x,x,indexing='ij')
        rho  = np.exp( -0.5*(X-L/2.0)**2/SIGMA**2 ) / (2*SIGMA**2*np.pi)**1.5
        rho *= np.exp( -0.5*(Y-L/2.0)**2/SIGMA**2 )
        rho *= np.exp( -0.5*(Z-L/2.0)**2/SIGMA**2 )
    else:
        raise ValueError("Please reduce the number of dimensions (<=3)")
    
    # Create the sample to test
    weight = np.ones( N_PARTICLES, dtype=np.float32 )
    pos    = np.random.normal(
        loc   = [L/2.0]*dim,
        scale = SIGMA,
        size  = ( N_PARTICLES,dim ) ).astype(np.float32)
    return {"position": pos,
            "weight"  : weight,
            "density" : rho}

def generateDirichletCondition(dim):
    """
    Generate the initial condition and the analytical solution for
    the non-periodic case.
    :returns: Dictionnary containing 'solution', 'position' and 'weight'
    """
    # Compute the analytical solution
    scale   = 1.0 / SYSTEM_LENGTH**dim
    rho     = scale * np.ones([N_grid]*dim)

    # Dimensional cases
    if dim == 1:
        rho[0]  = 0.5 * scale
        rho[-1] = 0.5 * scale
    elif dim == 2:
        rho[0,:]  = 0.5 * scale
        rho[:,0]  = 0.5 * scale

        rho[-1,:] = 0.5 * scale
        rho[:,-1] = 0.5 * scale
    elif dim == 3:
        rho[0,:,:]  = 0.5 * scale
        rho[:,0,:]  = 0.5 * scale
        rho[:,:,0]  = 0.5 * scale

        rho[-1,:,:] = 0.5 * scale
        rho[:,-1,:] = 0.5 * scale
        rho[:,:,-1] = 0.5 * scale
    else:
        raise ValueError("Please reduce the number of dimensions (<=3)")        
    
    # Create the sample to test
    weight = np.ones( N_PARTICLES, dtype=np.float32 )
    pos    = np.random.rand(N_PARTICLES,dim) * SYSTEM_LENGTH
    pos    = pos.astype(np.float32)

    return {"position": pos,
            "weight"  : weight,
            "density" : rho}


def plotSolutions(sol, rho, dim):
    import matplotlib.pyplot as plt
    if dim == 1:
        plt.plot(rho)
        plt.plot(sol)
    elif dim == 2:
        plt.figure()
        plt.title("Diff")
        plt.contourf(rho-sol)
        plt.colorbar()
        plt.figure()
        plt.title("Density")
        plt.contourf(rho)
        plt.colorbar()
        plt.figure()
        plt.title("Num Sol")
        plt.contourf(sol)
        plt.colorbar()
    plt.show()


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
        

def testDeposit(periodic, dim, dev=False):
    """
    Create a random data set, compute the distribution with pySolverTools
    and compare the result with the analytical solution.
    :param int periodic: Are the boundaires periodic
    :param int dim: Number of dimensions
    :returns: Relative error
    """
    updateNgrid(dim)
    
    # define the system
    L  = [SYSTEM_LENGTH]*dim
    N  = [N_grid]*dim
    dx = L[0]/(N[0]-1)

    # generate sample and solution
    if periodic:
        tmp = generateNeumannCondition(dim)
    else:
        tmp = generateDirichletCondition(dim)
    rho    = tmp["density"]
    pos    = tmp["position"]
    weight = tmp["weight"]
    
    # Compute the numerical solution
    sol = pysolvertools.deposit(pos, weight, L, N, periodic=periodic)/(N_PARTICLES*dx**dim)

    # Compute the relative error
    err = np.sqrt((np.sum((sol-rho)**2) / np.sum(rho**2)))

    if dev:
        plotSolutions(sol,rho,dim)
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
    err = testDeposit(opt.periodic, opt.dim, opt.dev)

    # test the error
    if err < opt.eps:
        print "Test: Deposit in %iD with %s boundaries passed" % (opt.dim, txt)
        print "Accuracy: %g" % err
    else:
        print "Test: Deposit in %iD with %s boundaries FAILED" % (opt.dim, txt)
        raise ValueError("Test FAILED with an error of %g" % err)
