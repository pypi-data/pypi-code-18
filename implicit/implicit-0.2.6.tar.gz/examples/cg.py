"n
"" test script to verify the CG method works, and time it versus cholesky """
from __future__ import print_function

import argparse
from collections import defaultdict
import functools
import logging
import numpy
import time

from implicit import alternating_least_squares, _implicit
from implicit.implicit import nonzeros
from lastfm import read_data, bm25_weight

def benchmark_solver(Cui, factors, solver, callback, iterations=1, dtype=numpy.float64,
    regularization=0.00, num_threads=2):
    users, items = Cui.shape

    # have to explode out most of the alternating_least_squares call here
    X = numpy.random.rand(users, factors).astype(dtype) * 0.01
    Y = numpy.random.rand(items, factors).astype(dtype) * 0.01
    
    Cui, Ciu = Cui.tocsr(), Cui.T.tocsr()

    for iteration in range(iterations):
        s = time.time()
        solver(Cui, X, Y, regularization, num_threads=num_threads)
        solver(Ciu, Y, X, regularization, num_threads=num_threads)
        callback(time.time() - s, X, Y)
        logging.debug("finished iteration %i in %s", iteration, time.time() - s)

    return X, Y


def least_squares_loss(Cui, X, Y):
    """ Note: this assumes loss w/ regularization of 0 - which isn't realistic
    but for comparison of CG vs Cholesky optimizers is probably sufficient """
    users, factors = X.shape
    YtY = Y.T.dot(Y)
    loss = 0
    for u in range(users):
        A = YtY #+ regularization * numpy.eye(factors)
        b = numpy.zeros(factors)

        for i, confidence in nonzeros(Cui, u):
            factor = Y[i]
            A += (confidence - 1) * numpy.outer(factor, factor)
            b += confidence * factor
            loss += confidence

        loss += (A.dot(X[u]) - 2 * b).dot(X[u])

    # loss here is over all training examples (positive + negative)
    # normalize by the size of the matrix to have some sense of scale
    return loss / (sum(Cui.data))

    # loss = Cui * (Pu - YX_u) ^2 +  regularization*(||x||  + ||y||)
    # loss = YtX_CX_XuY - 2 YTCuPu*Xu + Cui Pu ^2 + ...
    #   deriv = 2 YtCuYXu - 2 YtCuPu 

    # loss = sum (AXu - b).dot(Xu)
        # + regularization * ||x|| + ||y""
        # + CuiPu^2

    # so CuiPu^2 is constant
    # regularization fuck that for testing


def benchmark_cg_accuracy(args):
    plays = bm25_weight(read_data(args.inputfile)[1]).tocsr()
      
    scores = []
    def test_models(elapsed, X, Y):
        scores.append(least_squares_loss(plays, X, Y))
        print(scores)

    scores = []
    benchmark_solver(plays, 100, functools.partial(_implicit.least_squares_cg, cg_steps=2),
                     test_models, iterations=25)
    print("cg2", scores)
    scores = []
    benchmark_solver(plays, 100, functools.partial(_implicit.least_squares_cg, cg_steps=3),
                     test_models, iterations=25)
    print("cg3", scores)
    scores = []
    benchmark_solver(plays, 100, functools.partial(_implicit.least_squares_cg, cg_steps=4),
                     test_models, iterations=25)
    print("cg4", scores)
    scores = []
    benchmark_solver(plays, 100, _implicit.least_squares,
                     test_models, iterations=25)
    print("chol", scores)


def benchmark_cg_times(args):
    plays = bm25_weight(read_data(args.inputfile)[1])

    with open(args.outputfile, "wb") as output:
        for factors in [50, 100 ,150, 200, 250, 300, 350, 400]:
            timing = defaultdict(list)
            benchmark_solver(plays, factors, functools.partial(_implicit.least_squares_cg,
            cg_steps=4),
                lambda elapsed, X, Y: timing['cg'].append(elapsed))

""" test script to verify the CG method works, and time it versus cholesky """
from __future__ import print_function

import argparse
from collections import defaultdict
import functools
import logging
import numpy
import time

from implicit import alternating_least_squares, _implicit
from implicit.implicit import nonzeros, calculate_loss
from lastfm import read_data, bm25_weight

def benchmark_solver(Cui, factors, solver, callback, iterations=1, dtype=numpy.float64,
    regularization=0.00, num_threads=2):
    users, items = Cui.shape

    # have to explode out most of the alternating_least_squares call here to test a 
    # single iteration. todo: refactor to a solver class
    X = numpy.random.rand(users, factors).astype(dtype) * 0.01
    Y = numpy.random.rand(items, factors).astype(dtype) * 0.01
    
    Cui, Ciu = Cui.tocsr(), Cui.T.tocsr()

