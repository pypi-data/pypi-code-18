import numpy as np
from scipy import sparse

# A(tgr,tgc) <- A(tgr,tgc)+Ai
def sum_sub_mat(A,Ai,tgr,tgc):
  if Ai is None:
    return A
  if A.shape==Ai.shape:
    return A+Ai
  (I,J,K)=sparse.find(Ai)
  A+=sparse.csc_matrix((K,(tgr[I],tgc[J])),shape=A.shape)
  return A

def csr_zero_rows(A, rows_to_zero):
  if not isinstance(A, sparse.csc_matrix):
    raise ValueError('Matrix given must be of CSR format.')
  mask=np.in1d(A.indices, rows_to_zero)
  A.data[mask]=0
  #A.eliminate_zeros()
  #A.eliminate_zeros()

def csr_one_rows(A, rows_to_zero):
  if not isinstance(A, sparse.csc_matrix):
    raise ValueError('Matrix given must be of CSR format.')
  mask=np.in1d(A.indices, rows_to_zero)
  A.data[mask]=1
  
def csr_sum_onerow(A, row):
  if not isinstance(A, sparse.csc_matrix):
    raise ValueError('Matrix given must be of CSR format.')
  mask=np.in1d(A.indices, row)
  return sum(A.data[mask])