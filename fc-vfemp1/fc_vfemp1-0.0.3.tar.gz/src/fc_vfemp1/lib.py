import numpy as np
from scipy.sparse import linalg
from fc_tools.others import isModuleFound
from fc_simesh.siMesh import siMesh,HyperCube
from fc_vfemp1.operators import Loperator,Lmass,Hoperator,Hmass,Lstiff
from fc_vfemp1.FEM import NormL2,NormH1,AssemblyP1
from fc_vfemp1.BVP import BVP,PDE,Assembly_Dirichlet_pt

def print_separator():
  print('---------------------------------------------------------------')
  
def PrintCopyright():
  print('Solving Boundary Value Problems (BVP\'s) with')
  print('          fc_vfemp1 package')
  print('Copyright (C) 2017 Cuvelier F.')
  print('  (LAGA/CNRS/Paris 13 University)')

def relative_errors(Th,Uex,U):
  Mass=AssemblyP1(Th,Lmass(dim=Th.dim))
  Stiff=AssemblyP1(Th,Lstiff(dim=Th.dim))
  errInf=np.max(np.abs(U-Uex))/(1+np.max(np.abs(Uex)))
  errL2=NormL2(Th,U-Uex,Mass=Mass)/(1+NormL2(Th,Uex,Mass=Mass))
  errH1=NormH1(Th,U-Uex,Mass=Mass,Stiff=Stiff)/(1+NormH1(Th,Uex,Mass=Mass,Stiff=Stiff))
  return (errL2,errH1,errInf)

def generic_order(run,**kwargs):
  """
  Returns a dictionary containing ....
     
  Parameters
  ----------
  `run` : a function solving a BVP for a given mesh size (set with `N`) and 
          returning informations (dict) 
       
  Optional (key/value) parameters
  -------------------------------
  `LN` : array or list of integers
      mesh size grows with `N in LN`.
      
  Others options are those of the `solve` function of class `BVP`:
  `solver` : to specify a solver for the sparse system.
      Default is `solver=lambda A,b: scipy.sparse.linalg.spsolve(A,b)`
      
  `perm`   : to specify permutation in the sparse matrix. For example
      `perm=lambda A: scipy.sparse.csgraph.reverse_cuthill_mckee(A)`
  """
  LN=kwargs.pop('LN',[25,50,100,150])
  #sol=kwargs.pop('sol','sin(x)*sin(y)')
  debug=kwargs.pop('debug',0)
  res=run(verbose=10,graphics=False,**kwargs)
  nLn=len(LN)
  Lh=np.zeros((nLn,))
  Lnq=np.zeros((nLn,))
  Lnme=np.zeros((nLn,))
  Lu_errL2=np.zeros((nLn,))
  Lu_errInf=np.zeros((nLn,))
  Lu_errH1=np.zeros((nLn,))
  i=0
  for N in LN:
    print('[%2d/%2d] N=%d'%(i+1,len(LN),N))
    res=run(N=N,graphics=False,verbose=debug,**kwargs)
    Th=res['bvp'].Th
    uex=res['uex'];U=res['U'];
    Uex=Th.feval(uex)
    (errL2,errH1,errInf)=relative_errors(Th,Uex,U)
    print('   Mesh sizes : nq=%6d, nme=%7d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
    Lh[i]=Th.get_h()
    Lnq[i]=Th.nq
    Lnme[i]=Th.get_nme()
    Lu_errL2[i]=errL2
    Lu_errInf[i]=errInf
    Lu_errH1[i]=errH1
    print('   ndof=%d - Error : uH1=%.2e, uL2=%.2e, uInf=%.2e'
      %(2*Lnq[i], Lu_errH1[i],Lu_errL2[i],Lu_errInf[i]))
    i+=1
    
  return {'LN':LN,'Lnq':Lnq,'Lnme':Lnme,'Lh':Lh,
          'Lu_errL2':Lu_errL2,'Lu_errH1':Lu_errH1,'Lu_errInf':Lu_errInf}

def order(run,**kwargs):
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
  res_order=generic_order(run,**kwargs)
  if graphics and isModuleFound('fc_simesh_matplotlib'):
    import matplotlib.pyplot as plt
    from fc_tools.matplotlib import DisplayFigures
    from fc_vfemp1.matplotlib import plot_order
    plt.close('all')
    plt.ion()
    plt.figure()
    plot_order(res_order)  