'''
This is my module about matrix operation. It imitates matlab grammar.
If you love matlab as well as python, then this is your choice.
It will be a good experience to operating matrices matlab-like.

--------------------------------------------------------------

Grammar:

    >>> import mymat
    >>> A = mymat.MyMat([])
    # use import mymat.pymat to import PyMat

    MyMat (= MMat) imitates the expression of matlab: (Python left, Matlab right)
        A*B := A*B  (B*A := B*A)
        A/B := A/B == A*B.I (B/A := B/A == B*A.I)
        A**B := A.*B  (B**A := B.*A)
        A//B := A./B  (B//A := B./A)
        A<<B := A.^B  (B<<A := B.^A)
        A^B := A^B
        A|B := [A,B]   A&B :=[A;B]

    >>> A=TestMat(5)
    >>> A
    matrix([[ 1,  2,  3,  4,  5],
            [ 6,  7,  8,  9, 10],
            [11, 12, 13, 14, 15],
            [16, 17, 18, 19, 20],
            [21, 22, 23, 24, 25]])
    >>> A[[3,4,7,10]]    # with single index as in matlab
    matrix([[11, 16,  7, 22]])
    >>> A[[2,3],1:4]
    matrix([[ 6,  7,  8,  9],
            [11, 12, 13, 14]])
    >>> A[[1,3],[2,4]]   # use A.get(([1,3],[2,4])) to get matrix([2, 14])
    matrix([[ 2,  4],
            [12, 14]])

    >>> A[3:1:-1,:]     # reversing order
    matrix([[11, 12, 13, 14, 15],
            [ 6,  7,  8,  9, 10],
            [ 1,  2,  3,  4,  5]])

    If you want to delete several rows or columns, then use delete method or just
    A[k,:]=[] as in matlab. A(k,:)=[] (in matlab) <=> A.delete(k,[]) (in Python)


other methods:
    __call__: A(ind) == A[ind]
    delete(ind1=row, ind2=col): delete row-rows and col-columns
    proj(ind1=row, ind2=col): =0 out of A[row, col], for example A.proj(ind1=COLON, ind2=[2,3])=[2,3] where A=[1,2,3,4]
    repmat((ind1, ind2)|ind): repeat matrix as in Matlab (like tile)
    just: cut matrix to a certain size, and supplement zeros if the size is too large.
    cat: as concatenate
    equal: (A == B == C).all()
    apply: A.apply(lambda x:x+1) == A+1
    plus: A.plus(n) == A + nI
    robinson: A.robinson(j, x) == A[j<-x], namely A[:,j]=x used in Cramer rule
    echelon: get the echelon form (include the corresponding column indexes)
    tril, triu, diag are similar to matlab
    rowtrans1/2/3: elementary row transforms (Gauss tranforms)
    comat: get the co-matrix (similar with delete)
    cofactor: A.cofactor(i,j)=Aij get the cofactor based on comat
    rho: the spectral radius
    tofrac: convert to matrix of fractions.Fraction

functions:
    fun2mat: generate MyMat{f(i,j)}
    ind2ind: the most essential function
    split2: 2-level version of split transforming a string to a matrix with two seperators

varibles:
    COLON = slice(None), COLON2=(COLON, COLON)

matrices:
    FM: Fourier matrix
    FIM: Fourier inverse matrix
    FUM: Fourier unitary matrix
    Ho: Householder matrix
    Ref: reflection matrix
    H: Hilbert matrix
    Elm1,Elm2,Elm3: elementary matrices
'''

from mymat.mymat import *
