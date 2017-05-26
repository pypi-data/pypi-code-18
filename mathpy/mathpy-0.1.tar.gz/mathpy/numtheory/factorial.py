# encoding=utf8


"""
Module containing functions for calculating or approximating factorials.

"""

import numpy as np
from decimal import Decimal, localcontext


def factorial(n, prec=100):
    r"""
    Function for calculating factorials using the standard approach as explained in the
    Notes section. For factorials over 100, the decimal package is used to support the
    resulting large integers.

    Parameters
    ----------
    n : int
        The desired integer to calculate the factorial.
    prec : int default 100, optional
        Defines level of precision for factorials over 100
        for use by the decimal package

    Returns
    -------
    f : int or float
        The computed factorial of the given integer.

    Notes
    -----
    Factorials are denoted for a positive integer :math:`x` as :math:`x!` and are
    defined as:

    .. math::

        x! = (x)(x - 1) \cdots (2)(1)

    For example, the factorial of 5 is written as:

    .. math::

        5! = (5)(4)(3)(2)(1) = 120

    Examples
    --------
    >>> factorial(10)
    3628800.0
    >>> factorial(50)
    3.0414093201713376e+64
    # Factorials above 100 use the decimal package to handle the resulting large integers
    >>> factorial(200)
    Decimal('7.886578673647905035523632139321850622951359776871732632947425332443594499634033429203042840119846238E+374')

    References
    ----------
    Press, W., Teukolsky, S., Vetterling, W., & Flannery, B. (2007). Numerical recipes (3rd ed.).
        Cambridge: Cambridge University Press.

    Weisstein, Eric W. "Factorial." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/Factorial.html

    """
    factor = np.arange(1, n + 1)

    if n > 100:
        with localcontext() as ctx:
            ctx.prec = prec
            f = Decimal(1)
            for i in reversed(factor):
                f = Decimal(f) * i
    else:
        f = float(1)
        for i in reversed(factor):
            f = f * i

    return f


def stirlingln(n, keep_log=False, prec=100):
    r"""
    Approximates the factorial of n using the approximation
    given by Ramanujan in his lost notebook (Ramanujan 1988,
    as cited in Wikipedia). Computing the factorial in logarithmic
    form is useful as it helps avoid overflow when n is large. As
    values of n increase, the approximation given becomes more
    exact.

    Parameters
    ----------
    n : int
        The desired integer to calculate the factorial.
    keep_log : bool default False
        If True, the approximation remains in logarithmic
        form. If False, converts to exponent form before
        returning the factorial approximation.
    prec : int default 100, optional
        Defines level of precision for factorials over 100.

    Returns
    -------
    f : int or float
        The computed log factorial of the given integer.

    Notes
    -----
    It is often useful to compute the logarithmic form of the
    factorial and convert it to exponent form to avoid overflow.
    The approximation is an alternative approach given by
    Srinivasa Ramanujan (Ramanujan 1988).

    .. math::

        ln n! \approx n ln n - n + \frac{1}{6} ln(n(1 + 4n(1 + 2n))) + \frac{1}{2} ln \pi

    Examples
    --------
    # Difference between actual factorial calculation and Stirling's Approximation
    # for low values of n is practically zero
    >>> (factorial(5) - stirlingln(5)) / stirlingln(5)
    3.8020354295010749e-06
    >>> stirlingln(50)
    3.041409303897981e+64
    >>> stirlingln(100)
    9.3326215380340829e+157
    # If the keep_log flag is set to True, the output remains in logarithmic form.
    >>> stirlingln(100, True)
    363.73937555488197

    References
    ----------
    Stirling's approximation. (2017, March 8). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Stirling%27s_approximation&oldid=769328178

    """
    n = float(n)
    if n > 100:
        with localcontext() as ctx:
            ctx.prec = prec
            f = Decimal(n * np.log(n) - n + (1. / 6.) * np.log(n * (1. + 4. * n * (1. + 2. * n))) + .5 * np.log(np.pi))
    else:
        f = n * np.log(n) - n + (1. / 6.) * np.log(n * (1. + 4. * n * (1. + 2. * n))) + .5 * np.log(np.pi)

    if keep_log is False:
        return np.exp(f)

    return f


def stirling(n, prec=100):
    r"""
    Approximates a factorial n using Stirling's Approximation. Specifically, the approximation is done
    using a method developed by [2]Gosper.

    Parameters
    ----------
    n : int
        The desired integer to calculate the factorial.
    prec : int default 100, optional
        Defines level of precision for factorials over 100
        for use by the decimal package

    Returns
    -------
    f : int or float
        The computed factorial of the given integer.

    Notes
    -----
    Stirling's approximation is a method of approximating a factorial :math:`n!`.
    As the value of :math:`n` increases, the more exact the approximation becomes;
    however, it still yields almost exact results for small values of :math:`n`.

    The approximation used is given by Gosper [2], which is noted to be a better
    approximation to :math:`n!` and also results in a very close approximation to
    :math:`0! = 1`.

    .. math::

        n! \approx \sqrt{(2n + \frac{1}{3})\pi} n^n e^{-n}

    Examples
    --------
    >>> stirling(0)
    1.0233267079464885

    # Difference between actual factorial and Stirling's approximation is wider
    # for the non-logarithmic case, but is still rather close to 0.
    >>> (factorial(5) - stirling(5)) / stirling(5)
    0.00024981097589214563

    >>> stirling(5)
    119.9700301696855
    >>> stirling(50)
    3.0414009581300833e+64

    References
    ----------
    Stirling's approximation. (2017, March 8). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Stirling%27s_approximation&oldid=769328178

    Weisstein, Eric W. "Stirling's Approximation." From MathWorld--A Wolfram Web Resource.
        http://mathworld.wolfram.com/StirlingsApproximation.html

    """
    if n >= 100:
        with localcontext() as ctx:
            ctx.prec = prec
            f = Decimal(np.sqrt((2 * n + 1/3) * np.pi) * n ** n * np.exp(-n))
    else:
        f = np.sqrt((2 * n + 1/3) * np.pi) * n ** n * np.exp(-n)

    return f
