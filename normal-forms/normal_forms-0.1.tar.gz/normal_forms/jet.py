import numpy as np
import sympy
import combinatorics
from multiindex import multiindex


class jet(object):
    """truncated Taylor's series

    The jet is represented in both an expanded and closed form. The closed form is :math:`\\sum_{0\\leq d\\leq k}` ``coeff[deg]*basis[deg]``, where :math:`d` is ``deg``, while the expanded form is the list of numpy arrays ``coeff`` each with shape :math:`(m,{n+d-1 \\choose d})` and the list of column vectors ``basis``. ``coeff[deg][i,j]`` is the :math:`d^{th}` derivative of :math:`f_i` with respect to the :math:`j^{th}` multiindex divided by the multiindex factorial and ``basis[deg]`` is of the form :math:`\\begin{bmatrix}(x_1-x^{(1)})^d & (x_1-x^{(1)})^{d-1}(x_2-x^{(2)}) & \\cdots& (x_n-x^{(n)})^{d} \\end{bmatrix}^T` where ``x`` :math:`=\\begin{bmatrix} x^{(1)} &\\cdots& x^{(n)}\\end{bmatrix}^T`.

    Arguments
    ---------
    f : callable
        function that accepts ``n`` arguments and returns tuple of length ``m`` numbers, corresponding to mathematical function :math:`f:\\mathbb{R}^n\\rightarrow\\mathbb{R}^m`
    x : number (if ``n==1``) or iterable  (if ``n>=1``)
        center about which jet is expanded
    k : int
        maximum degree of jet

    Attributes
    ----------
    m : int
        number of output numbers, dimension of range of :math:`f`
    n : int
        number of input arguments, dimension of domain of :math:`f`
    var : tuple of Sympy variables
        ``x1``, ``x2``, ..., ``xn`` representing input variables
    coeff : tuple of numpy arrays
        jet coefficients indexed as ``coeff[deg][coord,term]`` where :math:`0\leq` ``deg`` :math:`\leq k`, :math:`0\leq` ``coord`` :math:`\leq m`, and :math:`0\leq` ``term`` :math:`<{m-1+d \\choose d}` and :math:`d` is ``deg``
    basis : tuple of Sympy Matrices
        monomial basis elements :math:`\\prod_{i\\in S}` ``xi-x[i-1]`` where :math:`S` is a set in the power set of :math:`\\{1,\\ldots,n\\}` and :math:`|S|\\leq k` indexed as ``basis[deg][term]``
    series : Sympy Matrix
        Sympy Matrix with shape (``m``,1), symbolic representation of jet
    series_lam : callable
        lambdified version of series
    """

    def __init__(self, f, x, k):
        """initialize the jet"""
        self.f = f
        self.x = x
        self.k = k
        if np.array(x).shape == ():
            n, x = 1, [x]
        else:
            n = len(x)
        if np.array(f(*x)).shape == ():
            m = 1
        else:
            m = len(f(*x))
        self.m = m
        self.n = n

        # create list of n symbols
        var = sympy.symbols('x1:%i' % (n + 1, ))
        self.var = var

        # compute number of terms per degree in expanded form sum(coeff[:,deg]*basis[deg])
        n_terms = combinatorics.simplicial_list(n, k)

        # compute coeff and basis element vectors of expanded form
        coeff = [np.empty([m, n_terms[deg]]) for deg in range(k + 1)]
        basis = [sympy.ones(n_terms[deg], 1) for deg in range(k + 1)]
        coeff[0][:, 0] = list(sympy.Matrix([f(*var)]).subs(zip(var, x)))
        for deg in range(1, k + 1):
            m_idx = multiindex(deg, n)
            for term in range(n_terms[deg]):
                coeff[deg][:, term] = list(
                    sympy.diff(sympy.Matrix([f(*var)]), *m_idx.to_var(var))
                    .subs(zip(var, x)) / m_idx.factorial())
                basis[deg][term] = m_idx.to_polynomial(var, x)
                m_idx.increment()
        self.coeff = coeff
        self.basis = basis

        # compute series and simplify
        series = sympy.zeros(m, 1)
        for deg in range(k + 1):
            series += sympy.Matrix(coeff[deg]) * basis[deg]
        series.simplify()
        self.series = series

        # lambdify series
        self.series_lam = sympy.lambdify(var, list(series))

    def __call__(self, *args):
        """evaluate the jet"""
        res = self.series_lam(*args)
        if len(res) == 1:
            res = res[0]
        return res
