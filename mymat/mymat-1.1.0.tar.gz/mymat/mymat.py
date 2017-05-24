# -*- coding: utf-8 -*-

import fractions

import numpy as np
import numpy.linalg as LA

'''notations (abbreviation):
num: complex number
ind: index (int, slice or list, or tuple of index sometimes)
ind1, ind2: row index, column index
sglind: single index (int, slice or list)
crd: coordinate
vec: vector
colvec: column vector
slc: slice
ran: range
lst: list
mat: matrix
r(m): row
c(n): column
'''


# python for my matrix type

# special matrices:
def O(m, n=None, dtype=np.int32):
    # 0 matrix
    # deprecated, use MyMat.zeros
    return MyMat.zeros(m, n, dtype)


def I(m, n=None, dtype=np.int32):
    # identity matrix
    # deprecated, use MyMat.eye
    return MyMat.eye(m, n, dtype)

# maps
def mat_map(f, *As):
    # matrices (np.matrix) in As have the same size
    rn, cn = As[0].shape    # size (shape) of matrix
    return np.mat([[f(*(A[k, l] for A in As)) for l in range(cn)] for k in range(rn)])


# relations
# will be used in test
def equal(A, *Ms):
    A = BaseMatrix(A)
    if A.isempty():
        for M in Ms:
            if not BaseMatrix(M).isempty():
                return False
        return True
    for M in Ms:
        M = np.mat(M)
        if A.shape != M.shape or (A != M).any():
            return False
    return True


def equal_tol(A, *Ms, tol=0.001):
    for k, M in enumerate(Ms):
        M = np.mat(M)
        for N in Ms[k+1:]:
            N = np.mat(N)
            if A.shape != M.shape or LA.norm(A - M)>=tol:
                return False
    return True

# def isreal(x):
#     return isinstance(x, (int, float))

def isscalar(x):
    return np.isscalar(x) or isinstance(x, fractions.Fraction) or isinstance(x, MyMat) and x.isscalar()


# concepts for index
def issgl(x):
    # single index used in python
    return isinstance(x, (int, slice, list))

def isemp(x, N):
    # empty index
    if isinstance(x, list):
        return x == [] or all((a>N or a<=-N) for a in x)
    elif isinstance(x, slice):
        x = fixslice(x, N)
        if x.step is None or x.step >0:
            return x.start >= x.stop or x.stop<-N or x.start>=N
        else:
            return x.start <= x.stop or x.start<-N or x.stop>=N
    elif isinstance(x, int):
        return x>N or x<=-N
    elif isinstance(x, tuple):
        return isemp(x[0]) or isemp(x[1])
    else:
        return False

def fixslice(slc, N):
    # specify slice
    if slc.step is None or slc.step >0:
        if slc.start is None:
            start = 0
        elif slc.start <0:
            start = slc.start + N
        else:
            start = slc.start
        if slc.stop is None:
            stop = N-1
        elif slc.stop <0:
            stop = slc.stop + N
        else:
            stop = slc.stop
    else:  # slc.step <0
        if slc.start is None:
            start = N-1
        elif slc.start <0:
            start = slc.start + N
        else:
            start = slc.start
        if slc.stop is None:
            stop = 0
        elif slc.stop <0:
            stop = slc.stop + N
        else:
            stop = slc.stop
    return slice(start, stop, slc.step)

def iscrd(x):
    # coordinate type index, e.g. A[[1,2],[2,3]]
    return isinstance(x, tuple) and isinstance(x[0], list) and isinstance(x[1], list)

COLON = slice(None)
COLON2 = (slice(None), slice(None))

# transform of the indices
import itertools

def times(ind, dim=1):
    '''tranform coordinate index to double index
>>> times(([1,2],[3,4,6]))
([1, 1, 1, 2, 2, 2], [3, 4, 6, 3, 4, 6])
>>> times(([1,2],[3,4,6]), 2)
([1, 2, 1, 2, 1, 2], [3, 3, 4, 4, 6, 6])
'''
    if iscrd(ind):
        if dim == 1:
            lst = itertools.product(ind[0],ind[1])
            b=([], [])
            for a in lst:
                b[0].append(a[0])
                b[1].append(a[1])
            return b
        else: # dim == 2
            lst = itertools.product(ind[1],ind[0])
            b=([], [])
            for a in lst:
                b[0].append(a[1])
                b[1].append(a[0])
            return b
    else:
        return ind

def ind2iter(ind, N):
    # transform slice to range, int and list to list
    if isinstance(ind, list):
        return ind
    elif isinstance(ind, slice): # slc is a slice
        c = ind.step
        if c is None or c>0:
            a = ind.start if ind.start else 0
            b = ind.stop if ind.stop else N     # 0 <= a <= b <= N
            return (range(a, b, c) if c else range(a,b)) if a <= b else []
        elif c<0:
            a = ind.start if ind.start else N-1
            b = ind.stop if ind.stop else 0     # 0 <= b <= a <= N
            return range(a, b, c) if b <= a else []
        else:
            raise ValueError('slice step cannot be zero!')
    else:
        return [ind]

def ind2tuple(ind, N):
    # slice, int and list to list
    # call ind2iter
    # used in delete method
    if isinstance(ind, list):
        return tuple(ind)
    elif isinstance(ind, slice): # slc is a slice
        return tuple(ind2iter(ind, N))
    else:
        return (ind,)

# def restrain(ind, N):
#     # specify slice and list
#     if isinstance(ind, list):
#         return [a for a in ind if -N<=a<N]
#     elif isinstance(ind, slice): # ind is a slice
#         if ind.step is None or ind.step >0:
#             if ind.start <0:
#                 ind.start += N
#             elif ind.start is None:
#                 ind.start = 0
#             else:
#                 ind.start = min(ind.start, N-1)
#             if ind.stop <0:
#                 ind.stop += N
#             elif ind.stop is None:
#                 ind.stop = N-1
#             else:
#                 ind.stop = min(ind.stop, N-1)
#         else:
#             if ind.start <0:
#                 ind.start += N
#             elif ind.start is None:
#                 start = N-1
#             else:
#                 start = min(ind.start, N-1)
#             if ind.stop <0:
#                 stop = ind.stop + N
#             elif ind.stop is None:
#                 ind.stop = 0
#             else:
#                 ind.stop = min(ind.stop, N-1)
#         return ind
#     else:
#         return min(ind, N-1) if ind >=0 else ind + N


def ind2ind(ind):
    '''index of matlab type to index of python type
This is the main gimmick to define MyMat.
It calls slice2slice.
'''
    if isinstance(ind, tuple):
        return tuple(ind2ind(a) for a in ind)
    if isinstance(ind, list):
        return [a - 1 for a in ind]
    elif isinstance(ind, slice):
        return slice2slice(ind)       # see its definition
    else:
        return ind - 1

def slice2slice(slc):
    '''slice of matlab style to slice of python style
for example: M[1:3] := M[0:3]
>>> slice2slice(slice(1, 6, 2))
slice(0, 6, 2)
>>> slice2slice(slice(-3, 0))
slice(-4, None, None)
>>> ind2ind(slice(5,2,-1))
slice(4, 0, -1)
'''
    a, b, c = slc.start, slc.stop, slc.step
    if c is None or c > 0:
        # if a <= b:
        return slice(a-1 if a else None, None if b == 0 else b, c)
    elif c < 0:
        # if a >= b:
        return slice(a-1 if a else None, None if b == 1 or b is None else b-2, c)
    else:
        raise ValueError('slice step cannot be zero!')

def int2pair(ind, r, c=1):
    '''
>>> int2pair(ind2ind([3,4,7,10]),5,5)
([2, 3, 1, 4], [0, 0, 1, 1])
'''
    if isinstance(ind, int):
        return np.mod(ind, r), np.floor_divide(ind, r)
    else:
        #~if c is None:
        #~    c = np.ceil(maxind(ind)/r)
        return [np.mod(a, r) for a in ind], [np.floor_divide(a, r) for a in ind2iter(ind, r*c)]

def pair2int(ind, r, c=None):
    '''inverse of int2pair
>>> pair2int(int2pair([4,7,12,22],5,5),5,5)
[4, 7, 12, 22]
'''
    if isinstance(ind[0], int) and isinstance(ind[1], int):
        return ind[0] + r * ind[1]
    else:
        if c is None:
            c=max(ind[1])
        return [a + r * b for a, b in zip(ind2iter(ind[0], r), ind2iter(ind[1], c))]

"""
# int2pair(ind2ind) == ind2ind(int2pair2)
def int2pair2(ind, r, c=1):
    # single index (int) => pair index (tuple)
    if isinstance(ind, int):
        return (r, np.floor_divide(ind, r)) if np.mod(ind, r)==0 else (np.mod(ind, r), np.floor_divide(ind, r)+1)
    else:  # extend to lists or slices
        ind=ind2iter(ind, r * c)
        p=([],[])
        for a in ind:
            if np.mod(a, r)==0:
                p[0].append(r); p[1].append(np.floor_divide(a, r))
            else:
                p[0].append(np.mod(a, r)); p[1].append(np.floor_divide(a, r)+1)
        return p
"""

def maxind(ind, N):
    # only for single index:
    if isinstance(ind, int):
        return ind
    elif isinstance(ind, list):
        return max(ind)
    elif isinstance(ind, slice):
        c = ind.step
        if c is None or c > 0:
            return ind.stop - 1 if ind.stop else N-1
        elif c < 0:
            return ind.start - 1 if ind.start else N-1
        else:
            raise ValueError('slice step cannot be zero!')
    else:
        raise TypeError('function maxind only for single index!')


# definition of Base Class of MyMat
class BaseMatrix(np.matrix):
    """Base class of MyMat"""

    def __new__(cls, data, *args, **kwargs):
        if isinstance(data, (list, tuple, range, np.matrix)):
            data=np.array(data)
        elif isinstance(data, str):
            if '\\\\' in data or '&' in data:
                import re
                rx1 = re.compile('\\\\')
                rx2 = re.compile('&')
                data = rx2.sub(',', rx1.sub(';', data))
            data = np.array(np.matrix(data))    # default type
        elif isscalar(data):
            data = np.array(data)
        else:
            pass # data = data
        #elif isinstance(data, BaseMatrix):
        #    return data
        if data.dtype != np.complex128 and data.dtype != object:
            kwargs.setdefault('dtype', np.float64)
        return super(BaseMatrix, cls).__new__(cls, data, *args, **kwargs)

    def __repr__(self):
        # see join
        if self.isempty():
            return 'Empty matrix'
        else:
            return '['+self.join(ch2=';\n ')+']: M(%d X %d)'%(self.shape)

    @classmethod
    def random(cls, m, n=None, randfun=np.random.rand):
        # generate a random matrix
        # randfun: m, n -> m X n - matrix
        if n is None:
            n = m
        return cls(randfun(m, n))

    @classmethod
    def randint(cls, m, n=None, lb=0, ub=10):
        # random matrix
        if n is None:
            n = m
        return cls(np.random.randint(lb, ub, size=(m, n)), dtype=np.int32)

    @classmethod
    def empty(cls):
        # empty matrix
        return cls([])

    @classmethod
    def zeros(cls, m, n=None, dtype=np.int32):
        # 0 matrix
        if n is None:
            n = m
        return cls(np.zeros((m, n)), dtype=dtype)

    @classmethod
    def ones(cls, m, n=None, dtype=np.int32):
        # 1 matrix
        if n is None:
            n = m
        return cls(np.ones((m, n)), dtype=dtype)

    @classmethod
    def eye(cls, m, n=None, dtype=np.int32):
        # identity matrix
        if n is None:
            n = m
        return cls(np.eye(m, n), dtype=dtype)

    @classmethod
    def map(cls, f, *As):
        # matrices (MyMat) in As have the same size
        rn, cn = As[0].shape    # size (shape) of matrix
        return cls([[f(*(A[k, l] for A in As)) for l in range(cn)] for k in range(rn)])

    @classmethod
    def fromFunc(cls, func, m=1, n=None):
        if n is None:
            n = m
        return cls([[func(k, l) for l in range(n)] for k in range(m)])

    # matlab style operator:
    def __mul__(self, other):
        if isinstance(other, BaseMatrix):
            if other.isscalar():
                other = other.toscalar()
            if self.isscalar():
                return self.toscalar() * other
            else:
                return super(BaseMatrix, self).__mul__(other)
        elif np.isscalar(other):
            return super(BaseMatrix, self).__mul__(other)
        elif isinstance(other, fractions.Fraction):
            return self.apply(lambda x: x * other)
        else:
            return super(BaseMatrix, self).__mul__(BaseMatrix(other))

    def __rmul__(self, other):
        return self * other

    def __imul__(self, other):
        self.update(self * other)
        return self

    def __pow__(self, other):
        # A**B := A.*B
        return self.__class__(np.multiply(self, other))

    def __rpow__(self, other):
        # B**A := B.*A
        return self.__class__(np.multiply(other, self))

    def __ipow__(self, other):
        self.update(self ** other)
        return self

    def __floordiv__(self, other):
        # A//B := A./B
        return self.__class__(np.divide(self, other))

    def __rfloordiv__(self, other):
        # B//A := B./A
        return self.__class__(np.divide(other, self))

    def __ifloordiv__(self, other):
        self.update(self // other)
        return self

    def __truediv__(self, other):
        # A/B := A/B (A*inv(B))
        if isinstance(other, BaseMatrix) and other.isscalar():
            return self.__class__(np.divide(self, other.toscalar()))
        elif isscalar(other):
            return self * (1 / other)  # = 1/other * self
        return self * other.I

    def __rtruediv__(self, other):
        # r/A := r/A (r * inv(A))
        return other * self.I

    def __itruediv__(self, other):
        self.update(self / other)
        return self

    def __xor__(self, num):
        # A^n := A^n, n is int
        if isinstance(num, BaseMatrix) and num.isscalar():
            return super(BaseMatrix, self).__pow__(num.toscalar())
        return super(BaseMatrix, self).__pow__(num)

    def __rxor__(self, num):
        pass

    def __ixor__(self, num):
        self.update(self ^ other)
        return self

    def __lshift__(self, other):
        # A<<B := A.^B
        return self.__class__(np.power(self, other))

    def __rlshift__(self, other):
        # r<<A := r.^A
        return self.__class__(np.power(other, self))

    def __ilshift__(self, other):
        self.update(self << other)
        return self

    @property
    def I(self):
        return self.__class__(self.getI())

    # get-set methods:
    """don't define __setitem__ directly"""
    def __getitem__(self, ind):
        # don't call get
        r, c = self.shape
        if iscrd(ind):
            # for coordinate-type index
            self = super(BaseMatrix, self).__getitem__((ind[0], COLON))
            return super(BaseMatrix, self).__getitem__((COLON, ind[1]))
        else:
            if issgl(ind):
                return super(BaseMatrix, self).__getitem__(int2pair(ind, r, c))
            return super(BaseMatrix, self).__getitem__(ind)

    def get(self, ind):
        # ind can be single index
        r, c = self.shape
        if issgl(ind):
            return super(BaseMatrix, self).__getitem__(int2pair(ind, r, c))
        return super(BaseMatrix, self).__getitem__(ind)

    def ezset(self, i, j, val=0):
        # get element A(i,j)
        return super(BaseMatrix, self).__setitem__((i,j), val)

    def ezget(self, i, j, val=0):
        # get element A(i,j)
        return super(BaseMatrix, self).__getitem__((i,j))

    def __setitem__(self, ind, val):
        # call set
        if val == []:
            self.update(self.delete(ind1=ind[0], ind2=ind[1]))
            return
        r, c = self.shape
        if issgl(ind):
            self.set(ind, val)
        else:
            if iscrd(ind):
                if np.isscalar(val):
                    self.set(times(ind), val)
                elif isinstance(val, MyMat):
                    if val.isscalar():
                        self.set(times(ind), val.toscalar())
                    else:
                        self.set(times(ind), val.flatten().tolist())
                else: # val is a number or a list
                    self.set(times(ind), MyMat(val))
            else:
                self.set(ind, val)

    def set(self, ind, val):
        # call maxind
        r, c = self.shape
        if issgl(ind):   # single index
            mx = maxind(ind, r*c)
            if mx >= r*c:
                mx1, mx2 = int2pair(mx + 1, r, c)
                self.just(max(r, mx1+1), max(c, mx2+1))

            if np.isscalar(val):
                super(BaseMatrix, self).__setitem__(int2pair(ind, r, c), val)
            elif isinstance(val, list):
                super(BaseMatrix, self).__setitem__(int2pair(ind, r, c), val)
            elif isinstance(val, BaseMatrix):
                if val.isscalar():
                    super(BaseMatrix, self).__setitem__(int2pair(ind, r, c), val.toscalar())
                elif val.isrowvec():
                    super(BaseMatrix, self).__setitem__(int2pair(ind, r, c), val.tolist())
                elif val.iscolvec():
                    super(BaseMatrix, self).__setitem__(int2pair(ind, r, c), val.T.tolist())
            elif isinstance(val, np.matrix):
                super(BaseMatrix, self).__setitem__(int2pair(ind, r, c), BaseMatrix(val))
        else:      # double index
            if self.index_type == 'matlab':
                if isinstance(ind[0], int):
                    mx1 = ind[0]
                    if isinstance(ind[1], int):
                        mx2 = ind[1]
                        if mx1 > r or mx2 > c:
                            self.just(max(r, mx1), max(c, mx2))
                    else:
                        mx2 = maxind(ind[1], c)
                        if mx1 > r or mx2 >= c:
                            self.just(max(r, mx1), max(c, mx2+1))
                else:
                    mx1 = maxind(ind[0], r)
                    if isinstance(ind[1], int):
                        mx2 = ind[1]
                        if mx1 >= r or mx2 > c:
                            self.just(max(r, mx1+1), max(c, mx2))
                    else:
                        mx2 = maxind(ind[1], c)
                        if mx1 >= r or mx2 >= c:
                            self.just(max(r, mx1+1), max(c, mx2+1))
            else:
                mx1 = maxind(ind[0], c)
                mx2 = maxind(ind[1], c)
                if mx1 >= r or mx2 >= c:
                    self.just(max(r, mx1+1), max(c, mx2+1))
            if isscalar(val) or isinstance(val, BaseMatrix):
                super(BaseMatrix, self).__setitem__(ind, val)
            elif isinstance(val, (list, np.matrix)):
                super(BaseMatrix, self).__setitem__(ind, BaseMatrix(val))

    def delete(self, ind1=[], ind2=[]):
        r, c = self.shape
        if not isemp(ind1, r):
            ind1=ind2tuple(ind1, r)
            self=np.concatenate(tuple(super(BaseMatrix, self).__getitem__((slice(a+1,b), COLON)) for a, b in zip((-1,)+ind1, ind1+(r,)) if b-a!=1))
            if self.isempty():
                return self.empty()
        if not isemp(ind2, c):
            ind2=ind2tuple(ind2, c)
            return np.concatenate(tuple(super(BaseMatrix, self).__getitem__((COLON, slice(a+1,b))) for a, b in zip((-1,)+ind2, ind2+(c,)) if b-a!=1), 1)
        else:
            return self.copy()


    def update(self, other):
        # change the value preserving the id
        if self.dtype != other.dtype:
            try:
                self.dtype = other.dtype
            except Exception as ex:
                print(ex)
                print('Fail to convert %s to %s when calling update'%(self.dtype, other.dtype))
        if self.shape != other.shape:
            self.resize(other.shape, refcheck=False)
        super(BaseMatrix, self).__setitem__((COLON, COLON), other)

    def __call__(self, *ind):
        if len(ind)==1:
            return self[ind[0]]
        return self[ind]

    # shape methods:
    def cat(self, *others, dim=1):
        if self.isempty():
            return np.concatenate(others, axis=dim-1)
        elif not others:
            return self
        else:
            return np.concatenate((self,)+others, axis=dim-1)

    def __or__(self, other):
        return np.concatenate((self, other), 1)

    def __ior__(self, other):
        self.update(self | other)
        return self

    def __and__(self, other):
        return np.concatenate((self, other))

    def __iand__(self, other):
        self.update(self & other)
        return self

    def just(self, m, n=None):
        if n is None: n = m
        r, c = self.shape
        if 0 < m <= r:
            temp = super(BaseMatrix, self).__getitem__((slice(m), slice(c)))
        elif m > r:
            temp = self & self.zeros(m - r, c)
        elif -r <= m < 0:
            m = - m
            temp = super(BaseMatrix, self).__getitem__((slice(r-m, r), slice(c)))
        elif m < -r:
            m = - m
            temp = self.zeros(m - r, c) & self
        else:
            temp = self.empty()
            self.update(temp); return # self
        if 0 < n <= c:
            temp = super(BaseMatrix, temp).__getitem__((slice(m), slice(n)))
        elif n > c:
            temp = temp | self.zeros(m, n - c)
        elif -c <= n < 0:
            temp = super(BaseMatrix, temp).__getitem__((slice(m), slice(c+n, c)))
        elif n < -c:
            temp = self.zeros(m, - n - c) | temp
        else:
            temp = self.empty()
        self.update(temp)
        # return self

    def repmat(self, m=2):
        return np.tile(self, m)


    # conversion:
    def change_type(self, dtype=np.float64):
        return np.asmatrix(self, dtype)

    def tofrac(self):
        # to matrix of fractions
        return self.apply(fractions.Fraction)

    def __str__(self):
        # see join
        return '['+self.join(ch2=';\n ')+']'

    def join(self, ch1=', ', ch2='; '):
        r, c = self.shape
        return ch2.join(ch1.join(str(super(BaseMatrix, self).__getitem__((k, l))) for l in range(c)) for k in range(r))

    def totex(self):
        return '\\begin{bmatrix}\n' + self.join(ch1=' & ', ch2='\\\\\n') + '\n\\end{bmatrix}'

    def tolineq(self):
        '''return linear equation object
        '''
        A = super(BaseMatrix, self).__getitem__((COLON, slice(0, -1)))
        b = super(BaseMatrix, self).__getitem__((COLON, -1))
        return LinearEquation(A, b)


    def toscalar(self):
        return super(BaseMatrix, self).__getitem__((0,0))

    def tolist(self):
        if self.isrowvec():
            # return list of numbers
            return super(BaseMatrix, self).tolist()[0]
        else:
            return super(BaseMatrix, self).tolist()

    def toarray(self):
        if self.isrowvec():
            return self.A1
        else:
            return self.A

    def tomatrix(self):
        return np.matrix(self.tolist())

    def tomat(self):
        # == tomatrix
        return np.mat(self.tolist())

    def tovec(self, dim=1):
        if dim==1:
            return self.__class__([[self[k, l]] for l in range(1, self.shape[1]+1) for k in range(1, self.shape[0]+1)])
        elif dim==2:
            lst=[]
            for k in range(1, self.shape[0]+1):
                lst.extend(self[k,:].tolist())
            return self.__class__(lst)

    # comparison methods
    def wequal(self, *others):
        # weakly equal
        if self.isempty():
            for other in others:
                if not BaseMatrix(other).isempty():
                    return False
            return True
        for other in others:
            other = BaseMatrix(other)
            if self.shape != other.shape or (self != other).any():
                return False
        return True

    def equal(self, *others):
        # others must be a tuple of BaseMatrix-s
        if self.isempty():
            for other in others:
                if not other.isempty():
                    return False
            return True
        for other in others:
            if self.shape != other.shape or (self != other).any():
                return False
        return True

    # is* methods
    def isempty(self):
        return self.shape[1]==0 or self.shape[0]==0

    def isscalar(self):
        return self.shape == (1, 1)

    def isrowvec(self):
        return self.shape[0] == 1

    def iscolvec(self):
        return self.shape[1] == 1

    def issquare(self):
        return self.shape[0] == self.shape[1]

    def isvec(self):
        return self.isrowvec() or self.iscolvec()

    def issymmetic(self):
        return self.equal(self.T)

    def ishermite(self):
        return self.equal(self.H)

    def isunitary(self):
        m, n=self.shape
        return m == n and (self.H*self).equal(np.eye(m, n))

    # calculate methods:
    def norm(self, p=2):
        if self.isrowvec():
            return LA.norm(self.toarray(), p)
        elif self.iscolvec():
            return LA.norm(self.T.toarray(), p)
        else:
            return LA.norm(self, p)

    def det(self):
        if self.issquare():
            return LA.det(self)
        else:
            raise Exception('it is not a square matrix!')

    def expm(self, N=10):
        p=[1/np.prod(range(1, n+1)) for n in range(N)]
        return self.poly(p)

    def rho(self):
        return max(map(abs, LA.eig(self)[0]))

    def plus(self, num=1):
        m, n = self.shape
        if num == 1:
            return self + self.eye(m, n, dtype=self.dtype)
        elif num == 0:
            return self
        else:
            return self + num * self.eye(m, n, dtype=self.dtype)

    def poly(self, p):
        # self is a square matrix
        r, c = self.shape
        if r != c:
            raise Exception('The matrix should be square!')
        if p == []:
            return self.zeros(r)
        elif len(p) == 1:
            return p[0] * self.eye(r, dtype=self.dtype)
        else:
            return (self.poly(p[1:])*self).plus(r, dtype=self.dtype)

    def diag(self, k=0, form='matrix'):
        m, n = self.shape
        if form == 'matrix':
            other = self.zeros(m, n, dtype=self.dtype)
        if 0 <= k < n:
            for i in range(min(m, n-k)):
                super(BaseMatrix, other).__setitem__((i, i+k), super(BaseMatrix, self).__getitem__((i, i+k)))
        elif -m < k < 0:
            for i in range(-k, min(m, n)):
                super(BaseMatrix, other).__setitem__((i, i+k), super(BaseMatrix, self).__getitem__((i, i+k)))
        else:
            if 0 <= k < n:
                L = min(m, n-k)
                other = self.zeros(L, 1)
                for i in range(L):
                    super(BaseMatrix, other).__setitem__((L, i), super(BaseMatrix, self).__getitem__((i, i+k)))
            elif -m < k < 0:
                L = min(n, m+k)
                other = self.zeros(L, 1)
                for i in range(-k, L):
                    super(BaseMatrix, other).__setitem__((L, i), super(BaseMatrix, self).__getitem__((i, i+k)))

    def tril(self, k=0):
        cpy = self.copy()
        m, n = cpy.shape
        if 0<= k <n-1:
            for i in range(0, min(m, n-k-1)):
                for j in range(i+k+1, n):
                    super(BaseMatrix, cpy).__setitem__((i, j), 0)
                # cpy[i, i+k+1:] = 0
        elif -m< k <0:
            super(BaseMatrix, cpy).__setitem__((slice(0, -k), COLON), 0)
            # cpy[1:-k, :] = 0
            for i in range(-k, min(m, n-k-1)):
                for j in range(i+k+1, n):
                    super(BaseMatrix, cpy).__setitem__((i, j), 0)
                # cpy[i, i+k+1:] = 0
        elif k <=-m:
            cpy = self.zeros(m, n, dtype=self.dtype)
        return cpy

    def triu(self, k=0):
        cpy = self.copy()
        m, n=cpy.shape
        if 1<= k <=n-1:
            super(BaseMatrix, cpy).__setitem__((COLON, slice(0, k)), 0)
            for j in range(k, min(n, m+k-1)):
                for i in range(j-k+1, m):
                    super(BaseMatrix, cpy).__setitem__((i, j), 0)
        elif -m< k <=0:
            for j in range(min(n, m-k-1)):
                for i in range(j-k+1, m):
                    super(BaseMatrix, cpy).__setitem__((i, j), 0)
        elif k > n-1:
            cpy = self.zeros(m, n, dtype=self.dtype)
        return cpy

    def itril(self):
        A = self.tril(-1)
        return A.plus(1)


    def itriu(self):
        A = self.triu(1)
        return A.plus(1)

    def comat(self, ind1=[], ind2=[]):
        # co-matrix called in cofactor
        cpy = self.copy()
        return cpy.delete(ind1, ind2)

    def cofactor(self, i=1, j=1):
        # algebaric cofactor
        M = self.comat(i, j)
        return (-1)**(i+j)*M.det()


    # drawing
    def draw(self, show=False, *args, **kwargs):
        import matplotlib.pyplot as plt
        r, c = self.shape
        if r == 1:
            ph = plt.plot(self.tolist(), *args, **kwargs)
        elif c == 1:
            ph = plt.plot(self.T.tolist(), *args, **kwargs)
        else:
            ph = [plt.plot(self.tolist()[k], *args, **kwargs) for k in range(r)]
        if show: plt.show()
        return ph

    # others
    def apply(self, func):
        m, n = self.shape
        return self.__class__([[func(super(BaseMatrix, self).__getitem__((k, l))) for l in range(n)] for k in range(m)])


class MyMat(BaseMatrix):

    index_type = 'matlab'

    def __new__(cls, data, *args, **kwargs):
        if isinstance(data, MyMat):
            return data
        elif isinstance(data, BaseMatrix):
            data = np.array(data)
        return super(MyMat, cls).__new__(cls, data, *args, **kwargs)

    # get-set methods
    def __getitem__(self, ind):
        # another version of get
        ind = ind2ind(ind)
        return super(MyMat, self).__getitem__(ind)

    def get(self, ind):
        ind = ind2ind(ind)
        return super(MyMat, self).get(ind)


    def set(self, ind, val):
        if issgl(ind):   # single index
            ind = ind2ind(ind)   # transform the index
            super(MyMat, self).set(ind, val)
        else:      # double index
            # why does not it need ind2ind in these cases?
            # because super(MyMat, self).__setitem__ may call __getitem__ method that has been overiden
            if isinstance(ind[0], slice) and isinstance(ind[1], (int, slice)) or isinstance(ind[0], int) and isinstance(ind[1], slice):
                pass
            else:
                ind = ind2ind(ind)  # tranform the matrix-index to py-index
            super(MyMat, self).set(ind, val)

    def ezset(self, i, j, val=0):
        # get element A(i,j)
        return super(MyMat, self).__setitem__((i-1,j-1), val)

    def ezget(self, i, j, val=0):
        # get element A(i,j)
        return super(MyMat, self).__getitem__((i-1,j-1))


    def delete(self, ind1=[], ind2=[]):
        # delete ind1-row and ind2-column
        r, c = self.shape
        if not isemp(ind1, r):
            ind1 = ind2tuple(ind2ind(ind1), r)
            if ind1 == list(range(r)):
                return self.empty()
            self = np.concatenate(tuple(super(MyMat, self).__getitem__((slice(a+1,b), COLON)) for a, b in zip((-1,)+ind1, ind1+(r,)) if b-a!=1))
        if not isemp(ind2, c):
            ind2 = ind2tuple(ind2ind(ind2), c)
            if ind2 == list(range(c)):
                return self.empty()
            return np.concatenate(tuple(super(MyMat, self).__getitem__((COLON, slice(a+1,b))) for a, b in zip((-1,)+ind2, ind2+(c,)) if b-a!=1), 1)
        else:
            return self

    @classmethod
    def map(cls, f, *As):
        # matrices (MyMat) in As have the same size
        r, c = As[0].shape    # size (shape) of matrix
        return cls([[f(*(A[k, l] for A in As)) for l in range(1, c+1)] for k in range(1, r+1)])


    # linear algebra:
    def proj(self, ind1=COLON, ind2=COLON):
        # projection on ind1-row and ind2-column
        # calls compind
        r, c = self.shape
        ind1 = compind(ind1, r)
        ind2 = compind(ind2, c)
        if ind1 != []:
            self[ind1, COLON] = 0
        if ind2 != []:
            self[COLON, ind2] = 0
        return self

    def robinson(self, k, x):
        # A(k->x)
        cpy = self.copy()
        cpy[COLON, k] = x
        return cpy

    # elementary transforms
    def row_transform1(self, i, j):
        # swap row i and row j
        self[i,:], self[j, :] = self[j,:].copy(), self[i,:].copy()
        return self

    def row_transform2(self, i, k):
        # k != 0 generally
        self[i,:] = k * self[i,:]
        return self

    def row_transform3(self, i, j, k):
        # row i + k * row j
        self[i,:] += k * self[j,:]
        return self

    def col_transform1(self, i, j):
        self[:, i], self[:, j] = self[:, j].copy(), self[:, i].copy()
        return self

    def col_transform2(self, i, k):
        self[:, i] = k * self[:, i]
        return self

    def col_transform3(self, i, j, k):
        self[:, i] += k * self[:, j]
        return self

    def echelon(self):
        '''echelon form of matrix:
        any matrix -> echelon form by elementary row transforms
        if rank(A) == r, then the echelon form of A is
                [A0 e1 A1 e2 A2 ... er Ar],
        where ek = [0,...,1,...0]' and Ar is empty or A[k,:]==0 when k>r.
        '''
        r, c = self.shape
        A = self.copy()
        # Gauss Elimintation Process
        k = l = 1
        cols = []
        while k<=r and l<c:
            if all(A[k:r, l]==0):
                l += 1
                continue

            for index, p in enumerate(A[k:r, l].T.tolist()):
                # find the first nonzero element or the element with maximum abstract value
                if p != 0:
                    ind = index
                    break
            if ind != 0:                                               # swap row_k, row_u
                u = k + ind
                A[k, l:c], A[u, l:c]=A[u, l:c].copy(), A[k, l:c].copy()

            if A[k, l] != 1:
                if l < c:
                    A[k, (l+1):c] /= A[k, l]
                A[k, l]=1

            if k < r:
                A[k+1:r, l+1:c] -= A[k+1:r, l]*A[k, l+1:c]
                A[k+1:r, l] = 0
            cols.append(l)
            k += 1; l += 1
        # if k == r:
        #     if A[k, l] != 0 and A[k, l] != 1:
        #         A[k, k:c] /= A[k, l]
        #         cols.append(l)

        # Back Substitution Process
        R = len(cols)  # rank(A)
        for l in cols[-1:0:-1]:
            if any(A[1:R-1, l] != 0):
                if l<c:
                    A[1:R-1, l+1:c] -= A[1:R-1, l]*A[R, l+1:c]
                A[1:R-1, l] = 0
            R -= 1
        return A, cols

    def argmin(self, findall=False):
        '''find the minimum of matrix and the index
        set findall=True if you want to find all indexes of minimum'''
        m, n=self.shape
        if not findall:
            minelm=self[1]; ind = (1,1)
            for k in range(1,1+m):
                for l in range(1,1+n):
                    temp = self[k,l]
                    if temp < minelm:
                        minelm = temp
                        ind = (k,l)
            return minelm, ind
        else:
            minelm=self[1]; ind = [(1,1)]
            for l in range(2,1+n):
                temp = self[1,l]
                if temp < minelm:
                    minelm = temp
                    ind = [(1,l)]
                elif temp == minelm:
                    ind.append((1,l))
            for k in range(2,1+m):
                for l in range(1,1+n):
                    temp = self[k,l]
                    if temp < minelm:
                        minelm = temp
                        ind = [(k,l)]
                    elif temp == minelm:
                        ind.append((k,l))
            return minelm, ind

    def argmax(self, findall=False):
        '''see argmin'''
        a, ind = (-self).argmin(findall=findall)
        a = -a
        return a, ind


# functions and special matrices
def compind(ind, N):
    # complementary index
    if isinstance(ind, int):
        return list(range(1,ind))+list(range(ind+1, N+1))
    elif isinstance(ind, list):
        return [k for k in range(1, N+1) if k not in ind]
    elif isinstance(ind, slice):
        if ind.step is None or ind.step==1:
            if ind.stop is None:
                return [] if ind.start is None else list(range(1, ind.start))
            if ind.start is None:
                return list(range(ind.stop+1, N+1))
            if ind.start <= ind.stop:
                return list(range(1, ind.start))+list(range(ind.stop+1, N+1))
            else:
                COLON
        elif ind.step == -1:
            if ind.stop is None:
                return [] if ind.start is None else list(range(ind.start+1, N+1))
            if ind.start is None:
                return list(range(1, ind.stop))
            if ind.start >= ind.stop:
                return list(range(1, ind.stop)) + list(range(ind.start+1, N+1))
            else:
                return COLON
        else:
            return [k for k in range(1, N+1) if k not in ind2iter(ind, N)]

# matrix instance

# im = MyMat([[0, 1], [-1, 0]])
def E(i, j, m, n=None, dtype=np.int32):
    if n is None: n = m
    A = O(m,n)
    A[i,j] = 1
    return A

def H(m, n=None):
    # Hilbert matrix
    if n is None:
        n = m
    return MyMat([[1 / (k + l - 1) for l in range(1, n+1)] for k in range(1, m+1)])


def TestMat(m, n=None, dtype=np.int32):
    # for testing
    if n is None:
        n = m
    return MyMat([[l + k*n for l in range(1, n+1)] for k in range(m)], dtype=np.int32)


def Ho(w):
    # Householder matrix
    # w.norm(2)==1, w is column vector
    w=MyMat(w)
    if w.norm(2)!=1: w /= w.norm(2)
    if w.isrowvec():
        return I(w.size) - 2*w.T*w
    else:
        return I(w.size) - 2*w*w.T

def Ref(x, y):
    # Reflection matrix
    # ||x|| == ||y||, x != y
    x=MyMat(x); y=MyMat(y)
    w=(x-y)/(x-y).norm()
    return Ho(w)

def Elm1(i, j, m):
    A = I(m)
    A[i,i]=0
    A[j,j]=0
    A[i,j]=1
    A[j,i]=1

def Elm2(i, k, m):
    # k != 0
    A = I(m)
    A[i,i]=k

def Elm3(i,j,k,m):
    # i != j
    A=I(m)
    A[i,j]=m

def Compl(a=0, b=0):
    # linear represenation of complex number
    return MyMat([[a, b], [-b, a]])

def Quat(a=0, b=0, c=0, d=0):
    # linear represenation of quaternions
    return MyMat([[a, b, c, d], [-b, a, -d, c], [-c, d, a, -b], [-d, -c, b, a]])


def FM(N=1):
    # Fourier matrix
    A = MyMat(range(N))
    return np.exp(np.pi*2j/N*A.T*A)

def FIM(N=1):
    # Fourier inverse matrix
    A = MyMat(range(N))
    return np.exp(np.pi*-2j/N*A.T*A)/N

def FUM(N=1):
    # Fourier unitary matrix
    A = MyMat(range(N))
    return np.exp(np.pi*2j/N*A.T*A)/np.sqrt(N)

def FFM(d, N=1):
    # Fourier frame matrix
    A = MyMat(range(N))
    return np.exp(np.pi*2j/N*A.T[:d]*A)/np.sqrt(N)


class PyMat(BaseMatrix):
    # python for imitating matrices (2D) in matlab
    # matrix on complex numbers
    index_type = 'python'

    def __new__(cls, data, *args, **kw):
        if isinstance(data, PyMat):
            return data
        elif isinstance(data, BaseMatrix):
            data = np.array(data)
        return super(PyMat, cls).__new__(cls, data, *args, **kw)


# helpers
def split2(s, ch1='[;\\\\]',ch2='[,&]'):
    '''double split: string to matrix (list of lists)
'''
    import re
    rx1 = re.compile(ch1)
    lst = rx1.split(s.strip())
    rx2 = re.compile(ch2)
    return [[ss.strip() for ss in rx2.split(s.strip())] for s in lst]


# equation class
class LinearEquation(object):
    '''LinearEquation: Ax=b
    A: coefficient matrix
    b: b'''
    def __init__(self, A, b):
        self.A = MyMat(A)
        self.b = MyMat(b)

    def __str__(self):
        form = '_%d'
        r, c = self.A.shape
        eq = []
        for k in range(r):
            row=[]
            for l in range(c):
                elem = super(BaseMatrix, self.A).__getitem__((k, l))
                if elem == 1:
                    row.append("+ x" + form%(l+1))
                elif elem == -1:
                    row.append("- x" + form%(l+1))
                elif elem>0:
                    row.append('+ ' + str(elem)+"x" + form%(l+1))
                elif elem<0:
                    row.append('- ' + str(abs(elem)) + "x" + form%(l+1))
                # elif elem == 0:
                #     row.append("0")
                else:
                    pass
            eq.append(' '.join(row).lstrip('+ ') + '=%s '%str(super(BaseMatrix, self.b).__getitem__(k)))
        return '\n'.join(eq)

    def solve(self):
        return np.linalg.solve(self.A, self.b.toarray())

    def jacobiIter(self):
        form = '_{%d}'
        r, c = self.A.shape
        eq = []
        for k in range(r):
            row = [str(super(BaseMatrix, self.b).__getitem__(k))]
            for l in range(c):
                if l != k:
                    elem = -super(BaseMatrix, self.A).__getitem__((k, l))
                    if elem == 1:
                        row.append("+ x^{(k)}" + form%(l+1))
                    elif elem == -1:
                        row.append("- x^{(k)}" + form%(l+1))
                    elif elem>0:
                        row.append('+ ' + str(elem) + "x^{(k)}" + form%(l+1))
                    elif elem<0:
                        row.append('- ' + str(abs(elem)) + "x^{(k)}" + form%(l+1))
                    # elif elem == 0:
                    #     row.append("0")
                    else:
                        pass
            eq.append("x^{(k+1)}" + form%(k+1) + '= %s('%str(1/super(BaseMatrix, self.A).__getitem__((k,k))) + ' '.join(row).lstrip('+ ') + ')\\\\')
        return '\\left\\{\\begin{array}{ll}\n%s\n\\end{array}\\right.'%'\n'.join(eq)


    def totex(self):
        form = '_{%d}'
        r, c = self.A.shape
        eq = []
        for k in range(1, r+1):
            row=[]
            for l in range(1, c+1):
                elem = self.A[k,l]
                if elem == 1:
                    row.append("+ x" + form%(l))
                elif elem == -1:
                    row.append("- x" + form%(l))
                elif elem > 0:
                    row.append('+ ' + str(elem) + "x" + form%(l))
                elif elem < 0:
                    row.append('- ' + str(abs(elem)) + "x" + form%(l))
                # elif elem == 0:
                #     row.append("0")
                else:
                    pass
            eq.append(' '.join(row).lstrip('+ ') + '& =%s \\\\'%str(self.b[k]))
        return '\\left\\{\\begin{array}{rl}\n%s\n\\end{array}\\right.'%'\n'.join(eq)
