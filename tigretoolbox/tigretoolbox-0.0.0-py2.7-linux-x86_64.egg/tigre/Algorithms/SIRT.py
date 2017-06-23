

from __future__ import division
from __future__ import print_function
import time
import os
import sys
from tigre.Utilities.init_multigrid import init_multigrid
import numpy as np
import copy
from _Ax import Ax
from _Atb import Atb
from tigre.Utilities.order_subsets import order_subsets
from tigre.Utilities.Measure_Quality import Measure_Quality as MQ

# TODO: this is quite nasty; it would be nice to reorganise file structure later so top level folder is always in path
currDir = os.path.dirname(os.path.realpath(__file__))
rootDir = os.path.abspath(os.path.join(currDir, '..'))
if rootDir not in sys.path:  # add parent dir to paths
    sys.path.append(rootDir)



def SIRT(proj, geo, alpha, niter,
         lmbda=1, lmbda_red=0.99, OrderStrategy=None, Quameasopts=None, init=None, verbose=True,noneg=True):
    """
        SIRT_CBCT solves Cone Beam CT image reconstruction using Oriented Subsets
                   Simultaneous Algebraic Reconxtruction Techique algorithm

        SIRT_CBCT(PROJ,GEO,ALPHA,NITER) solves the reconstruction problem
        using the projection data PROJ taken over ALPHA angles, corresponding
        to the geometry descrived in GEO, using NITER iterations.

        SIRT_CBCT(PROJ,GEO,ALPHA,NITER,OPT,VAL,...) uses options and values for solving. The
        possible options in OPT are:


        'lambda':      Sets the value of the hyperparameter. Default is 1

        'lambda_red':   Reduction of lambda. Every iteration
                        lambda=lambdared*lambda. Default is 0.99

        'Init':        Describes different initialization techniques.
                       'none'     : Initializes the image to zeros (default)
                       'FDK'      : intializes image to FDK reconstrucition
                       'multigrid': Initializes image by solving the problem in
                                    small scale and increasing it when relative
                                    convergence is reached.
                       'image'    : Initialization using a user specified
                                    image. Not recomended unless you really
                                    know what you are doing.
                        dtype=str

        'InitImg'      an image for the 'image' initialization. Avoid.
                       dtype=np.array([],dtype=np.float32)
        'Verbose'      True or False. Default is True. Gives information about the
                       progress of the algorithm.
        'QualMeas'     Asks the algorithm for a set of quality measurement
                       parameters. Input should contain a string with optional values 'CC',
                       'RMSE','MSSIM' or 'UQI'.
                        dtype = str

        'OrderStrategy' Chooses the subset ordering strategy. Options are
                       'ordered' :uses them in the input order, but divided
                       'random'  : orders them randomply
                       'angularDistance': chooses the next subset with the
                                          biggest angular distance with the ones used.
                        dtype=str
    --------------------------------------------------------------------------
    --------------------------------------------------------------------------
     This file is part of the TIGRE Toolbox

     Copyright (c) 2015, University of Bath and
                         CERN-European Organization for Nuclear Research
                         All rights reserved.

     License:            Open Source under BSD.
                         See the full license at
                         https://github.com/CERN/TIGRE/license.txt

     Contact:            tigre.toolbox@gmail.com
     Codes:              https://github.com/CERN/TIGRE/
    --------------------------------------------------------------------------
     Coded by:           MATLAB (original code): Ander Biguri
                         PYTHON : Sam Loescher, Reuben Lindroos
    """
    if verbose==True:
        print('SIRT algorithm in progress.')

    blocksize = 1
    angles, angle_index = order_subsets(alpha, blocksize, OrderStrategy)
    alpha = angles.ravel()

    #     Projection weight:
    #       - fixing the geometry
    #       - making sure there are no infs in W

    geox = copy.deepcopy(geo)
    geox.sVoxel[0:] = geo.DSD - geo.DSO
    geox.sVoxel[2] = max(geox.sDetector[1], geox.sVoxel[2])
    geox.nVoxel = np.array([2, 2, 2])
    geox.dVoxel = geox.sVoxel / geox.nVoxel
    W = Ax(np.ones(geox.nVoxel, dtype=np.float32), geox, alpha, "ray-voxel")
    W[W < min(geo.dVoxel / 4)] = np.inf
    W = 1 / W
    geox=None

    #     Back_Proj weight
    #     NOTE: hstack(array,last value) as np.arange does not include upper limit of interval.

    if geo.mode != 'parallel':

        start = geo.sVoxel[1] / 2 - geo.dVoxel[1] / 2 + geo.offOrigin[1]
        stop = -geo.sVoxel[1] / 2 + geo.dVoxel[1] / 2 + geo.offOrigin[1]
        step = -geo.dVoxel[1]
        xv = np.arange(start, stop + step, step)

        start = geo.sVoxel[2] / 2 - geo.dVoxel[2] / 2 + geo.offOrigin[2]
        stop = -geo.sVoxel[2] / 2 + geo.dVoxel[2] / 2 + geo.offOrigin[2]
        step = -geo.dVoxel[2]
        yv = -1 * np.arange(start, stop + step, step)

        (yy, xx) = np.meshgrid(yv, xv)
        xx = np.expand_dims(xx, axis=2)
        yy = np.expand_dims(yy, axis=2)

        A = (alpha + np.pi / 2)
        V = (geo.DSO / (geo.DSO + (yy * np.sin(-A)) - (xx * np.cos(-A)))) ** 2
        V=np.sum(V,axis=2)
        V = np.array(V, dtype=np.float32)

    else:
        V = np.ones([geo.nVoxel[0], geo.nVoxel[1]])*len(alpha)
    # Iterate
    lq = []

    if init == 'multigrid':
        if verbose==True:
            print('init multigrid in progress...')
        res= init_multigrid(proj, geo, alpha,alg='SIRT')
        if verbose==True:
            print('init multigrid complete.')
    if init == 'FDK':
        raise ValueError('FDK not implemented as of yet (coming soon)!')

    if type(init) == np.ndarray:
        if (geo.nVoxel==init.shape).all():

            res = init

        else:
            raise ValueError('wrong dimension of array for initialisation')
    elif init==None:
        res=np.zeros(geo.nVoxel, dtype=np.float32)

    tic=None
    toc=time.clock()
    for i in range(niter):
        if Quameasopts != None:
            res_prev = res
        if verbose==True:
            if i==1:
                    print('Esitmated time until completetion (s): '+ str(niter*(tic-toc)))


        # VERBOSE:
        # proj_err = proj-Ax(res,geo,alpha,'interpolated')
        # weighted_err = W*proj_err
        # backprj = Atb(weighted_err,geo,alpha,'FDK')
        # weighted_backprj = 1/V*backprj
        # res+=lmbda*weighted_backprj

        res += lmbda *1/V* Atb(W*(proj- Ax(res, geo, alpha, 'ray-voxel')), geo,
                                      alpha, 'FDK')
        if noneg:
            res = res.clip(min=0)
        if Quameasopts != None:
            lq.append(MQ(res, res_prev, Quameasopts))
            res_prev = res

        tic=time.clock()


    lmbda *= lmbda_red
    if Quameasopts != None:
        return res.transpose(), lq
    else:
        return res.transpose()



