from __future__ import absolute_import

import logging

import numpy as np

from time_complexity_estimator.complexities import ALL_CLASSES, UnderDeterminedEquation
from time_complexity_estimator.logging_decorant import LogWith


@LogWith()
def fit_complexity_class(no_measures, execution_times, terminated, complexity_classes=ALL_CLASSES, verbose=False):
    best_complexity = None
    lowest_residuals = np.inf
    for complexity in complexity_classes:
        try:
            inst = complexity(terminated)
            residuals = inst.compute_coefficients(no_measures, execution_times)

            if residuals < lowest_residuals - 1e-6:
                lowest_residuals = residuals
                best_complexity = inst
            if verbose:
                print(inst, '(r={:f})'.format(residuals))

        except UnderDeterminedEquation:
            msg = "Equation for complecity class: " + complexity.__class__.__name__ + " is under-determined"
            logging.warning(msg)
            print(msg)

    logging.info("Fitted the most suitable complexity class: %s", best_complexity.__class__.__name__)
    return best_complexity
