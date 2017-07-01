import numpy as np
import combinatorics


class multiindex(object):
    """a multiindex class

    Attributes
    ----------
    n : int
        number of indices
    idx_max : int
        upper bound, indices can take nonnegative values less than this
    """

    def __init__(self, n, idx_max=None):
        """initialize indices as zeros

        Attributes
        ----------
        n : int
            number of indices
        idx_max : int
            upper bound, indices can take nonnegative values less than this
        """

        self.idx = np.zeros(n, dtype=int)
        self.idx_max = idx_max

    def increment(self):
        """Increment multiindex.

        A 'telephone-book' ordering is used and within the multiindex indices are assumed to be increasing from left to right. For example, the multiindices with length ``n==2`` and with indices less than ``idx_max=3`` are, in increasing order: (0,0), (0,1), (0,2), (1,1), (1,2), (2,2). The next multiindex is cycled back to the first multiindex.
        """

        n_idx = len(self.idx)
        if all(self.idx >= self.idx_max):
            self.idx = np.zeros(n_idx, dtype=int)
        else:
            i = n_idx - 1
            self.idx[i] += 1
            while self.idx[i] == self.idx_max:
                i -= 1
                self.idx[i] += 1
            self.idx[i:] = self.idx[i]

    def to_polynomial(self, var, x):
        """ convert multiindex to corresponding polynomial

        Arguments
        ---------
        var : iterable
            list of Sympy variables ``x1``, ``x2``, ..., ``xn``
        x : iterable
            roots of returned polynomial

        Returns
        -------
        Sympy symbolic expression
            :math:`\\prod_{i=1}^{n}` ``var[i-1]-xi``
        """

        return np.product([var[idx] - x[idx] for idx in self.idx])

    def to_var(self, var):
        """convert multiindex to list of variables

        Arguments
        ---------
        var : iterable
            list of Sympy variables ``x1``, ``x2``, ..., ``xn``

        Returns
        -------
        list of Sympy symbolic expressions
            list of ``var[idx]`` for ``idx`` in ``self.idx``
        """

        return [var[idx] for idx in self.idx]

    def factorial(self):
        """multiindex factorial

        Multiindex factorial is defined as :math:`(\\alpha_1,\\ldots,\\alpha_k)!=\\alpha_1!\cdots \\alpha_k!`. In this implementation, :math:`\\alpha_i` corresponds to the number of occurences of ``i`` in ``self.idx``.

        Returns
        -------
        int
        """

        fac_key = np.zeros(self.idx_max, dtype=int)
        for idx in self.idx:
            fac_key[idx] += 1
        fac = combinatorics.factorial_list(int(np.max(fac_key)))
        return np.product([fac[key] for key in fac_key])
