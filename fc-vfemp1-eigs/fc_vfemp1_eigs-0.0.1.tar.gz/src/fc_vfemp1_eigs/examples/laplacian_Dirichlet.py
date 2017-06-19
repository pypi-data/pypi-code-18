import numpy as np
import os

from fc_tools.others import isModuleFound

from fc_oogmsh import gmsh
from fc_vfemp1_eigs.sys import get_geo
from fc_simesh.siMesh import siMesh
from fc_vfemp1.operators import Loperator,Lstiff
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
  'geofile' : string ('disk4bounds' by default)
      specify the name of the .geo file used by gmsh
  `k` : integer (6 by default)
      The number of eigenvalues and eigenvectors desired.
  `sigma` : real or complex (0 by default)    
      Find eigenvalues near sigma using shift-invert mode.
      see help of the function scipy.sparse.linalg.eigs
  `graphics` : boolean  
      The coordinates of mesh nodes.
  `verbose` : integer (1 by default)
      No verbosity for 0 value. With `verbose=10` only print the BVP.
  """
  N=kwargs.get('N',20)
  NumEigs=kwargs.get('k',6)
  d=kwargs.get('d',2) # d=2 (2D mesh), 3 (3D mesh) or 2.5 (3D surface mesh)
  sigma=kwargs.get('sigma',0)
  verbose=kwargs.pop('verbose',1)
  graphics=kwargs.get('graphics',True)
  colorbar=kwargs.get('colorbar',False)
  colormap=kwargs.get('colormap','viridis')
  isocolor=kwargs.get('isocolor','LightGray')
  graphics=kwargs.get('graphics',True)
  geofile=kwargs.get('geofile','disk4bounds')
  
  if d==2:
    (geodir,geofile)=get_geo(2,2,geofile)
  if d==3:
    (geodir,geofile)=get_geo(3,3,geofile)  
  if d==2.5:
    (geodir,geofile)=get_geo(3,2,geofile)    
  geoFile=geodir+os.sep+geofile+'.geo'
  if verbose>0:
    elib.print_separator()
    elib.PrintCopyright()
    elib.print_separator()
    print(' Dirichlet eigenvalue problem for the Laplacian on unit disk')
    print('  Mesh generated with gmsh and %s.geo file.\n'%geofile)
    print('               -Laplacian(u) = lambda*u\n')
    print(' and Dirichlet boundary conditions :')
    print('   * u=0 on all boundaries')
    elib.print_separator()
  if verbose==10:
    return
  if verbose>0:
    print('*** Setting the mesh using gmsh and %s.geo file.'%geofile)
  meshfile=gmsh.buildmesh(d,geoFile,N, force=True,verbose=0)
  Th=siMesh(meshfile)
  if verbose>0:
    print('     Mesh sizes : nq=%d, nme=%d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
  if verbose>0:
    print('*** Setting the eBVP')
  Lop=Lstiff(Th.dim)
  pde=PDE(Op=Lop)
  bvp=BVP(Th,pde=pde)
  Dirichlet=kwargs.pop('Dirichlet',Th.sThlab[Th.find(Th.d-1)])
  
  for lab in Dirichlet:
    bvp.setDirichlet(lab,0.)
  if verbose>0:
    print('*** Solving the eBVP')
  eigVals,eigVecs= elib.eBVPsolve(bvp,k=NumEigs,which='LM', sigma=sigma,tol=1e-6,maxiter=Th.nq)
  
  assert np.max(np.abs(eigVecs.imag))<1e-15, "Eigenfunctions must be real, found %g"%np.max(np.abs(eigVecs.imag))
  assert np.max(np.abs(eigVals.imag))<1e-15 and np.min(eigVals.real)>0, "Eigenvalues must be real positive"
  eigVals=eigVals.real
  eigVecs=eigVecs.real
  
  elib.eigenvectors_scale(eigVecs)
  
  if graphics and isModuleFound('fc_simesh_matplotlib') and Th.dim==2:
    if verbose>0:
      print('*** Plotting eigenfunctions')
    import matplotlib.pyplot as plt
    import fc_simesh_matplotlib.siMesh as siplt
    from fc_tools.matplotlib import set_axes_equal,DisplayFigures
    plt.close('all')
    plt.ion()
    for i in range(NumEigs):
      plt.figure()
      siplt.plot(Th,eigVecs[:,i],colormap=colormap)
      if colorbar:
        plt.colorbar()
      siplt.plotiso(Th,eigVecs[:,i],isorange=[0],color=isocolor,linewidth=2)
      set_axes_equal()
      plt.axis('off')
      plt.title('$\\lambda^{\\rm num}_{%d}=%.3f$'%(i+1,eigVals[i]))
    DisplayFigures()
    
  if graphics and isModuleFound('fc_simesh_mayavi') and Th.dim==3:
    if verbose>0:
      print('*** Plotting eigenfunctions')
    from mayavi import mlab
    import fc_simesh_mayavi.siMesh as simlab
    from fc_tools.mayavi import mlab_latex3D
    mlab.close(all=True)
    contours=[-0.75,-0.5,-0.25,0.25,0.5,0.75]
    for i in range(NumEigs):
      mlab.figure()
      if Th.d==2:
        simlab.plot(Th,eigVecs[:,i],colormap=colormap)
        if colorbar:
          mlab.colorbar(title='eigen %d : %.3f'%(i+1,eigVals[i]))
        simlab.plotiso(Th,eigVecs[:,i],contours=[0],color=isocolor,line_width=2)
      if Th.d==3:
        simlab.plot(Th,eigVecs[:,i],colormap=colormap,opacity=0.03)
        if colorbar:
          mlab.colorbar()
        simlab.slice(Th,eigVecs[:,i],origin=[0,0,0],normal=[0,0,1],colormap=colormap)
        simlab.sliceiso(Th,eigVecs[:,i],contours=contours,origin=[0,0,0],normal=[0,0,1],color='LightGray',opacity=0.5)
        simlab.sliceiso(Th,eigVecs[:,i],contours=[0],origin=[0,0,0],normal=[0,0,1],color='white',line_width=2)
        simlab.slice(Th,eigVecs[:,i],origin=[0,0,0],normal=[0,1,0],colormap=colormap)
        simlab.sliceiso(Th,eigVecs[:,i],contours=contours,origin=[0,0,0],normal=[0,1,0],color='LightGray',opacity=0.5)
        simlab.sliceiso(Th,eigVecs[:,i],contours=[0],origin=[0,0,0],normal=[0,1,0],color='white',line_width=2)
        simlab.slice(Th,eigVecs[:,i],origin=[0,0,0],normal=[1,0,0],colormap=colormap)
        simlab.sliceiso(Th,eigVecs[:,i],contours=contours,origin=[0,0,0],normal=[1,0,0],color='LightGray',opacity=0.5)
        simlab.sliceiso(Th,eigVecs[:,i],contours=[0],origin=[0,0,0],normal=[1,0,0],color='white',line_width=2)
        #simlab.iso_surface(Th,eigVecs[:,i],contours=[0],color=isocolor,opacity=0.1)
      #mlab_latex3D('$\\lambda^{\\rm num}_{%d}=%.3f$'%(i+1,eigVals[i]))
    
  return {'bvp':bvp,'eigVal':eigVals,'eigVec':eigVecs}
