"""Definition of complexity classes."""

import logging

import numpy as np
from scipy.special import lambertw

from time_complexity_estimator.logging_decorant import LogWith


class NotFittedError(Exception):
    pass


class UnderDeterminedEquation(Exception):
    pass


class ComplexityClass:
    """ Abstract class that fits complexity classes to timing data.
    """

    def __init__(self, terminated_measurement):
        # list of parameters of the fitted function class as returned by the
        # last square method np.linalg.lstsq
        self.coefficients = None
        self.terminated_measurement = terminated_measurement

    @LogWith()
    def compute_coefficients(self, no_measures, execution_times):
        """ Compute coefficients to timing data
        """
        x = self._transform_n(no_measures)
        y = self._transform_time(execution_times)
        coefficients, residuals, rank, s = np.linalg.lstsq(x, y)
        if len(residuals) == 0:
            raise UnderDeterminedEquation

        logging.info("Computed coefficients for %15s complexity class. Residuals: %.20f", self.__class__.__name__,
                     residuals[0])
        self.coefficients = coefficients
        return residuals[0]

    def compute_time(self, no_measures):
        """ Compute the function_name of the fitted function at `no_measures`. """
        if self.coefficients is None:
            logging.error("Coefficients not fitted yet. Class: %s", self.__class__.__name__)
            raise NotFittedError()

        # Result is linear combination of the terms with the fitted
        # coefficients
        x = self._transform_n(no_measures)
        tot = 0
        for i in range(len(self.coefficients)):
            tot += self.coefficients[i] * x[:, i]  # x[:, i] wez i-ta kolumne z x; mnożenie
        if tot < 0:
            return 0
        else:
            return tot

    def compute_no_elements(self, time):
        """ Compute number of elements of the fitted function for time"""
        result = (time - self.coefficients[0]) / self.coefficients[1]
        if result < 0:
            return 0
        else:
            return self._inverse_function(result)

    def __str__(self):
        prefix = ""
        if self.terminated_measurement is False:
            prefix = prefix + "Could not perform all measurements. Predicted time complexity: "

        if self.coefficients is None:
            return prefix + ': not yet fitted'
        return prefix + self.format_str().format(*tuple(self.coefficients))

    # --- abstract methods

    @staticmethod
    def format_str():
        return 'FORMAT STRING NOT DEFINED'

    def _transform_n(self, n):
        raise NotImplementedError()

    def _inverse_function(self, x):
        raise NotImplementedError()

    def _transform_time(self, t):
        return t


# --- Concrete implementations of the most popular complexity classes

class Constant(ComplexityClass):
    def _transform_n(self, n):
        return np.ones((len(n), 1))

    def compute_no_elements(self, time):
        if time >= self.coefficients[0]:
            return np.inf
        else:
            return 0

    def _inverse_function(self, x):
        return x

    @staticmethod
    def format_str():
        return 'O(1), estimated time = {:.2G}'


class Linear(ComplexityClass):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n]).T

    def _inverse_function(self, x):
        return x

    @staticmethod
    def format_str():
        return 'O(n), estimated time = {:.2G} + {:.2G}*n'


class Quadratic(ComplexityClass):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n * n]).T

    def _inverse_function(self, x):
        return np.sqrt(x)

    @staticmethod
    def format_str():
        return 'O(n^2), estimated time = {:.2G} + {:.2G}*n^2'


class Cubic(ComplexityClass):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n ** 3]).T

    def _inverse_function(self, x):
        return np.cbrt(x)

    @staticmethod
    def format_str():
        return 'O(n^3), estimated time = {:.2G} + {:.2G}*n^3'


class Logarithmic(ComplexityClass):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), np.log(n)]).T

    def _inverse_function(self, x):
        return np.exp(x)

    @staticmethod
    def format_str():
        return 'O(log(n)), estimated time = {:.2G} + {:.2G}*log(n)'


class Linearithmic(ComplexityClass):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n * np.log(n)]).T

    def _inverse_function(self, x):
        return x / lambertw(x)

    @staticmethod
    def format_str():
        return 'O(n*log(n)), estimated time = {:.2G} + {:.2G}*n*log(n)'


class Polynomial(ComplexityClass):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), np.log(n)]).T

    def _inverse_function(self, x):
        return np.power(x, 1 / self.coefficients[1])

    def _transform_time(self, t):
        return np.log(t)

    @staticmethod
    def format_str():
        return 'O(n^x), estimated time = {:.2G} * n^{:.2G}'


class Exponential(ComplexityClass):
    def _transform_n(self, n):
        return np.vstack([np.ones(len(n)), n]).T

    def compute_no_elements(self, time):
        return np.log(time)

    def _transform_time(self, t):
        return np.log(t)

    def _inverse_function(self, x):
        return np.power(x, 1 / self.coefficients[1])

    @staticmethod
    def format_str():
        return 'O(x^n), estimated time = {:.2G} + {:.2G}^n'


ALL_CLASSES = [Constant, Linear, Quadratic, Cubic, Polynomial,
               Logarithmic, Linearithmic, Exponential]
