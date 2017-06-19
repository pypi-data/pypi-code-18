from fc_tools.others import isModuleFound
assert isModuleFound('fc_vfemp1_biharmonic'),'Package fc_vfemp1_biharmonic must be installed to run this example'

import numpy as np
import os
from numpy import pi,cos,sin

from fc_oogmsh import gmsh
from fc_simesh.siMesh import siMesh,HyperCube
from fc_vfemp1.operators import Loperator,Lmass,Hoperator,Hmass,StiffElasHoperator
from fc_vfemp1.FEM import NormL2,AssemblyP1
from fc_vfemp1.BVP import BVP,PDE
import fc_vfemp1_biharmonic.lib as blib
import fc_vfemp1_eigs.lib as elib
from fc_vfemp1_eigs.sys import get_geo

def run(**kwargs):
  N=kwargs.get('N',100)
  NumEigs=kwargs.get('k',6) 
  sigma=kwargs.get('sigma',0)
  regular=kwargs.pop('regular',True) # True uses HyperCube function otherwise uses gmsh
  L=kwargs.get('L',2)
  H=kwargs.get('H',1)
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
    print('      2D biharmonic eigenvalues BVP on [0,%d]x[0,%d]'%(L,H))
    if regular:
      print('      Mesh generated with HyperCube function.\n')
    else:
      print('      Mesh generated with gmsh and %s.geo file.\n'%geofile)
    print('               Laplacian(laplacian(u)) = lambda*u\n')
    print(' and simply supported plate boundary conditions :')
    print('   * u=0 and Laplacian(u)=0  on [1,2,3,4]')
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
    meshfile=gmsh.buildmesh2d(geoFile,N, force=True,verbose=0,options='-smooth 4 -setnumber H %g -setnumber L %g'%(H,L))
    Th=siMesh(meshfile)
  if verbose>0:
    print('     Mesh sizes : nq=%d, nme=%d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
  if verbose>0:
    print('*** Setting the eBVP')
  bvp=blib.BiharmonicBVP(Th)
  for lab in Th.sThlab[Th.find(d=1)]:
    blib.setSimplySupportedPlate(bvp,lab,[0,0])
  Bop=Hoperator(dim=2,m=2)
  Bop.H[0][0]=Loperator(dim=2,a0=1)  
  if verbose>0:
    print('*** Solving the eBVP')
  eigVal,eigVec= elib.eBVPsolve(bvp,RHSop=Bop,k=NumEigs, which='LM',sigma=sigma,tol=1e-9,maxiter=Th.nq)
  
  assert np.max(np.abs(eigVec.imag))<1e-15, "Eigenfunctions must be real"
  assert np.max(np.abs(eigVal.imag))<1e-15 and np.min(eigVal.real)>0, "Eigenvalues must be real positive"
  eigVal=eigVal.real
  eigVec=eigVec.real
  
  eigValEx,eigVecEx=elib.BiharmonicSSPEigenOnRectangle(Th,L,H,NumEigs)
  eigVcomp0=elib.eigenvectors_component(bvp,eigVec,0)
  if trans: # transformation
    eigVecTrans=elib.L2_complete_trans(Th,eigValEx,eigVcomp0,eigVecEx)
  else:
    eigVecTrans=eigVcomp0
    
  
  eVecL2,eVecH1,eVal=elib.errors(Th,eigVal,eigVecTrans,eigValEx,eigVecEx)
  if verbose>0:
    for i in range(NumEigs):
      print('  %2d: lambda=%.3f..., error=%.5e'%(i+1,eigValEx[i],eVal[i]))
      print('        L2-error=%.5e, H1-error=%.5e'%(eVecL2[i],eVecH1[i]))

  if graphics and isModuleFound('fc_simesh_matplotlib'):
    if verbose>0:
      print('*** Plotting eigenfunctions')
    import matplotlib.pyplot as plt
    import fc_simesh_matplotlib.siMesh as siplt
    from fc_tools.matplotlib import set_axes_equal,DisplayFigures, error_colorbar_format
    from fc_vfemp1_eigs.matplotlib import ploteigs

    plt.close('all')
    plt.ion()
    
    for i in range(NumEigs):
      if gsolex:
        plt.figure()
        siplt.plot(Th,eigVecEx[:,i])
        if colorbar:
          plt.colorbar()
        siplt.plotiso(Th,eigVecEx[:,i],isorange=[0],color='LightGray',linewidth=2)
        set_axes_equal()
        plt.axis('off')
        plt.title('$\\lambda^{\\rm ex}_{%d}=%.3f$'%(i+1,eigValEx[i]))
      if gsolnum:
        plt.figure()
        siplt.plot(Th,eigVecTrans[:,i].real)
        if colorbar:
          plt.colorbar()
        siplt.plotiso(Th,eigVecTrans[:,i].real,isorange=[0],color='LightGray',linewidth=2)
        set_axes_equal()
        plt.axis('off')
        plt.title('$\\lambda^{\\rm num}_{%d}=%.3f$'%(i+1,eigVal[i].real))
    
    if gerror:
      sft=error_colorbar_format()
      for i in range(NumEigs):
        tmp=eigVecTrans[:,i]#/max(abs(eigVecTrans[:,i]))
        plt.figure()
        siplt.plot(Th,abs(eigVecEx[:,i]-eigVecTrans[:,i]),cmap='jet')
        plt.colorbar(format=sft)
        set_axes_equal()
        plt.axis('off')
        plt.title('$\\lambda^{\\rm ex}_{%d}=%.3f$'%(i+1,eigValEx[i]))
    DisplayFigures()
    
  return {'bvp':bvp,'Bop':Bop,'eigVal':eigVal,'eigVec':eigVecTrans,
          'eigValEx':eigValEx,'eigVecEx':eigVecEx,
          'eVecL2':eVecL2,'eVecH1':eVecH1,'eVal':eVal}
    
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