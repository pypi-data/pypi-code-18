from __future__ import unicode_literals

from numpy.random import RandomState
from numpy.testing import assert_allclose

from glimix_core.link import ProbitLink
from glimix_core.lik import (BernoulliProdLik, BinomialProdLik,
                                 DeltaProdLik, PoissonProdLik)

def test_delta_prod_lik():
    random = RandomState(0)

    lik = DeltaProdLik(ProbitLink())

    assert lik.name == 'Delta'

    lik.outcome = [1, 0, 1]
    assert_allclose(lik.outcome, [1, 0, 1])

    assert lik.sample_size == 3
    assert_allclose(lik.mean([-1, 0, 0.5]), [-1, 0, 0.5])
    assert_allclose(lik.sample([-10, 0, 0.5], random), [-10, 0, 0.5])

def test_bernoulli_prod_lik():
    random = RandomState(0)

    lik = BernoulliProdLik(ProbitLink())

    assert lik.name == 'Bernoulli'

    lik.outcome = [1, 0, 1]
    assert_allclose(lik.outcome, [1, 0, 1])

    assert lik.sample_size == 3
    assert_allclose(lik.mean([-1, 0, 0.5]), [0.15865525, 0.5, 0.69146246])
    assert_allclose(lik.sample([-10, 0, 0.5], random), [0, 1, 1])

def test_binomial_prod_lik():
    random = RandomState(0)

    lik = BinomialProdLik([6, 2, 3], ProbitLink())
    assert_allclose(lik.ntrials, [6, 2, 3])

    assert lik.name == 'Binomial'

    lik.nsuccesses = [4, 0, 1]
    assert_allclose(lik.nsuccesses, [4, 0, 1])

    assert lik.sample_size == 3
    assert_allclose(lik.mean([-1, 0, 0.5]), [0.15865525, 0.5, 0.69146246])
    assert_allclose(lik.sample([-10, 0, 0.5], random), [0, 1, 2])

def test_poisson_prod_lik():
    random = RandomState(0)

    lik = PoissonProdLik(ProbitLink())

    assert lik.name == 'Poisson'

    lik.noccurrences = [1, 4, 3]
    assert_allclose(lik.noccurrences, [1, 4, 3])

    assert lik.sample_size == 3
    assert_allclose(lik.mean([-1, 0, 0.5]), [0.15865525, 0.5, 0.69146246])
    assert_allclose(lik.sample([-10, 0, 0.5], random), [0, 1, 1])
