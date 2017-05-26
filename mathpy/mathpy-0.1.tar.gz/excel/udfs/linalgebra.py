#encoding=utf8

"""

MATRIX DECOMPOSITION

"""

from mathpy.linalgebra import lu, matrix, norm, qr

import numpy as np
import xlwings as xw


@xw.func
@xw.arg('x', np.array, doc='Input array. Must be a square, symmetric, positive-definite '
                           'matrix to perform Cholesky decomposition')
@xw.ret(expand='table')
def CHOLESKY(x):
    r"""
    Factors a symmetric, positive definite matrix into the product of the matrix L and its transpose, LL^T

    Parameters
    ----------
    x
        Continuous range of cells representing matrix to be decomposed

    Returns
    -------
    array-like
        The products L and its transpose L^T are output side by side, respectively.

    See Also
    --------
    cholesky : function
        Function used to calculate the matrix products L and L^T

    """
    return np.hstack(lu.cholesky(x))


"""
LU Decomposition
"""

@xw.func
@xw.arg('x', doc='Input array. Must be square to perform LU decompostion')
@xw.ret(expand='table')
def LU(x):
    r"""
    Factors a square matrix into the product of a lower-triangular matrix, :math:`L`,
    and an upper-triangular matrix, :math:`U`.

    Parameters
    ----------
    x
        Continuous range of cells representing matrix to be decomposed

    Returns
    -------
    array-like
        The products L and U are output side by side, respectively.

    See Also
    --------
    lu : function
        Function used to compute the LU decomposition.

    """
    return np.hstack(lu.lu(x))

"""
QR Decomposition
"""


@xw.func
@xw.arg('x', np.array, doc='Input array.')
@xw.ret(expand='table')
def QRDECOMP(x):
    """
    Factors an m x n matrix into the product of an orthogonal matrix Q and an upper-triangular matrix R, QR

    Parameters
    ----------
    x
        Continuous range of cells representing matrix to be decomposed

    Returns
    -------
    array-like
        The factorized products Q and R are output side by side

    See Also
    --------
    qr : function
        Function used to calculate the QR decomposition of the matrix

    """
    return np.hstack(qr.qr(x))


"""

MATRIX TEST METHODS

"""

"""
Matrix isorthogonal
"""


@xw.func
@xw.arg('x', np.array, doc='Input array. An orthogonal matrix is equal to its identity when multiplied by its '
                           'tranpose, AA^T = I. Orthogonal matrices are also invertible, A^-1 = A^T')
def ISORTHOGONAL(x):
    """
    Checks if the supplied matrix is orthogonal.

    Parameters
    ----------
    x : Continuous range of cells representing matrix to be decomposed

    Returns
    -------
    Boolean
        TRUE if the matrix is orthogonal, FALSE otherwise

    See Also
    --------
    isorthogonal : function
        Backend function that checks if a matrix is orthogonal

    """

    return matrix.isorthogonal(x)

"""
Matrix issymmetric
"""


@xw.func
@xw.arg('x', np.array, doc='Input array. A symmetric matrix is always square.')
def ISSYMMETRIC(x):
    """
    Checks if the supplied matrix is symmetric

    Parameters
    ----------
    x : Continuous range of cells representing matrix to be decomposed

    Returns
    -------
    Boolean
        TRUE if the matrix is symmetric, FALSE otherwise

    See Also
    --------
    issymmetric : function
        Backend function that determines if the matrix is symmetric

    """
    return matrix.issymmetric(x)


"""
Matrix isskewsymmetric
"""


@xw.func
@xw.arg('x', np.array, doc='Input array. A skew symmetric matrix is always square with 0s on the diagonal.')
def ISSKEWSYMMETRIC(x):
    """
    Checks if the matrix is skew-symmetric

    Parameters
    ----------
    x : Continuous range of cells representing matrix to be decomposed

    Returns
    -------
    Boolean
        TRUE if the matrix is skew-symmetric, FALSE otherwise

    See Also
    --------
    isskewsymmetric : function
        Backend function that determines if the matrix is skew-symmetric

    """
    return matrix.isskewsymmetric(x)


"""
Matrix ispositivedefinite
"""


@xw.func
@xw.arg('x', np.array, doc='Input array. A positive definite matrix is also symmetric.')
def ISPOSITIVEDEFINITE(x):
    """
    Checks if the matrix is positive definite

    Parameters
    ----------
    x : Continuous range of cells representing matrix to be decomposed

    Returns
    -------
    Boolean
        TRUE if the matrix is positive definite, FALSE otherwise

    See Also
    --------
    ispositivedefinite : function
        Backend function that determines if the matrix is positive definite

    """
    return matrix.ispositivedefinite(x)


"""
Matrix ispositivesemidefinite
"""


@xw.func
@xw.arg('x', np.array, doc='Input array. A positive definite matrix is also semi-positive definite.')
def ISPOSITIVESEMIDEFINITE(x):
    """
    Checks if the matrix is positive semi-definite

    Parameters
    ----------
    x : Continuous range of cells representing matrix to be decomposed

    Returns
    -------
    Boolean
        TRUE if the matrix is positive semi-definite, FALSE otherwise

    See Also
    --------
    ispositivesemidefinite : function
        Backend function that determines if the matrix is positive semi-definite

    """
    return matrix.ispositivesemidefinite(x)


"""
Matrix isnegativedefinite
"""


@xw.func
@xw.arg('x', np.array, doc='Input array. A negative definite matrix has all negative eigenvalues')
def ISNEGATIVEDEFINITE(x):
    """
    Checks if the matrix is negative definite

    Parameters
    ----------
    x : Continuous range of cells representing matrix to be decomposed

    Returns
    -------
    Boolean
        TRUE if the matrix is negative definite, FALSE otherwise

    See Also
    --------
    isnegativedefinite : function
        Backend function that determines if the matrix is negative definite

    """
    return matrix.isnegativedefinite(x)


"""
Matrix isnegativesemidefinite
"""


@xw.func
@xw.arg('x', np.array, doc='Input array. A negative semi-definite matrix is also negative definite')
def ISNEGATIVESEMIDEFINITE(x):
    """
    Checks if the matrix is negative semi-definite

    Parameters
    ----------
    x : Continuous range of cells representing matrix to be decomposed

    Returns
    -------
    Boolean
        TRUE if the matrix is negative semi-definite, FALSE otherwise

    See Also
    --------
    isnegativesemidefinite : function
        Backend function that determines if the matrix is negative semi-definite

    """
    return matrix.isnegativesemidefinite(x)


"""
Matrix isindefinite
"""


@xw.func
@xw.arg('x', np.array, doc='Input array. An indefinite matrix is neither positive or negative definite '
                           '(or semi-definite for either case).')
def ISINDEFINITE(x):
    """
    Checks if the matrix is indefinite

    Parameters
    ----------
    x : Continuous range of cells representing matrix to be decomposed

    Returns
    -------
    Boolean
        TRUE if the matrix is indefinite, FALSE otherwise

    See Also
    --------
    isindefinite : function
        Backend function that determines if the matrix is indefinite

    """
    return matrix.isindefinite(x)


"""
VECTOR AND MATRIX NORMS
"""


@xw.func
@xw.arg('x', np.array, doc='Input vector or matrix. If the input is one-dimensional (vector), the vector norm is '
                           'calculated. If the input is two-dimensional (matrix), the matrix norm is returned.')
@xw.arg('order', doc='Optional. Determines which vector or matrix norm to calculate. Defaults to the 2-norm for '
                     'vectors and the Frobenius norm for matrices.')
@xw.arg('p', doc='Optional. Sets the order of p when calculating the p-norm of a vector.')
def NORM(x, order=None, p=None):
    """
    If the input is one-dimensional (vector), the vector norm is calculated. If the input is two-dimensional
    (matrix), the matrix norm is returned.

    Parameters
    ----------
    x : Continuous range of cells representing the vector or matrix

    order : string
        Optional. Determines which norm is calculated

    p : int
        Optional. If `order` is 'p', this value determines the order of the p-norm to calculate

    Returns
    -------
    norm : float
        The computed vector or matrix norm

    See Also
    --------
    norm : function
        mathpy function used to compute the norm of the supplied vector or matrix

    """
    return norm.norm(x, order, p)


"""
MATRIX MULTIPLICATION
"""


@xw.func
@xw.arg('a', np.array, doc='First matrix')
@xw.arg('b', np.array, doc='Second matrix')
@xw.ret(expand='table')
def DOT(a, b):

    return np.dot(a, b)


"""
EIGENVALUES AND EIGENVECTORS
"""

@xw.func
@xw.arg('a', np.array)
@xw.ret(expand='table')
def EIGEN(a):

    return np.hstack(np.linalg.eig(a))
