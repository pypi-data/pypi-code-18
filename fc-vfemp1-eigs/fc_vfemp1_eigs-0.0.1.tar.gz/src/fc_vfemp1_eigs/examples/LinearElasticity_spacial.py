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

# Theory of Vibration, A.A. Shabana
# page 8, TABLE 1.1. Properties of Selected Engineering Materials
# Aluminium
# rho= 2770 kg/m^3 (Material density)
# E = 71 GPa  (Modulus of Elasticity/ module d'Young)
# Modulus of Rididity (G or mu) : 26Gpa
def run(**kwargs):
  N=kwargs.pop('N',20)
  r=kwargs.pop('r',20)# in mm
  R1=kwargs.pop('R1',500)# in mm
  R2=kwargs.pop('R2',100)# in mm
  NumEigs=kwargs.pop('k',9) 
  sigma=kwargs.pop('sigma',0)
  verbose=kwargs.pop('verbose',1)
  graphics=kwargs.pop('graphics',True)
  colorbar=kwargs.pop('colorbar',False)
  nu=kwargs.pop('nu',0.334)    # Poisson's ratio
  E=kwargs.pop('E',71e6)    # Modulus of elasticity in kg/s^2/mm ( GPa=10^9 Pa = 10^6 kg/s^2/mm )
  rho=kwargs.pop('rho',2.770e-6) # Material density in kg/mm^3
  dirlab=kwargs.pop('Dirichlet',[]) # Dirichlet labels
  geofile='spacial'
  (geodir,geofile)=get_geo(3,3,geofile)
  geoFile=geodir+os.sep+geofile+'.geo'
  if verbose>0:
    elib.print_separator()
    elib.PrintCopyright()
    elib.print_separator()
    print('      3D Linear elasticity eigenvalues BVP on \n')
    print('      Mesh generated with gmsh and %s.geo file.\n'%geofile)
    print('               - sigma(U) = lambda*U\n')
    print(" with Young's modulus E=%.3e and Poisson's ratio nu=%g"%(E,nu) )
    print(' and boundary conditions :')
    if len(dirlab)>0:
      print('   * Dirichlet on %s'%str(dirlab))
      print('        U = 0')
      print('   * Free on other boundaries')
    else:
      print('   * Free on all boundaries')
    print('       sigma(U).n =0 ')
    elib.print_separator()
  if verbose==10:
    return
  if verbose>0:
    print('*** Setting the mesh using gmsh and %s.geo file.'%geofile)
  options='-smooth 4 -setnumber R1 %g -setnumber R2 %g -setnumber r %g'%(R1,R2,r)
  meshfile=gmsh.buildmesh3d(geoFile,N, force=True,verbose=3,options=options)
  Th=siMesh(meshfile)
  if verbose>0:
    print('     Mesh sizes : nq=%d, nme=%d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
  if verbose>0:
    print('*** Setting the eBVP')
  mu= E/(2*(1+nu))
  lam = E*nu/((1+nu)*(1-2*nu))  
  Hop=StiffElasHoperator(3,lam,mu)
  pde=PDE(Op=Hop)
  bvp=BVP(Th,pde=pde)
  for lab in dirlab:
    bvp.setDirichlet(lab,[0.,0.,0.]) 
  Bop=Hmass(Th.dim,Th.dim,a0=rho)
  if verbose>0:
    print('*** Solving the eBVP')
  eigVal,eigVec= elib.eBVPsolve(bvp,RHSop=Bop,k=NumEigs,which='LM',sigma=sigma,tol=1e-9,maxiter=Th.nq)
  
 # assert np.max(np.abs(eigVec.imag))<1e-15, "Eigenfunctions must be real"
 # assert np.max(np.abs(eigVal.imag))<1e-15 and np.min(eigVal.real)>=0, "Eigenvalues must be real positive"
  eigVal=eigVal.real
  eigVec=eigVec.real
  
  #print(eigVal)
  freq=np.sqrt(np.abs(eigVal))/(2*np.pi)

  res={'bvp':bvp,'eigVal':eigVal,'eigVec':eigVec,'freq':freq,'N':N,'R1':R1,'R2':R2,'r':r,'E':E,'rho':rho,'nu':nu}
  if graphics and isModuleFound('fc_simesh_mayavi'):
    kwargs['max_displacement']=kwargs.get('max_displacement',(R1+R2+r)/20.) 
    if verbose>0:
      print('*** Plotting eigenfunctions')
    plot(res,**kwargs)
    
  return res

def plot(res,**kwargs):
  from mayavi import mlab
  import fc_simesh_mayavi.siMesh as simlab
  from fc_vfemp1_eigs.mayavi import plot_displacement
  import copy
  bvp=res['bvp'];Th=bvp.Th;
  eigVal=res['eigVal'];eigVec=res['eigVec']
  freq=res['freq'];
  L=np.max(Th.bbox[[1,3,5]]-Th.bbox[[0,2,4]])
  magnitude=kwargs.pop('magnitude',True)
  max_displacement=kwargs.pop('max_displacement',L/20) 
  size=kwargs.pop('size',(640,480))
  size=(size[0],size[1]+49)
  title=kwargs.pop('title',True)
  mlab.close(all=True)
  for i in range(len(eigVal)):
    U=bvp.splitsol(eigVec[:,i])
    mU=np.sqrt(U[0]**2+U[1]**2++U[2]**2)
    for l in range(Th.dim):
      U[l]=max_displacement*U[l]/np.max(mU)
    mlab.figure(size=size)
    if magnitude:
      plot_displacement(Th,U,magnitude=mU,**kwargs)
    else:
      plot_displacement(Th,U,**kwargs)
    #if title:
     # plt.title('freq[%d]=$%.3f$Hz, [max.=%g]'%(i+1,freq[i],max_displacement))
