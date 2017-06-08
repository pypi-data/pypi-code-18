import numpy as np
from scipy import weave
from util_CMB import benchmark
input_mat = np.array( [[10.,3.],[3.,7.]] )
npix= 1000000

def unsafe_cholesky_C(mat):
    """
    Unsafe in the sense we are not checking the positive-definitiveness
    of the matrix. But much faster than the python one.

    Parameters
    ----------
        * mat: 2x2 array, the matrix to invert

    Output
    ----------
        * mat: 2x2 array, the lower triangle (/!\ 01 block is not used)
    """
    ## TODO check that the matrix is positive-definite before!
    c_code = r"""
        int INFO=1;
        char U='U';
        int N = 2;
        dpotrf_( &U, &N, mat, &N, &INFO );
        """
    weave.inline(c_code, ['mat'],headers=["<math.h>",'</Users/julien/Documents/lib/lapack-release/LAPACKE/include/lapacke.h>'])
    return mat

def safe_cholesky_python(mat):
    """
    Safe in the sense we are not checking the positive-definitiveness
    of the matrix. But much slower than the C one.

    Parameters
    ----------
        * mat: 2x2 array, the matrix to invert

    Output
    ----------
        * mat: 2x2 array, the lower triangle
    """
    ## TODO check that the matrix is positive-definite before!
    c_code = r"""
        int INFO=1;
        char U='U';
        int N = 2;
        DPOTRF( &U, &N, mat, &N, &INFO );
        """
    try:
        cho = np.linalg.cholesky(mat).T
    except:
        cho = np.zeros_like(mat)
    return cho

@benchmark
def compute_python(mat_full):
    cho_full = np.array([safe_cholesky_python(mat) for mat in mat_full])

@benchmark
def compute_C(mat_full):
    cho_full = np.array([unsafe_cholesky_C(mat) for mat in mat_full])

## Cholesky decomposition of each blocks
mat_full = [ np.array( [[10.,3.],[3.,7.]] ) for i in range(npix)]
compute_python(mat_full)
compute_C(mat_full)

# c_code=r"""
# int INFO=1;
# char U='U';
# int NN = 2;
# dpotrf_( &U, &NN, input_mat, &NN , &INFO);
# """
# weave.inline(c_code, ['cho', 'N', 'input_mat'],headers=["<math.h>",'</Users/julien/Documents/lib/lapack-release/LAPACKE/include/lapacke.h>'])
# #,type_converters = weave.converters.blitz)
# print input_mat
# input_mat = np.array( [[10.,3.],[3.,7.]] )
# print np.linalg.cholesky(input_mat)
