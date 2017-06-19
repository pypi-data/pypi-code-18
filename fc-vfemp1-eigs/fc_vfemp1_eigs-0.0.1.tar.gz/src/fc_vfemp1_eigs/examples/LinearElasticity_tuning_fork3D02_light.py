from fc_tools.others import isModuleFound
assert isModuleFound('fc_vfemp1_eigs'),'Package fc_vfemp1_eigs must be installed to run this example'

import numpy as np
import os
from fc_oogmsh import gmsh
from fc_simesh.siMesh import siMesh
from fc_vfemp1.operators import Hmass,StiffElasHoperator
from fc_vfemp1.BVP import BVP,PDE
import fc_vfemp1_eigs.lib as elib
from fc_vfemp1_eigs.sys import get_geo

verbose=1

# Geometrical/Mesh properties:
N=75 
L=120 # in mm 
r=10  # in mm
R=40  # in mm
l=100 # in mm
# Material properties:
nu=0.334     # Poisson's ratio
E= 71e6      # Modulus of elasticity in kg/s^2/mm ( GPa=10^9 Pa = 10^6 kg/s^2/mm )
rho=2.770e-6 # Material density in kg/mm^3
# Select Dirichlet boundary:
dirlab=[1] # Dirichlet on Boundary \Gamma_1
# Parameters for eBVPsolve function
NumEigs=9  
sigma=0

max_displacement=r
# Find .geo file
geofile='tuning_fork_02'
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
  print('*** Setting the mesh using gmsh and %s.geo file.'%geofile)
options='-smooth 4 -setnumber L %g -setnumber l %g -setnumber r %g -setnumber R %g'%(L,l,r,R)
meshfile=gmsh.buildmesh3d(geoFile,N, force=True,verbose=3,options=options)
Th=siMesh(meshfile)
if verbose>0:
  print('     Mesh sizes : nq=%d, nme=%d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
  print('*** Setting the eBVP')
# Setting the eBVP
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
# Solving the eBVP
eigVal,eigVec= elib.eBVPsolve(bvp,RHSop=Bop,k=NumEigs,which='LM',sigma=sigma, tol=1e-9,maxiter=Th.nq)
  
assert np.max(np.abs(eigVec.imag))<1e-15, "Eigenfunctions must be real"
assert np.max(np.abs(eigVal.imag))<1e-15 and np.min(eigVal.real)>=0, "Eigenvalues must be real positive"
eigVal=eigVal.real
eigVec=eigVec.real
  
freq=np.sqrt(np.abs(eigVal))/(2*np.pi)

if isModuleFound('fc_simesh_mayavi'):
  if verbose>0:
    print('*** Plotting eigenfunctions')
  from mayavi import mlab
  import fc_simesh_mayavi.siMesh as simlab
  from fc_vfemp1_eigs.mayavi import plot_displacement
  mlab.close(all=True)
  for i in range(len(eigVal)):
    U=bvp.splitsol(eigVec[:,i])
    mU=np.sqrt(U[0]**2+U[1]**2+U[2]**2)
    for l in range(Th.dim):
      U[l]=max_displacement*U[l]/np.max(mU)
    mlab.figure()
    plot_displacement(Th,U,magnitude=mU,colormap='jet')
