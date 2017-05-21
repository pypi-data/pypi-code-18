#!/usr/bin/env python
from enum import Enum
import numpy

__author__ = "Ronie Martinez"
__copyright__ = "Copyright 2017, Ronie Martinez"
__credits__ = ["Ronie Martinez"]
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Ronie Martinez"
__email__ = "ronmarti18@gmail.com"
__status__ = "Prototype"


class DogSize(Enum):
    """
    Enum of dog breeds and equivalent size in pounds (lbs).
    """
    SMALL = (0, 21)
    MEDIUM = (21, 51)
    LARGE = (51, 91)
    GIANT = (91, numpy.Inf)


class Age(Enum):
    """
    Enum of dog breeds and equivalent conversion tuple (<human_years_tuple>, <dog_years_tuple>)
    """
    SMALL = ((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20),
             (15, 24, 28, 32, 36, 40, 44, 48, 52, 56, 60, 64, 68, 72, 76, 80, 84, 88, 92, 96))
    MEDIUM = ((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20),
              (15, 24, 28, 32, 37, 42, 47, 51, 56, 60, 65, 69, 74, 78, 83, 87, 92, 96, 101, 105))
    LARGE = ((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20),
             (15, 24, 28, 32, 40, 45, 50, 55, 61, 66, 72, 77, 82, 88, 93, 99, 104, 109, 115, 120))
    GIANT = ((1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16),
             (15, 24, 28, 32, 42, 49, 56, 64, 71, 78, 86, 93, 101, 108, 115, 123))


class DogYearError(Exception):
    pass


def get_dog_years(human_years, dog_size):
    """
    Convert age from human years to dog years.
    :param human_years: Age in human years.
    :param dog_size: Size of dog in pounds (lbs).
    :raises DogYearError, if inputs are invalid.
    :return: Age in dog years
    """
    for size in DogSize:
        a, b = size.value
        if a <= dog_size < b:
            x, y = Age[size.name].value
            return numpy.interp(human_years, x, y)
    raise DogYearError()


def get_human_years(dog_years, dog_size):
    """
    Convert age from dog years to human years.
    :param dog_years: Age in dog years.
    :param dog_size: Size of dog in pounds (lbs).
    :raises DogYearError, if inputs are invalid.
    :return: Age in human years.
    """
    for size in DogSize:
        a, b = size.value
        if a <= dog_size < b:
            x, y = Age[size.name].value
            return numpy.interp(dog_years, y, x)
    raise DogYearError()
