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

  geofile='disk5holes'
  (geodir,geofile)=get_geo(2,2,geofile)
  print_separator()
  PrintCopyright()
  print_separator()
  print('      2D Laplacian eigenvalues BVP ')
  print('         on GMSH mesh from %s.geo\n'%geofile)
  print('               - Laplacian(u) = lambda*u\n')
  print(' and boundary conditions :')
  print('   * Dirichlet on [1,10]')
  print('                  u = 0')
  print('   * Neumann on [20,21]')
  print('              du/dn = 0')
  print('   * Robin on [22,23]')
  print('       du/dn + 10*u = 0')
  print_separator()

  print('*** Setting the mesh using gmsh and %s file'%geofile)
  meshfile=gmsh.buildmesh2d(geodir+os.sep+geofile+'.geo',N, force=True,verbose=0)
  Th=siMesh(meshfile)
  print('     Mesh sizes : nq=%6d, nme=%7d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
    
  print('*** Setting the eBVP')
  Lop=Loperator(dim=2,A=[[1,None],[None,1]])
  pde=PDE(Op=Lop)
  bvp=BVP(Th,pde=pde)
  bvp.setDirichlet(1,0.)
  bvp.setDirichlet(10,0.)
  bvp.setRobin(20,0.)
  bvp.setRobin(21,0.)
  bvp.setRobin(22,0.,ar=10)
  bvp.setRobin(23,0.,ar=10)

  print('*** Solving the eBVP')
  eigVal,eigVec= eBVPsolve(bvp,k=NumEigs,which='LM',sigma=sigma,tol=1e-6,maxiter=Th.nq)

  if isModuleFound('fc_simesh_matplotlib'):
    print('*** Plotting eigenfunctions')
    import matplotlib.pyplot as plt
    import fc_simesh_matplotlib.siMesh as siplt
    from fc_tools.matplotlib import set_axes_equal,DisplayFigures
    from fc_vfemp1_eigs.matplotlib import ploteigs

    plt.close('all')
    plt.ion()
    ploteigs(Th,eigVal,eigVec,colormap='jet')
    DisplayFigures()
  return {'bvp':bvp,'eigenvalues':eigVal,'eigenvectors':eigVec}