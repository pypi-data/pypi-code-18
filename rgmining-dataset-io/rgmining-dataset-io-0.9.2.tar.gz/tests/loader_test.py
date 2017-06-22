#
# loader_test.py
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
"""Unit tests for dataset_io.loader module.
"""
# pylint: disable=invalid-name
from collections import defaultdict
import json
import random
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import unittest

from dataset_io import loader
from dataset_io.helper import normalize_rating

from tests.mock import Graph


class TestLoad(unittest.TestCase):
    """Test case for load method.
    """

    def setUp(self):
        """Create a sample graph and its JSON data.
        """
        self.reviews = defaultdict(dict)
        self.size = 0

        buf = StringIO()
        for r in range(10):
            for p in range(5):
                if random.random() > 0.5:
                    member_id = "r{0}".format(r)
                    product_id = "p{0}".format(p)
                    rating = random.randint(1, 5)
                    self.reviews[member_id][
                        product_id] = normalize_rating(rating)
                    self.size += 1
                    json.dump({
                        "member_id": member_id,
                        "product_id": product_id,
                        "rating": rating,
                        "date": "2014-01-01"
                    }, buf)
                    buf.write("\n")
        self.input = buf.getvalue().split("\n")

    def test_without_anomalous(self):
        """Test load method without specifying default anomalous score.
        """
        g = loader.load(Graph(), self.input)
        self.assertEqual(len(g.review), self.size)
        for r in g.review:
            self.assertIn(r.member_id, self.reviews)
            self.assertIn(r.product_id, self.reviews[r.member_id])
            self.assertAlmostEqual(
                r.rating, self.reviews[r.member_id][r.product_id])

    def test_without_normalizing(self):
        """Test load method without normalizing rating scores.
        """
        g = loader.load(Graph(), self.input, normalize=None)
        self.assertEqual(len(g.review), self.size)
        for r in g.review:
            self.assertIn(r.member_id, self.reviews)
            self.assertIn(r.product_id, self.reviews[r.member_id])
            self.assertAlmostEqual(
                r.rating, self.reviews[r.member_id][r.product_id] * 4 + 1)

    def test_with_anomalous(self):
        """Test load method with specifying default anomalous score.
        """
        anomalous = 0.42
        g = loader.load(Graph(), self.input, anomalous)
        self.assertEqual(len(g.review), self.size)
        for r in g.review:
            self.assertIn(r.member_id, self.reviews)
            self.assertIn(r.product_id, self.reviews[r.member_id])
            self.assertAlmostEqual(
                r.rating, self.reviews[r.member_id][r.product_id])
        for r in g.reviewers:
            self.assertEqual(r.anomalous_score, anomalous)

    def test_load_twice(self):
        """Test even if load function is called twice, it loads correct dataset.
        """
        # Load a dataset.
        g = loader.load(Graph(), self.input)

        # Create another dataset which some nodes are overrapped.
        max_reviewers = 15
        max_products = 10
        buf = StringIO()
        for r in range(5, max_reviewers):
            for p in range(3, max_products):
                member_id = "r{0}".format(r)
                product_id = "p{0}".format(p)
                if product_id in self.reviews[member_id]:
                    continue

                rating = random.randint(1, 5)
                self.reviews[member_id][
                    product_id] = normalize_rating(rating)
                self.size += 1
                json.dump({
                    "member_id": member_id,
                    "product_id": product_id,
                    "rating": rating,
                    "date": "2014-01-01"
                }, buf)
                buf.write("\n")

        # Load another dataset.
        g = loader.load(g, buf.getvalue().strip().split("\n"))

        self.assertEqual(len(g.review), self.size)
        for r in g.review:
            self.assertIn(r.member_id, self.reviews)
            self.assertIn(r.product_id, self.reviews[r.member_id])
            self.assertAlmostEqual(
                r.rating, self.reviews[r.member_id][r.product_id])


if __name__ == "__main__":
    unittest.main()
