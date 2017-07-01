import numpy as np

def factorial_list(n):
    """Return a list of factorials

    Arguments
    ---------
    n : int
        maximum index of factorial list

    Returns
    -------
    numpy array with shape (``n+1``,1) and dtype ``int``
        list of factorials :math:`0!, \\ldots, n!`
    """
    seq = np.empty(n + 1, dtype=int)
    seq[0] = 1
    for i in range(1, n + 1):
        seq[i] = seq[i - 1] * i
    return seq


def simplicial_list(n, k):
    """
    Return a list of simplicial numbers

    The simplicial number :math:`{n+j-1 \\choose j}` is the number of :math:`j^{th}` degree partial derivatives of a function :math:`f` with domain of dimension :math:`n`.

    Arguments
    ---------
    n : int
        dimension of domain of :math:`f`
    k : int
        maximum derivative degree

    Returns
    -------
    numpy array with shape (``k+1``,1) and dtype ``int``
        list containing :math:`{n+j-1 \\choose j}` for :math:`j=0,\\ldots,k`
    """
    seq = np.empty(k + 1, dtype=int)
    seq[0] = 1
    for i in range(1, k + 1):
        seq[i] = seq[i - 1] * (n + i - 1) / i
    return seq
