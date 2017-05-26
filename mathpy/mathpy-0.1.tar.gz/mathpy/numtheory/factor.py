# encoding=utf8

"""
Methods for factoring integers into products of smaller primes.

"""

import numpy as np


def factor(n):
    """
    Implementation of an integer factorization routine utilizing trial division
    that decomposes an integer :math:`n` into a product of smaller integers. If
    :math:`n` is prime, :math:`n` is returned.

    Parameters
    ----------
    n : int, float
        Integer to be factored into product of smaller integers.

    Returns
    -------
    factors : list
        A list containing the factors of :math:`n` should they exist. If :math:`n`
        is prime, the returned list will only contain :math:`n`.

    Examples
    --------
    >>> factor(4)
    [2.0, 2.0]
    >>> factor(13)
    13
    >>> n = 9.24
    >>> factor(n)
    [3.0, 3.0]

    Notes
    -----
    Integer factorization by trial division is the most inefficient algorithm for decomposing
    a composite number. Trial division is the method of testing if :math:`n` is divisible by
    a smaller number, beginning with 2 and proceeding upwards. This order is used to eliminate
    the need to test for multiples of 2 and 3. Also, the trial factors never need to go further
    than the square root of :math:`n`, :math:`\sqrt{n}`, due to the factorinteger that if :math:`n` has
    a factorinteger, there exists a factorinteger :math:`f \leq \sqrt{n}`.

    References
    ----------
    Trial division. (2017, April 30). In Wikipedia, The Free Encyclopedia.
        From https://en.wikipedia.org/w/index.php?title=Trial_division&oldid=778023614

    """
    if n != np.round(n):
        raise ValueError('n must be an integer to factor')

    if n < 2:
        raise ValueError('n must be at least 2 for a factorinteger to exist.')

    div = 2.0
    factors = []

    while n % div == 0:
        factors.append(div)
        n /= div

    div += 1

    while n > 1 and div <= np.sqrt(n):
        if n % div == 0:
            factors.append(div)
            n /= div
        else:
            div += 2

    if n > 1:
        factors.append(n)

    return factors
