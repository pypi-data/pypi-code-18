import logging
import time
from multiprocessing import Manager, Process
from timeit import Timer

import numpy as np

from time_complexity_estimator.logging_decorant import LogWith


@LogWith()
def measure_execution_time(fun_to_test_name, initializer, timeout_after, n_timings, n_repeats=1):
    # we need a wrapper that holds a reference to fun_to_test_name and the generated data
    # for the timeit.Timer object
    class FuncWrapper(object):

        def __init__(self, n_el):
            self.data = initializer(n_el)

        def __call__(self):
            return fun_to_test_name(self.data)

    # Prepare array with number of measurements
    no_measures = prepare_no_measures()

    manager = Manager()
    execution_times = manager.list(range(no_measures.size))

    def perform_measurement(iteration, n_el):
        timer = Timer(FuncWrapper(n_el))
        measurements = timer.repeat(n_timings, n_repeats)
        execution_times[iteration] = np.min(measurements)

    measurements_count = 0
    for i, n in enumerate(no_measures):
        start = time.time()
        p = Process(target=perform_measurement, name="Perform_measurement", args=(i, n,))
        p.start()
        p.join(timeout_after)
        if p.is_alive():
            logging.warning("Measurement for n_elements: %i is performed for too long. Terminating...", n)
            # Terminate perform_measurement
            p.terminate()
            p.join()
            break
        else:
            measurements_count = i + 1
            end = time.time()
            diff = end - start
            timeout_after = timeout_after - diff
            logging.info("Measurement executed: n_elements: %6d, iteration: %2d, time left: %f sec", n, i,
                         timeout_after)

    # Check if measurement has been terminated
    terminated = measurements_count == no_measures.size

    return no_measures[:measurements_count], execution_times[:measurements_count], terminated


def prepare_no_measures():
    no_measures = np.linspace(1, 20, 20).astype('int64')
    no_measures = np.append(no_measures, np.linspace(30, 100, 8).astype('int64'))
    for i in range(2, 5):
        no_measures = np.append(no_measures, np.linspace(2 * 10 ** i, 10 ** (i + 1), 5).astype('int64'))
    return no_measures
