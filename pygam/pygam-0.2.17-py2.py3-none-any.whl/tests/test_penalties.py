# -*- coding: utf-8 -*-

import numpy as np
import pytest

from pygam import *

from pygam.penalties import derivative
from pygam.penalties import l2
from pygam.penalties import monotonic_inc
from pygam.penalties import monotonic_dec
from pygam.penalties import convex
from pygam.penalties import concave
from pygam.penalties import circular
from pygam.penalties import none
from pygam.penalties import wrap_penalty

from pygam.utils import generate_X_grid


def test_single_spline_penalty():
    """
    check that feature functions with only 1 basis are penalized correctly

    derivative penalty should be 0.
    l2 should penalty be 1.
    monotonic_ and convexity_ should be 0.
    """
    coef = np.array(1.)
    assert(np.alltrue(derivative(1, coef).A == 0.))
    assert(np.alltrue(l2(1, coef).A == 1.))
    assert(np.alltrue(monotonic_inc(1, coef).A == 0.))
    assert(np.alltrue(monotonic_dec(1, coef).A == 0.))
    assert(np.alltrue(convex(1, coef).A == 0.))
    assert(np.alltrue(concave(1, coef).A == 0.))
    assert(np.alltrue(circular(1, coef).A == 0.))
    assert(np.alltrue(none(1, coef).A == 0.))

def test_wrap_penalty():
    """
    check that wrap penalty indeed reduces inserts the desired penalty into the
    linear term when fit_linear is True, and 0, when fit_linear is False.
    """
    coef = np.array(1.)
    n = 2
    linear_penalty = -1

    fit_linear = True
    p = wrap_penalty(none, fit_linear, linear_penalty=linear_penalty)
    P = p(n, coef).A
    assert(P.sum() == linear_penalty)

    fit_linear = False
    p = wrap_penalty(none, fit_linear, linear_penalty=linear_penalty)
    P = p(n, coef).A
    assert(P.sum() == 0.)

def test_monotonic_inc(hepatitis):
    """
    check that monotonic_inc constraint produces monotonic increasing function
    """
    X, y = hepatitis

    gam = LinearGAM(constraints='monotonic_inc')
    gam.fit(X, y)

    XX = generate_X_grid(gam)
    Y = gam.predict(np.sort(XX))
    diffs = np.diff(Y, n=1)
    assert(((diffs >= 0) + np.isclose(diffs, 0.)).all())

def test_monotonic_dec(hepatitis):
    """
    check that monotonic_dec constraint produces monotonic decreasing function
    """
    X, y = hepatitis

    gam = LinearGAM(constraints='monotonic_dec')
    gam.fit(X, y)

    XX = generate_X_grid(gam)
    Y = gam.predict(np.sort(XX))
    diffs = np.diff(Y, n=1)
    assert(((diffs <= 0) + np.isclose(diffs, 0.)).all())

def test_convex(hepatitis):
    """
    check that convex constraint produces convex function
    """
    X, y = hepatitis

    gam = LinearGAM(constraints='convex')
    gam.fit(X, y)

    XX = generate_X_grid(gam)
    Y = gam.predict(np.sort(XX))
    diffs = np.diff(Y, n=2)
    assert(((diffs >= 0) + np.isclose(diffs, 0.)).all())

def test_concave(hepatitis):
    """
    check that concave constraint produces concave function
    """
    X, y = hepatitis

    gam = LinearGAM(constraints='concave')
    gam.fit(X, y)

    XX = generate_X_grid(gam)
    Y = gam.predict(np.sort(XX))
    diffs = np.diff(Y, n=2)
    assert(((diffs <= 0) + np.isclose(diffs, 0.)).all())


# TODO penalties gives expected matrix structure
# TODO circular constraints
