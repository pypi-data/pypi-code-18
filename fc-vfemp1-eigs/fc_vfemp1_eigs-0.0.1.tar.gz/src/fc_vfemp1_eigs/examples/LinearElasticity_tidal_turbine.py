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

# https://www.mathworks.com/examples/matlab/community/21097-vibration-of-a-turning-fork
# Theory of Vibration, A.A. Shabana
# page 8, TABLE 1.1. Properties of Selected Engineering Materials
# Aluminium
# rho= 2770 kg/m^3 (Material density)
# E = 71 GPa  (Modulus of Elasticity/ module d'Young)
# Modulus of Rididity (G or mu) : 26Gpa
def run(**kwargs):
  N=kwargs.get('N',2)
  NumEigs=kwargs.get('k',6) 
  sigma=kwargs.get('sigma',0)
  verbose=kwargs.pop('verbose',1)
  graphics=kwargs.get('graphics',True)
  colorbar=kwargs.get('colorbar',False)
  nu=kwargs.get('nu',0.334)    # Poisson's ratio
  E=kwargs.get('E',71e9)    # Modulus of elasticity in kg/s^2/m ( GPa=10^9 Pa = 10^6 kg/s^2/mm =10^9 kg/s^2/m )
  rho=kwargs.get('rho',2770) # Material density in kg/m^3
  L=kwargs.get('L',5) # to set caracteristic length to L meters
 
  geofile='tidal_turbine.geo'
  (geodir,geofile)=get_geo(3,3,geofile)
  geoFile=geodir+os.sep+geofile+'.geo'
  if verbose>0:
    elib.print_separator()
    elib.PrintCopyright()
    elib.print_separator()
    print(' 3D Linear elasticity eigenvalues BVP on')
    print(' mesh generated with gmsh and %s.geo file.\n'%geofile)
    print('               - sigma(U) = rho*lambda*U\n')
    print(" with Young's modulus E=%.3e GPa, Poisson's ratio nu=%g"%(E,nu) )
    print("      material density rho=%.3e kg/m^3"%rho)
    print(' Boundary conditions are:')
    print('   * Dirichlet on [1]')
    print('       U = 0')
    print('   * Free on [2]')
    print('       sigma(U).n =0 ')
    elib.print_separator()
  if verbose==10:
    return
  if verbose>0:
    print('*** Setting the mesh using gmsh and %s.geo file.'%geofile)
  meshfile=gmsh.buildmesh3d(geoFile,N, force=True,verbose=0,options='-smooth 4')
  trans=lambda q: L/471.41742430*q # to set caracteristic length to L meters
  Th=siMesh(meshfile,trans=trans)
  if verbose>0:
    print('     Mesh sizes : nq=%d, nme=%d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
  if verbose>0:
    print('*** Setting the eBVP')
  mu= E/(2*(1+nu))
  lam = E*nu/((1+nu)*(1-2*nu))  
  Hop=StiffElasHoperator(3,lam,mu)
  pde=PDE(Op=Hop)
  bvp=BVP(Th,pde=pde)
  bvp.setDirichlet(1,[0.,0.,0.]) 
  Bop=Hmass(Th.dim,Th.dim,a0=rho)
  if verbose>0:
    print('*** Solving the eBVP')
  eigVal,eigVec= elib.eBVPsolve(bvp,RHSop=Bop,k=NumEigs,which='LM',sigma=sigma,tol=1e-9,maxiter=Th.nq)
  
  #assert np.max(np.abs(eigVec.imag))<1e-15, "Eigenfunctions must be real"
  #assert np.max(np.abs(eigVal.imag))<1e-15 and np.min(eigVal.real)>0, "Eigenvalues must be real positive"
  eigVal=eigVal.real
  eigVec=eigVec.real
  
  freq=np.sqrt(np.abs(eigVal))/(2*np.pi)
#  print(freq)
  
  res={'bvp':bvp,'eigVal':eigVal,'eigVec':eigVec,'freq':freq}
  res={'bvp':bvp,'eigVal':eigVal,'eigVec':eigVec,'freq':freq,'N':N,'L':L,'E':E,'rho':rho,'nu':nu}
  #if graphics and isModuleFound('fc_simesh_matplotlib'):
    #if verbose>0:
      #print('*** Plotting eigenfunctions')
    #plot(res,**kwargs)
    
  if graphics and isModuleFound('fc_simesh_mayavi'):
    if verbose>0:
      print('*** Plotting eigenfunctions')
    plot_mayavi(res,**kwargs)
    
  return res

def plot(res,**kwargs):
  import matplotlib.pyplot as plt
  import fc_simesh_matplotlib.siMesh as siplt
  from fc_tools.matplotlib import set_axes_equal,DisplayFigures, error_colorbar_format
  import copy
  scale=kwargs.get('scale',20)
  bvp=res['bvp'];Th=bvp.Th;
  eigVal=res['eigVal'];eigVec=res['eigVec']
  plt.close('all')
  plt.ion()
  for i in range(len(eigVal)):
    U=bvp.splitsol(scale*eigVec[:,i])
    Thm=copy.deepcopy(Th)
    Thm.move(U)
    plt.figure()
    siplt.plot(Thm,np.sqrt(U[0]**2+U[1]**2+U[2]**2),d=2,cmap='jet')
    #plt.colorbar()
    #siplt.plotmesh(Thm,d=1,color='black')
    set_axes_equal()
    plt.axis('off')
    plt.title('$\\lambda^{\\rm num}_{%d}=%.3f$, [scale=%g]'%(i+1,eigVal[i],scale))
  DisplayFigures()
  
def plot_mayavi(res,**kwargs):
  from mayavi import mlab
  import fc_simesh_mayavi.siMesh as simlab
  import copy
  bvp=res['bvp'];Th=bvp.Th;
  eigVal=res['eigVal'];eigVec=res['eigVec']
  L=np.max(Th.bbox[[1,3,5]]-Th.bbox[[0,2,4]])
  max_displacement=kwargs.get('max_displacement',L/20.) # in meter
  mlab.close(all=True) 
  for i in range(len(eigVal)):
    U=bvp.splitsol(eigVec[:,i])
    mU=np.sqrt(U[0]**2+U[1]**2+U[2]**2)
    for i in range(3):
      U[i]=max_displacement*U[i]/np.max(mU)
    Thm=copy.deepcopy(Th)
    Thm.move(U)
    mlab.figure()
    mU=np.sqrt(U[0]**2+U[1]**2+U[2]**2)
    simlab.plot(Thm,mU,d=2,colormap='jet')
    simlab.plotiso(Thm,mU,d=2,color='white',line_width=2)
    
    
# plot_mayavi_video(res,0,magnification=6,Nf=50,filebase='videos/tidal_turbine_mod0')
def plot_mayavi_video(res,i,**kwargs):
  from mayavi import mlab
  from fc_vfemp1_eigs.mayavi import sequence_images
  import fc_simesh_mayavi.siMesh as simlab
  from fc_tools.mayavi import mlab_latex3D
  import copy
  bvp=res['bvp'];Th=bvp.Th;
  eigVal=res['eigVal'];eigVec=res['eigVec']
  L=np.max(Th.bbox[[1,3,5]]-Th.bbox[[0,2,4]])
  filebase=kwargs.get('filebase','test')
  max_displacement=kwargs.get('max_displacement',L/20.) # in meter
  magnification=kwargs.get('magnification',3) # in meter
  Nf=kwargs.get('Nf',25)
  U=bvp.splitsol(eigVec[:,i])
  mU=np.sqrt(U[0]**2+U[1]**2+U[2]**2)
  for l in range(3):
    U[l]=max_displacement*U[l]/np.max(mU)
  mlab.close(all=True)
  t=np.linspace(0,2*np.pi,Nf)
  V=3*[None]
  for k in range(Nf):
    st=np.sin(t[k])
    for l in range(3):
      V[l]=st*U[l]
    Thm=copy.deepcopy(Th)
    Thm.move(V)
    mlab.figure()
    mU=np.sqrt(U[0]**2+U[1]**2+U[2]**2)
    simlab.plot(Thm,mU,d=2,colormap='jet')
    simlab.plotiso(Thm,mU,d=2,color='white',line_width=2)
    mlab.view(azimuth=0, elevation=180, distance=98, focalpoint=[ 22.67,0.,-5.])
    print(mlab.view())
    File='%s_%5d.png'%(filebase,k+1)
    File=File.replace(' ','0')
    print('save figure in %s'%File)
    #mlab_latex3D('%d'%k,heigth=10,center=(0,20,0))
    mlab.savefig(File,magnification=magnification)



def plot_mayavi_video(res,**kwargs):
  from fc_vfemp1_eigs.mayavi import sequence_images
  bvp=res['bvp'];Th=bvp.Th;
  eigVal=res['eigVal'];eigVec=res['eigVec']
  k=len(eigVal)
  for i in range(k):
    sequence_images(Th,eigVal[i],eigVec[:,i],**kwargs)
