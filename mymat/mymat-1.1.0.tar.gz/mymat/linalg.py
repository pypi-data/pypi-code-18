# -*- coding: utf-8 -*-

# linear algebra

import numpy as np

import mymat

class Decomposition:
    
    @classmethod
    def random(cls, m, n=None):
        if n is None:
            m = n
        return cls(mymat.MyMat.random(m,n,randfun=np.random.rand))


class LUDecompsition(Decomposition):
    '''LU (Doolittle) Decompsition of matrix
    matrix: matrix'''
    def __init__(self, matrix):
        self.matrix = matrix

    def solve(self):
        # return L, U that A = LU
        A = self.matrix.copy()
        m, n = A.shape
        A[2:,1] /= A[1,1]
        N = min(m, n)
        for r in range(2, N):
            A[r, r:] -= A[r,1:r-1] * A[1:r-1,r:]
            A[r+1:, r] = (A[r+1:, r] - A[r+1:, 1:r-1] * A[1:r-1, r]) / A[r, r]
        A[N, N:] -= A[N,1:N-1] * A[1:N-1,N:]
        return A.tril(-1) + mymat.MyMat.eye(m, n), A.triu()

    def process(self):
        # return L, U that A = LU
        A = self.matrix.copy()
        m, n = A.shape
        A[2:,1] /= A[1,1]
        N = min(m, n)
        s = [A.totex()]
        for r in range(2, N):
            A[r, r:] -= A[r,1:r-1] * A[1:r-1,r:]
            A[r+1:, r] = (A[r+1:, r] - A[r+1:, 1:r-1] * A[1:r-1, r]) / A[r, r]
            s.append(A.totex())
        A[N, N:] -= A[N,1:N-1] * A[1:N-1,N:]
        s.append(A.totex())
        return '\\Rightarrow'.join(s)

class CholeskyDecompsition(Decomposition):
    '''Cholesky Decompsition of sysmetric matrix
    matrix: matrix'''
    def __init__(self, matrix):
        self.matrix = matrix

    def solve(self):
        # return L, that A = LL'
        A = self.matrix.copy()
        m, n = A.shape
        A[1,1] = np.sqrt(A[1,1])
        A[:,1] /= A[1,1]
        for r in range(2, m):
            A[r, r] = np.sqrt(A[r, r] - A[r, :r-1].norm()**2)
            A[r+1:, r] = (A[r+1:, r] - A[r+1:, :r-1] * A[r, :r-1].T) / A[r, r]
        A[m, n] = np.sqrt(A[m, n] - A[m, :n-1].norm()**2)
        return A.tril()

    def process(self):
        # return L, that A = LL'
        A = self.matrix.copy()
        m, n = A.shape
        A[1,1] = np.sqrt(A[1,1])
        A[:,1] /= A[1,1]
        s = [A.totex()]
        for r in range(2, m):
            A[r, r] = np.sqrt(A[r, r] - A[r, :r-1].norm()**2)
            A[r+1:, r] = (A[r+1:, r] - A[r+1:, :r-1] * A[r, :r-1].T) / A[r, r]
            A[r, r+1:] = A[r+1:, r].T
            s.append(A.totex())
        A[m, n] = np.sqrt(A[m, n] - A[m, :n-1].norm()**2)
        s.append(A.totex())
        return '\\Rightarrow'.join(s)


class ChasingDecompsition(Decomposition):
    '''Chasing Decompsition of tri-diagonal matrix
    matrix: matrix'''
    def __init__(self, matrix):
        self.matrix = matrix

    def solve(self):
        # return L, U that A = LU
        A = self.matrix.copy()
        m, n = A.shape
        A[1,2] /= A[1,1]
        for r in range(2, m):
            A[r, r] -= A[r,r-1] * A[r-1,r]
            A[r, r+1] /= A[r, r]
        A[m, m] -= A[m, m-1] * A[1:m-1,m]
        return A.tril(-1) + mymat.MyMat.eye(m, n), A.triu()

    def process(self):
        # return L, U that A = LU
        A = self.matrix.copy()
        m, n = A.shape
        A[1,2] /= A[1,1]
        s = [A.totex()]
        for r in range(2, m):
            A[r, r] -= A[r,r-1] * A[r-1,r]
            A[r, r+1] /= A[r, r]
            s.append(A.totex())
        A[m, m] -= A[m, m-1] * A[m-1,m]
        s.append(A.totex())
        return '\\Rightarrow'.join(s)

