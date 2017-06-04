import importlib.util
import logging

import numpy
import math

from time_complexity_estimator.complexities import ALL_CLASSES
from time_complexity_estimator.complexity_fitter import fit_complexity_class
from time_complexity_estimator.logging_decorant import LogWith
from time_complexity_estimator.time_measurer import measure_execution_time


class MustBePositive(Exception):
    pass


@LogWith()
def estimate_time_complexity(module_name, file_path, initializer_name, fun_to_test_name, cleaner_name=None,
                             timeout_after=30, verbose=False, n_timings=10):
    if timeout_after <= 0:
        raise MustBePositive("timeout_after")

    if n_timings <= 0:
        raise MustBePositive("n_timings")

    # Config logging
    logging.basicConfig(filename='estimate_time_complexity.log', level=logging.INFO,
                        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(msg)s',
                        datefmt="%Y-%m-%d %H:%M:%S")

    # Import functions from specified module
    fun_to_test, initializer, cleaner = import_functions_from_names(module_name, file_path, initializer_name,
                                                                    fun_to_test_name, cleaner_name=None)

    # Estimate complexity
    best = get_complexity_class(fun_to_test, initializer, timeout_after=timeout_after, n_timings=n_timings)

    # Clean if cleaner is specified
    if cleaner is not None:
        cleaner()
        logging.info('Calling cleaner: %s finished successfully', cleaner_name)

    formatted_message = fun_to_test_name + ": " + str(best)
    if verbose:
        print(formatted_message)

    def estimated_time_for_n_elements(n):
        return best.compute_time(numpy.array([n]))

    def estimated_n_elements_for_time(time_in_sec):
        return best.compute_no_elements(time_in_sec)

    logging.info("Finished estimating time complexity. Result: %s", formatted_message)

    return formatted_message, estimated_time_for_n_elements, estimated_n_elements_for_time


def import_functions_from_names(module_name, file_path, initializer_name, fun_to_test_name, cleaner_name=None):
    # Import a module given the full path
    spec = importlib.util.spec_from_file_location(module_name, file_path)
    imported_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(imported_module)
    logging.info('Importing a module: %s finished successfully', module_name)

    # Get a function form a string with the function's name
    initializer = getattr(imported_module, initializer_name)
    logging.info('Getting initializer: %s finished successfully', initializer_name)
    fun_to_test = getattr(imported_module, fun_to_test_name)
    logging.info('Getting fun_to_test: %s finished successfully', fun_to_test_name)

    # Cleaner may not be specified
    cleaner = None
    if cleaner_name is not None:
        cleaner = getattr(imported_module, cleaner_name)
        logging.info('Getting cleaner: %s finished successfully', cleaner_name)

    return fun_to_test, initializer, cleaner


def get_complexity_class(fun_to_test_name, initializer, timeout_after, n_timings, classes=ALL_CLASSES, verbose=False):
    no_measures, execution_times, terminated = measure_execution_time(fun_to_test_name, initializer,
                                                                      timeout_after=timeout_after,
                                                                      n_timings=n_timings)

    return fit_complexity_class(no_measures, execution_times, terminated, complexity_classes=classes, verbose=verbose)
