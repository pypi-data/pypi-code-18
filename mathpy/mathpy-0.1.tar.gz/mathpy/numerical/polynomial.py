# encoding=utf8


"""
Module containing functions for evaluating polynomials.

"""

from sympy import symbols, Poly


def horner_eval(f, x0):
    r"""
    Evaulates a polynomial function using Horner's method.

    Parameters
    ----------
    f : function
        The polynomial function to be evaluated. For example, to evaluate the
        polynomial :math:`f(x) = 3x^3 - 5x^2 + 2x - 1`, f should be similar to:

        .. code-block:: python

            def f(x):
                # The variable in function f must be set as x.
                return 3 * x^3 - 5 * x^2 + 2 * x - 1

    x0 : int, float
        The point at which to evaluate the function f.

    Returns
    -------
    poly_eval : int or float
        The evaluated polynomial function f at the given point x0.

    Notes
    -----
    Given a polynomial, such as:

    .. math [1]

        a_0 + a_1 x + a_2 x^2 + a_3 x^3 + \cdots + a_n x^n

    Horner's method evaluates the polynomial at a given point, such
    as :math:`x_0` by converting the polynomial into a 'nested'
    form by defining a new sequence. This is done by starting with the
    leading coefficient :math:`a_n`, multiplying it :math:`x` and adding
    the next coefficient. For example, using Horner's method to evaluate
    the polynomial :math:`f(x) = 3x^3 - 5x^2 + 2x - 1`, at :math:`x = 3`
    Horner's method proceeds as follows:

    .. math::

        b_3 = 3

    .. math::

        b_2 = 3x - 5 = 3(3) - 5 = 4

    .. math::

        b_1 = (4)x + 2 = (4)(3) + 2 = 14

    .. math::

        b_0 = (14)x - 1 = (14)(3) - 1 = 41

    Examples
    --------
    >>> def f(x): return 3 * x ** 3 - 5 * x ** 2 + 2 * x - 1
    >>> horner_eval(f, 3)
    41
    >>> def f2(x): return 4 * x ** 4 - 6 * x ** 3 + 3 * x - 5
    >>> horner_eval(f2, 10)
    34025

    References
    ----------
    Cormen, T., Leiserson, C., Rivest, R., & Stein, C. (2009).
        Introduction to algorithms (3rd ed.). Cambridge (Inglaterra): Mit Press.

    Horner's method. (2017, April 12). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Horner%27s_method&oldid=775072621

    """
    if callable(f) is False:
        raise TypeError('f must be a function')

    x = symbols('x')
    fx_coefs = Poly(f(x), x).all_coeffs()

    poly_eval = 0
    for i in fx_coefs:
        poly_eval = poly_eval * x0 + i

    return poly_eval
