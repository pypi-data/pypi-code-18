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
  verbose=kwargs.pop('verbose',1)
  graphics=kwargs.get('graphics',True)
  colorbar=kwargs.get('colorbar',False)
 
  geofile='disk5holes'
  (geodir,geofile)=get_geo(2,2,geofile)
  geoFile=geodir+os.sep+geofile+'.geo'
  if verbose>0:
    elib.print_separator()
    elib.PrintCopyright()
    elib.print_separator()
    print('      Mesh generated with gmsh and %s.geo file.\n'%geofile)
    print('               Laplacian(laplacian(u)) = lambda*u\n')
    print('  with boundary conditions')
    print('   * Clamped Plate (CP)')
    print('       u=0 and du/dn=0 on [1,10]')
    print('   * Simply Supported Plate (SSP)')
    print('       u=0 and Laplacian(u)=0 on [20,21,22,23]')
    elib.print_separator()
  if verbose==10:
    return
  if verbose>0:
    print('*** Setting the mesh using gmsh and %s.geo file.'%geofile)
  meshfile=gmsh.buildmesh2d(geoFile,N, force=True,verbose=0,options='-smooth 4')
  Th=siMesh(meshfile)
  if verbose>0:
    print('     Mesh sizes : nq=%d, nme=%d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
  if verbose>0:
    print('*** Setting the eBVP')
    
  bvp=blib.BiharmonicBVP(Th)
  blib.setClampedPlate(bvp,1,[0,0])
  blib.setClampedPlate(bvp,10,[0,0])
  for lab in [20,21,22,23]:
    blib.setSimplySupportedPlate(bvp,lab,[0,0])
  Bop=Hoperator(dim=2,m=2)
  Bop.H[0][0]=Loperator(dim=2,a0=1)  
  if verbose>0:
    print('*** Solving the eBVP')
  eigVal,eigVec= elib.eBVPsolve(bvp,RHSop=Bop,k=NumEigs,which='LM',sigma=sigma,tol=1e-9,maxiter=Th.nq)
  
  assert np.max(np.abs(eigVec.imag))<1e-15, "Eigenfunctions must be real"
  assert np.max(np.abs(eigVal.imag))<1e-15 and np.min(eigVal.real)>0, "Eigenvalues must be real positive"
  eigVal=eigVal.real
  eigVec=eigVec.real
  
  eigVcomp0=elib.eigenvectors_component(bvp,eigVec,0)
  
  if graphics and isModuleFound('fc_simesh_matplotlib'):
    if verbose>0:
      print('*** Plotting eigenfunctions')
    import matplotlib.pyplot as plt
    import fc_simesh_matplotlib.siMesh as siplt
    from fc_tools.matplotlib import set_axes_equal,DisplayFigures, error_colorbar_format
    from fc_vfemp1_eigs.matplotlib import ploteigs
    for i in range(NumEigs):
      eigVcomp0[:,i]=eigVcomp0[:,i]/max(abs(eigVcomp0[:,i]))
    plt.close('all')
    plt.ion()
    for i in range(NumEigs):
      plt.figure()
      siplt.plot(Th,eigVcomp0[:,i],vmin=-1,vmax=1,cmap='viridis')
      if colorbar:
        plt.colorbar()
      siplt.plotiso(Th,eigVcomp0[:,i],isorange=[0],color='LightGray',linewidth=2)
      set_axes_equal()
      plt.axis('off')
      plt.title('$\\lambda^{\\rm num}_{%d}=%.3f$'%(i+1,eigVal[i]))
    DisplayFigures()
    
  return {'bvp':bvp,'Bop':Bop,'eigVal':eigVal,'eigVec':eigVec}
