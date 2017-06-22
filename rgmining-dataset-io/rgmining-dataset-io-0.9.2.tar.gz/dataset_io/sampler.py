#
# samplar.py
#
# Copyright (c) 2016-2017 Junpei Kawamoto
#
# This file is part of rgmining-dataset-io.
#
# rgmining-dataset-io is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rgmining-dataset-io is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rgmining-dataset-io. If not, see <http://www.gnu.org/licenses/>.
#
# pylint: disable=no-member
"""Provide samplers for generating random ratings.

This module provides two samplers which generate random ratings.
One sampler is :class:`dataset_io.sampler.UniformSampler`.
This sampler generate ratings from an uniform distribution.
The other one is :class:`dataset_io.sampler.RatingBasedSampler`.
This sampler generate ratings from a rating distribution computed from a real
dataset provided by Amazon.com.

Note that ganerated ratings are normalized into [0, 1].
"""
import csv
from os import path
from numpy import random

_DATA_FILE = "rating.csv"


def _fullpath(filename):
    """Compute the full path of a given filename.

    Args:
      filename: Filename.

    Returns:
      The full path of the given filename.
    """
    return path.join(path.dirname(__file__), filename)


class UniformSampler(object):
    """Sampling review scores from a uniform distribution.

    This sampler is a callable object. To generate random ratings,

    .. code-block:: python

       sampler = UniformSampler()
       for rating in sampler():
           # use the rating.

    Note that in the above example, sampler never ends and break is required to
    stop the generation.
    """
    __slots__ = ()

    def __call__(self):
        """Create a iterator returns sampled values.

        Yields:
          A normalized uniform random review score.
        """
        while True:
            yield random.randint(0, 4) / 4.


class RatingBasedSampler(object):
    """Sampling review scores from a distribution based on actual reviews.

    This sampler generate ratings from a rating distribution computed from a real
    dataset provided by Amazon.com.

    According to the dataset, the distribution is the followings;

    .. csv-table::
       :header: rating, the number of reviews

       1, 167137
       2, 122025
       3, 189801
       4, 422698
       5, 1266919

    This sampler is a callable object. To generate random ratings,

    .. code-block:: python

       sampler = UniformSampler()
       for rating in sampler():
           # use the rating.

    Note that in the above example, sampler never ends and break is required to
    stop the generation.
    """
    __slots__ = ("_dist", "_keys")

    def __init__(self):
        self._dist = {}
        with open(_fullpath(_DATA_FILE)) as fp:

            for k, v in csv.reader(fp):

                self._dist[int(k)] = float(v)

        total = sum(self._dist.values())
        for k in self._dist:
            self._dist[k] /= total

        self._keys = sorted(self._dist.keys())

    def __call__(self):
        """Create a iterator returns sampled values.

        Yields:
          A normalized uniform random review score.
        """
        while True:
            U = random.random()
            for k in self._keys:
                U -= self._dist[k]
                if U < 0:
                    yield (k - 1) / 4.
