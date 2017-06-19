import numpy as np
from fc_simesh.siMesh import siMesh,HyperCube
from fc_vfemp1.operators import Loperator,Lmass,Hoperator,Hmass,Lstiff
from fc_vfemp1.FEM import NormL2,NormH1,AssemblyP1
from fc_vfemp1.BVP import BVP,PDE,Assembly_Dirichlet_pt
from scipy.sparse import linalg

def print_separator():
  print('---------------------------------------------------------------')
  
def PrintCopyright():
  print('Solving Eigenvalue Boundary Value Problems (eBVP\'s) with')
  print('          fc_vfemp1_eigs package')
  print('Copyright (C) 2017 Cuvelier F.')
  print('  (LAGA/CNRS/University of Paris XIII)')

def LaplacianDDDDEigenOnRectangle(Th,L,H,nb):
  Feigenvalue=lambda k,l: (k*np.pi/L)**2 + (l*np.pi/H)**2
  Feigenfunction=lambda k,l,x,y: np.sin((k*np.pi/L)*x)*np.sin((l*np.pi/H)*y)
  Nl=nb;Nk=nb
  EigVal=np.zeros((Nl*Nk,))
  indx=np.zeros((2,Nl*Nk))
  i=0
  for k in range(1,Nk+1):
    for l in range(1,Nl+1):
      indx[0,i]=k
      indx[1,i]=l
      EigVal[i]=Feigenvalue(k,l)
      i=i+1
  I=np.argsort(EigVal)
  EigVal=EigVal[I[:nb]]
  indx=indx[:,I[:nb]]
  EigVec=np.zeros((Th.nq,nb))
  for i in range(nb):
    EigVec[:,i]=Th.eval(lambda x,y: Feigenfunction(indx[0,i],indx[1,i],x,y))
  return EigVal,EigVec

def LaplacianNNNNEigenOnRectangle(Th,L,H,nb,**kwargs):
  nonzero=kwargs.get('nonzero',False)
  Feigenvalue=lambda k,l: (k*np.pi/L)**2 + (l*np.pi/H)**2
  Feigenfunction=lambda k,l,x,y: np.cos((k*np.pi/L)*x)*np.cos((l*np.pi/H)*y)
  Nl=nb;Nk=nb
  EigVal=np.zeros((Nl*Nk,))
  indx=np.zeros((2,Nl*Nk))
  i=0
  for k in range(Nk):
    for l in range(Nl):
      indx[0,i]=k
      indx[1,i]=l
      EigVal[i]=Feigenvalue(k,l)
      i=i+1
  if nonzero:
    I=np.where(EigVal>1e-8)[0]
    EigVal=EigVal[I]
    indx=indx[:,I]
  I=np.argsort(EigVal)
  EigVal=EigVal[I[:nb]]
  indx=indx[:,I[:nb]]
  EigVec=np.zeros((Th.nq,nb))
  for i in range(nb):
    EigVec[:,i]=Th.eval(lambda x,y: Feigenfunction(indx[0,i],indx[1,i],x,y))
  return EigVal,EigVec

def BiharmonicSSPEigenOnRectangle(Th,L,H,nb):
  EigVal,EigVec=LaplacianDDDDEigenOnRectangle(Th,L,H,nb)
  return EigVal**2,EigVec

def BiharmonicCHEigenOnRectangle(Th,L,H,nb):
  EigVal,EigVec=LaplacianNNNNEigenOnRectangle(Th,L,H,nb)
  return EigVal**2,EigVec

def eBVPsolve(bvp,**kwargs):
  condition=kwargs.pop('condition',bvp.m*[False])
  RHSop=kwargs.pop('RHSop',None)
  # perm=lambda A: scipy.sparse.csgraph.reverse_cuthill_mckee(A)
  perm=kwargs.pop('perm', None)
  if RHSop is None:
    if bvp.m==1:
      RHSop=Lmass(bvp.dim)
    else:
      RHSop=Hmass(bvp.dim,bvp.m)
  ID,IDc,gD=Assembly_Dirichlet_pt(bvp)
  A,b=bvp.Assembly(Dirichlet=False)
  bvpRHS=BVP(bvp.Th,pde=PDE(Op=RHSop))
  B,f=bvpRHS.Assembly()
  A,B=space_condition_pre(bvp,A,B,condition)
  
  A=(A[IDc])[::,IDc]
  B=(B[IDc])[::,IDc]
  if perm is not None:
    p=perm(A)
    A=A[p,::][::,p]
    B=B[p,::][::,p]
  eigenvalues,eigenvectors=linalg.eigs(A,M=B,**kwargs)
  if perm is not None:
    eigenvectors[p]=eigenvectors

  I=np.argsort(eigenvalues)
  eigenvalues=eigenvalues[I]
  eigenvectors=eigenvectors[:,I]
  eigVec=np.zeros((bvp.ndof,len(I)),dtype=eigenvectors.dtype)
  eigVec[IDc]=eigenvectors
  #if np.max(abs(eigenvectors.imag))<1e-14:
    #eigVec=np.zeros(eigenvectors.shape)
    #eigVec=eigenvectors.real
  return eigenvalues,eigVec

def errors(Th,numEigsVal,numEigsVec,exEigsVal,exEigsVec,**kwargs):
  assert numEigsVec.shape == exEigsVec.shape
  assert numEigsVal.shape == exEigsVal.shape
  assert Th.nq==numEigsVec.shape[0],' nq=%d and numEigsVec.shape[0]=%d'%(Th.nq,numEigsVec.shape[0])
  assert numEigsVal.shape[0]== numEigsVec.shape[1]
  ne=numEigsVal.shape[0]
  #numEigsVec=scaleEigensVec(Th,exEigsVec,numEigsVec)
  Mass=AssemblyP1(Th,Lmass(Th.dim))
  Stiff=AssemblyP1(Th,Lstiff(Th.dim))
  eVecL2=np.zeros((ne,))
  eVecH1=np.zeros((ne,))
  eVal=np.zeros((ne,))
  for i in range(ne):
    err=exEigsVec[:,i]-numEigsVec[:,i]
    eVecL2[i]=NormL2(Th,err,Mass=Mass)/NormL2(Th,exEigsVec[:,i],Mass=Mass)
    eVecH1[i]=NormH1(Th,err,Mass=Mass,Stiff=Stiff)/NormH1(Th,exEigsVec[:,i],Mass=Mass,Stiff=Stiff)
    eVal[i]=abs(exEigsVal[i]-numEigsVal[i])
    if abs(exEigsVal[i])>1:
      eVal[i]/=abs(exEigsVal[i]) 
  return eVecL2,eVecH1,eVal

def generic_orders(run,**kwargs):
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
  """
  LN=kwargs.pop('LN',[25,50,100,150])
  debug=kwargs.pop('debug',0)
  run(verbose=10,graphics=False,**kwargs)
  NumEigs=kwargs.pop('k',6)
  nLN=len(LN)
  iN=0
  Lu_errL2=np.zeros((nLN,NumEigs))
  Lu_errH1=np.zeros((nLN,NumEigs))
  L_eVal=np.zeros((nLN,NumEigs))

  nLn=len(LN)
  Lh=np.zeros((nLn,))
  Lnq=np.zeros((nLn,))
  Lnme=np.zeros((nLn,))
  i=0
  for N in LN:
    res=run(N=N,k=NumEigs,verbose=0,graphics=False,**kwargs)
    Th=res['bvp'].Th
    print('   Mesh sizes : nq=%6d, nme=%7d, h=%.3e'%(Th.nq,Th.get_nme(),Th.get_h()))
    Lu_errL2[i]=res['eVecL2']
    Lu_errH1[i]=res['eVecH1']
    L_eVal[i]=res['eVal']
    print('     -> u Err. L2=%.4e, H1=%.4e'%(np.max(Lu_errL2[i]),np.max(Lu_errH1[i])))
    Lh[i]=Th.get_h()
    Lnq[i]=Th.nq
    Lnme[i]=Th.get_nme()
    i+=1
  return {'LN':LN,'Lnq':Lnq,'Lnme':Lnme,'Lh':Lh,
          'Lu_errL2':Lu_errL2,'Lu_errH1':Lu_errH1,'L_eVal':L_eVal}

def spliteigs(bvp,eigVecs):
  NumEigs=eigVecs.shape[1]
  eigV=NumEigs*[None]
  for i in range(NumEigs):
    eigV[i]=bvp.splitsol(eigVecs[:,i])
  return eigV

def eigenvectors_modulus(bvp,eigVecs):
  eigV=spliteigs(bvp,eigVecs)
  NumEigs=eigVecs.shape[1]
  eigVmod=np.zeros((bvp.Th.nq,NumEigs))
  for i in range(NumEigs):
    for j in range(bvp.m):
      eigVmod[:,i]+=np.abs(eigV[i][j])**2
  return np.sqrt(eigVmod)

def eigenvectors_component(bvp,eigVecs,comp):
  assert (comp>= 0) and (comp<bvp.m)
  eigV=spliteigs(bvp,eigVecs)
  NumEigs=eigVecs.shape[1]
  eigVcomp=np.zeros((bvp.Th.nq,NumEigs),dtype=eigVecs.dtype)
  for i in range(NumEigs):
    eigVcomp[:,i]=eigV[i][comp]
  return eigVcomp

def eigenvector_scale(eigVec):
  return eigVec/np.max(np.abs(eigVec))

def eigenvectors_scale(eigVecs):
  NumEigs=eigVecs.shape[1]
  for i in range(NumEigs):
    eigVecs[:,i]=eigenvector_scale(eigVecs[:,i])

def linear_combination(U,V):
  """ Find 
      Let N>=n, {u_1,...,u_n} be n orthogonal vectors in K^N (N>=n) 
      and {v_1,...,v_n} be n orthogonal vectors in K^N (N>=n).
      This fonction computes the n-by-n matrix A such that
        u_i = A_{i,1}v_1 + ... + A_{i,n}v_n for all i in {1,...,n}
      U is a numpy  
  """
  assert U.shape==V.shape
  return np.dot(U.T,V)

def trans_old(Uex,U):
  A=linear_combination(U,Uex)
  return np.dot(U,A.T)

def complete_trans(eigVals,eigVec,eigVecEx):
  normalize(eigVec)
  eigVecTrans=np.zeros(eigVec.shape,dtype=eigVec.dtype)
  u, indices = np.unique(eigVals, return_inverse=True)
  for i in np.unique(indices):
    J=np.where(indices==i)[0]
    eigVecTrans[:,J]=trans(eigVecEx[:,J],eigVec[:,J])
  return eigVecTrans

def trans(Uex,U):
  Us=np.zeros(U.shape)
  PS=lambda i,j: np.dot(U[:,j].T,Uex[:,i])
  for i in range(U.shape[1]):
    for j in range(U.shape[1]):
      Us[:,i]+=PS(i,j)*U[:,j]
  return Us

def normalize(U):
  for i in range(U.shape[1]):
    U[:,i]=U[:,i]/np.sqrt(np.dot(U[:,i].T,U[:,i]))

def complete_trans_old(eigVals,eigVec,eigVecEx):
  normalize(eigVec)
  eigVecTrans=np.zeros(eigVec.shape,dtype=eigVec.dtype)
  u, indices = np.unique(eigVals, return_inverse=True)
  for i in np.unique(indices):
    J=np.where(indices==i)[0]
    eigVecTrans[:,J]=trans(eigVecEx[:,J],eigVec[:,J])
  for i in range(len(eigVals)):
    eigVecTrans[:,i]=eigVecTrans[:,i]/max(abs(eigVecTrans[:,i]))  
  
  return eigVecTrans


def space_condition_pre(bvp,A,B,condition):
  from fc_vfemp1.sparse import csr_one_rows,csr_zero_rows
  from fc_vfemp1.FEMtools import getVFindices
  VFInd=getVFindices(1,bvp.m,bvp.Th.nq)
  for i in range(bvp.m):
    if condition[i]:
      row=VFInd(0,i)
      csr_one_rows(A,row) 
      csr_one_rows(B,row)
      #B[row,row]=1
  return A,B

def L2_normalize(U,Mass):
  for i in range(U.shape[1]):
    U[:,i]=U[:,i]/np.sqrt(np.dot(U[:,i].T,Mass*U[:,i]))

def L2_trans(Uex,U,Mass):
  Us=np.zeros(U.shape)
  PS=lambda i,j: np.dot(U[:,j].T,Mass*Uex[:,i])
  for i in range(U.shape[1]):
    for j in range(U.shape[1]):
      Us[:,i]+=PS(i,j)*U[:,j] # Us[:,j] is a linear combination of vector U[:,0], U[:,1], ... 
  return Us

def L2_complete_trans(Th,eigValEx,eigVec,eigVecEx):
  eigVecTrans=np.zeros(eigVec.shape,dtype=eigVec.dtype)
  u, indices = np.unique(eigValEx, return_inverse=True)
  NumEigs=eigVec.shape[1]
  Mass=AssemblyP1(Th,Lmass(Th.dim))
  L2_normalize(eigVec,Mass)
  u, indices = np.unique(eigValEx, return_inverse=True)
  for i in np.unique(indices):
    J=np.where(indices==i)[0]
    eigVecTrans[:,J]=L2_trans(eigVecEx[:,J],eigVec[:,J],Mass)
  return eigVecTrans

def aligned_eigenvectors(Th,V1,V2,**kwargs):
  labels=kwargs.pop('labels',[100,101,102,103])
  tol=kwargs.pop('tol',1e-6)
  aVecs=[]
  for lab in labels:
    idx=Th.find(1,labels=lab)
    sTh=Th.sTh[idx]
    # minimization of \int_sTh |V|^2 dq
    #   where V=a1*V1+(1-a1)*V2
    # \int_sTh |V|^2 dq ~= <M*V,V>
    # We have
    #   <M*V,V>=a1^2*<M*V1,V1>+...
    M=AssemblyP1(sTh,Lmass(2))
    PS=lambda U,V: np.dot(V.T,M*U)
    B11=PS(V1,V1)
    B12=PS(V1,V2)
    B22=PS(V2,V2)
    a=B11+B22-2*B12
    b=2*B12-2*B22
    c=B22
    D=b**2-4*a*c
    alpha=0.5
    if D>=-1e-12 and np.abs(a)>1e-6:
      alpha=(-b+np.sqrt(np.abs(D)))/(2*a)
      #V=alpha*V1+(1-alpha)*V2
      V=eigenvector_scale(alpha*V1+(1-alpha)*V2)
      T=PS(V,V)
      if T<tol:
        aVecs.append(V)
      else:
        aVecs.append(None)
    elif np.abs(b)>1e-6:
      alpha=-c/b
      V=eigenvector_scale(alpha*V1+(1-alpha)*V2)
      T=PS(V,V)
      if T<tol:
        aVecs.append(V)
      else:
        aVecs.append(None)
    else:  
      aVecs.append(None)
  return aVecs,labels