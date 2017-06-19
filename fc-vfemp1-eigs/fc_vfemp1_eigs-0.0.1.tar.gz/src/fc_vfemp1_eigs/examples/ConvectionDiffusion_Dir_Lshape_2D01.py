import numpy as np
import os

from fc_tools.others import isModuleFound

from fc_oogmsh import gmsh
from fc_simesh.siMesh import siMesh
from fc_vfemp1.operators import Loperator
from fc_vfemp1.BVP import BVP,PDE

from fc_vfemp1_eigs.sys import get_geo
from fc_vfemp1_eigs.lib import eBVPsolve,PrintCopyright,print_separator

def run(**kwargs):
  N=kwargs.get('N',100)
  NumEigs=kwargs.get('k',12)
  sigma=kwargs.get('sigma',0)
  beta=kwargs.get('beta',[3,0])
  graphics=kwargs.get('graphics',True)

  geofile='Lshape'
  (geodir,geofile)=get_geo(2,2,geofile)
  print_separator()
  PrintCopyright()
  print_separator()
  print('      2D Convection-Diffusion eigenvalues BVP ')
  print('         on GMSH mesh from %s.geo\n'%geofile)
  print('               - Laplacian(u) + div(beta u) = lambda*u\n')
  print(' with beta=%s'%str(beta))
  print(' and boundary conditions :')
  print('   * Dirichlet on [1,10,20,21,22,23]')
  print('           u = 0')
  print_separator()

  print('*** Setting the mesh using gmsh and %s file'%geofile)
  meshfile=gmsh.buildmesh2d(geodir+os.sep+geofile+'.geo',N, force=True,verbose=0)
  Th=siMesh(meshfile)
  print('     Mesh sizes : nq=%6d, nme=%7d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
    
  print('*** Setting the eBVP')
  Lop=Loperator(dim=2,A=[[1,None],[None,1]],b=beta)
  pde=PDE(Op=Lop)
  bvp=BVP(Th,pde=pde)
  for lab in Th.sThlab[Th.find(d=1)]:
    bvp.setDirichlet(lab,0.)

  print('*** Solving the eBVP')
  eigVal,eigVec= eBVPsolve(bvp,k=NumEigs,which='LM',sigma=sigma,tol=1e-6,maxiter=Th.nq)

  if graphics and isModuleFound('fc_simesh_matplotlib'):
    print('*** Plotting eigenfunctions')
    import matplotlib.pyplot as plt
    import fc_simesh_matplotlib.siMesh as siplt
    from fc_tools.matplotlib import set_axes_equal,DisplayFigures
    from fc_vfemp1_eigs.matplotlib import ploteigs

    plt.close('all')
    plt.ion()
    ploteigs(Th,eigVal,eigVec,colormap='jet')
    DisplayFigures()
  return {'bvp':bvp,'eigenvalues':eigVal,'eigenvectors':eigVec,'beta':beta}