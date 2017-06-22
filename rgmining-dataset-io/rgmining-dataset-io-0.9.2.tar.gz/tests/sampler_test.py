#
# samplar_test.py
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
# pylint: disable=protected-access, invalid-name
"""Unit tests for dataset_io.sampler module.
"""
from __future__ import division
from collections import defaultdict
import itertools
import unittest

from dataset_io.helper import normalize_rating
from dataset_io.sampler import UniformSampler
from dataset_io.sampler import RatingBasedSampler


class TestUniformSampler(unittest.TestCase):
    """Test case for UniformSampler class.
    """

    def test(self):
        """Test the correctness by comparing max and min appearance.
        """
        counter = defaultdict(int)
        size = 100000
        sampler = UniformSampler()
        for s in itertools.islice(sampler(), size):
            counter[s] += 1

        error = max(counter.values()) - min(counter.values())
        self.assertLess(error, size * 0.01)  # Less than 1%.


class TestRatingBasedSampler(unittest.TestCase):
    """Test case for RatingBasedSampler class.
    """

    def test(self):
        """Test the correctness by comparing ratios of the original histogram.
        """
        counter = defaultdict(int)
        size = 100000
        sampler = RatingBasedSampler()
        for s in itertools.islice(sampler(), size):
            counter[s] += 1

        ratios = [
            abs(counter[normalize_rating(rating)] / size - value)
            for rating, value in sampler._dist.items()
        ]
        error = max(ratios) - min(ratios)
        self.assertLess(error, size * 0.01)


if __name__ == "__main__":
    unittest.main()
