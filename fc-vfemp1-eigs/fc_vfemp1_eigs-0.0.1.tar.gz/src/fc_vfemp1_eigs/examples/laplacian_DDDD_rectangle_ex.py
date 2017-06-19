import numpy as np
import os

from fc_tools.others import isModuleFound

from fc_oogmsh import gmsh
from fc_vfemp1_eigs.sys import get_geo
from fc_simesh.siMesh import siMesh,HyperCube
from fc_vfemp1.operators import Loperator,Lmass
from fc_vfemp1.BVP import BVP,PDE

import fc_vfemp1_eigs.lib as elib

def run(**kwargs):
  """
  Solves the Dirichlet eignevalue problem for the laplacian on [0,L]x[0,H] 
  and plots the eigenfunctions
      * `run(verbose=10)`
          prints the eBVP 
      * `res=run()`
          Solves the eBVP, plots some eigenfunctions and returns some results as *dict*.
      * `res=run(N=100,k=12)`
          Computes the 12 first eigenvalues of the eBVP with their corresponding eigenfunctions, 
          plots the numerical eigenfunctions and returns some results as *dict*.
      * `res=run(regular=False)`
          Uses **gmsh** for the mesh, solves the eBVP, plots the solutions and 
          returns some results as *dict*.
      
  Optional (key/value) parameters
  -------------------------------
  `N` : integer (150 by default)
      mesh size grows with `N`.
  `L` : real >0 (3 by default)
      Width of the rectangle [0,L]x[0,H]
  `H` : real >0 (2 by default)
      Height of the rectangle [0,L]x[0,H]
  `k` : integer (6 by default)
      The number of eigenvalues and eigenvectors desired.
  `sigma` : real or complex (0 by default)    
      Find eigenvalues near sigma using shift-invert mode.
      see help of the function scipy.sparse.linalg.eigs
  `graphics` : boolean  
      The coordinates of mesh nodes.
  `verbose` : integer (1 by default)
      No verbosity for 0 value. With `verbose=10` only print the BVP.
  `regular` : boolean (`True` by default).
      If True, uses `HyperCube` function (regular mesh) otherwise uses **gmsh**
      and *rect4.geo* file to generate the mesh.
  `trans` : boolean (`True` by default).    
      Transform the numerical eigenfunctions by ...
  """
  N=kwargs.get('N',150)
  NumEigs=kwargs.get('k',6)
  L=kwargs.get('L',3)
  H=kwargs.get('H',2)
  regular=kwargs.pop('regular',True) # True uses HyperCube function otherwise uses gmsh
  sigma=kwargs.get('sigma',0)
  verbose=kwargs.pop('verbose',1)
  trans=kwargs.get('trans',True)
  graphics=kwargs.get('graphics',True)
  colorbar=kwargs.get('colorbar',False)
  gsolex=kwargs.get('gsolex',True) # draw exact eigenfunctions
  gsolnum=kwargs.get('gsolnum',True) # draw numerical eigenfunctions
  if trans: 
    gerror=kwargs.get('gerror',True) # draw errors on eigenfunctions
  else:
    gerror=False
  if not regular:
    geofile='rect4'
    (geodir,geofile)=get_geo(2,2,geofile)
    geoFile=geodir+os.sep+geofile+'.geo'
  if verbose>0:
    elib.print_separator()
    elib.PrintCopyright()
    elib.print_separator()
    print('      Dirichlet eigenvalue problem for the Laplacian on [0,%d]x[0,%d]'%(L,H))
    if regular:
      print('      Mesh generated with HyperCube function.\n')
    else:
      print('      Mesh generated with gmsh and %s.geo file.\n'%geofile)
    print('               -Laplacian(u) = lambda*u\n')
    print(' and Dirichlet boundary conditions :')
    print('   * u=0 on [1,2,3,4]')
    elib.print_separator()
  if verbose==10:
    return
  if regular:
    if verbose>0:
      print('*** Setting the mesh using HyperCube function [fc_simesh]')
    Th=HyperCube(2,N,mapping=lambda q:np.array([L*q[0],H*q[1]]))
  else:
    if verbose>0:
      print('*** Setting the mesh using gmsh and %s.geo file.'%geofile)
    meshfile=gmsh.buildmesh2d(geoFile,N, force=True,verbose=0 ,options='-smooth 4 -setnumber H %g -setnumber L %g'%(H,L))
    Th=siMesh(meshfile)
  if verbose>0:
    print('     Mesh sizes : nq=%d, nme=%d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
  if verbose>0:
    print('*** Setting the eBVP')
  Lop=Loperator(dim=2,A=[[1,None],[None,1]])
  pde=PDE(Op=Lop)
  bvp=BVP(Th,pde=pde)
  for lab in Th.sThlab[Th.find(d=1)]:
    bvp.setDirichlet(lab,0.)
  if verbose>0:
    print('*** Solving the eBVP')
  eigVals,eigVecs= elib.eBVPsolve(bvp,k=NumEigs,which='LM', sigma=sigma,tol=1e-6,maxiter=Th.nq)
  
  assert np.max(np.abs(eigVecs.imag))<1e-15, "Eigenfunctions must be real, found %g"%np.max(np.abs(eigVecs.imag))
  assert np.max(np.abs(eigVals.imag))<1e-15 and np.min(eigVals.real)>0, "Eigenvalues must be real positive"
  eigVals=eigVals.real
  eigVecs=eigVecs.real
  
  if verbose>0:
    print('*** Computing exacts solutions to the eBVP')
  eigValsEx,eigVecsEx=elib.LaplacianDDDDEigenOnRectangle(Th,L,H,NumEigs)
  if trans:
    eigVecTrans=elib.L2_complete_trans(Th,eigValsEx,eigVecs,eigVecsEx)
  else:
    eigVecTrans=eigVecs
  if trans:
    if verbose>0:
      print('*** Computing errors')
    eVecL2,eVecH1,eVal=elib.errors(Th,eigVals,eigVecTrans,eigValsEx,eigVecsEx)
    if verbose>0:
      for i in range(NumEigs):
        print('  %2d: lambda=%.3f..., error=%.5e'%(i+1,eigValsEx[i],eVal[i]))
        print('        L2-error=%.5e, H1-error=%.5e'%(eVecL2[i],eVecH1[i]))

  if graphics and isModuleFound('fc_simesh_matplotlib'):
    if verbose>0:
      print('*** Plotting eigenfunction')
    import matplotlib.pyplot as plt
    import fc_simesh_matplotlib.siMesh as siplt
    from fc_tools.matplotlib import set_axes_equal,DisplayFigures, error_colorbar_format
    from fc_vfemp1_eigs.matplotlib import ploteigs
    plt.close('all')
    plt.ion()
    sft=error_colorbar_format()
    for i in range(NumEigs):
      if gsolex:
        plt.figure()
        siplt.plot(Th,eigVecsEx[:,i])
        if colorbar:
          plt.colorbar()
        siplt.plotiso(Th,eigVecsEx[:,i],isorange=[0],color='LightGray',linewidth=2)
        set_axes_equal()
        plt.axis('off')
        plt.title('$\\lambda^{\\rm ex}_{%d}=%.3f$'%(i+1,eigValsEx[i]))
      if gsolnum:
        plt.figure()
        siplt.plot(Th,eigVecTrans[:,i])
        if colorbar:
          plt.colorbar()
        siplt.plotiso(Th,eigVecTrans[:,i],isorange=[0],color='LightGray',linewidth=2)
        set_axes_equal()
        plt.axis('off')
        plt.title('$\\lambda^{\\rm num}_{%d}=%.3f$'%(i+1,eigVals[i]))
      if gerror:
        plt.figure()
        siplt.plot(Th,abs(eigVecsEx[:,i]-eigVecTrans[:,i]),cmap='jet')
        plt.colorbar(format=sft)
        set_axes_equal()
        plt.axis('off')
        plt.title('$\\lambda^{\\rm error}_{%d}=%.3e$'%(i+1,(eigValsEx[i]-eigVals[i])/(1+abs(eigValsEx[i]))))
    DisplayFigures()
  if trans:  
    return {'bvp':bvp,'eigVal':eigVals,'eigVec':eigVecTrans,
            'eigValEx':eigValsEx,'eigVecEx':eigVecsEx,
            'eVecL2':eVecL2,'eVecH1':eVecH1,'eVal':eVal}
  else:
    return {'bvp':bvp,'eigVal':eigVals,'eigVec':eigVecs}

def order(**kwargs):
  """
  Prints and plots orders of solutions of the BVP 
  
     `order()`
     `order(LN=[25,50,75,100])`
     `order(LN=[25,50,75,100],regular=False)`
            
  Optional (key/value) parameters
  -------------------------------
  `LN` : array or list of integers
      mesh size grows with `N in LN`.
  `graphics`: boolean (True by default)
      
  Others options are those of 
  * the `run` function in this file,
  * the `solve` function of class `BVP`:
    `solver` : to specify a solver for a sparse system A*x=b.
        Default is `solver=lambda A,b: scipy.sparse.linalg.spsolve(A,b)`
      
    `perm`   : to specify permutation in the sparse matrix. For example
        `perm=lambda A: scipy.sparse.csgraph.reverse_cuthill_mckee(A)`
  """  
  graphics=kwargs.get('graphics',True)
  res_order=elib.generic_orders(run,**kwargs)
  if graphics and isModuleFound('fc_simesh_matplotlib'):
    import matplotlib.pyplot as plt
    from fc_tools.matplotlib import DisplayFigures
    from fc_vfemp1_eigs.matplotlib import plot_orders
    plt.close('all')
    plt.ion()
    plot_orders(res_order) 
  return res_order