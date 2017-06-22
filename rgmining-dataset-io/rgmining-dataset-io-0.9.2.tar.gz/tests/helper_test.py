#
# helper_test.py
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
"""Unit tests for dataset_io.helper module.
"""
# pylint: disable=invalid-name
from collections import namedtuple
import json
import random
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import unittest

from dataset_io import helper

Reviewer = namedtuple("Reviewer", ("name", "anomalous_score"))
"""Mock of Reviewer class.
"""

Product = namedtuple("Product", ("name", "summary"))
"""Mock of Produce class.
"""

Graph = namedtuple("Graph", ("reviewers", "products"))
"""Mock of Graph class.
"""


class TestReviewer(unittest.TestCase):
    """Test case for Reviewer.
    """

    def test(self):
        """Construction test.
        """
        a = random.random()
        b = random.random()
        res = helper.Reviewer(a, b)
        self.assertEqual(res.reviewer_id, a)
        self.assertEqual(res.score, b)


class TestProduct(unittest.TestCase):
    """Test case for Product.
    """

    def test(self):
        """Construction test.
        """
        a = random.random()
        b = random.random()
        res = helper.Product(a, b)
        self.assertEqual(res.product_id, a)
        self.assertEqual(res.summary, b)


class TestQuiet(unittest.TestCase):
    """Test case for quite method.
    """

    def test_value_error(self):  # pylint: disable=no-self-use
        """Test with a value error.
        """
        @helper.quiet
        def sample_function():
            """Sample function.
            """
            raise ValueError
        sample_function()

    def test_no_error(self):  # pylint: disable=no-self-use
        """Test with non error function.
        """
        @helper.quiet
        def sample_function():
            """Sample function.
            """
        sample_function()

    def test_another_error(self):
        """Test with raising another error.
        """
        @helper.quiet
        def sample_function():
            """Sample function raises TypeError.
            """
            raise TypeError
        self.assertRaises(TypeError, sample_function)


class TestConvertData(unittest.TestCase):
    """Test case for convert_data method.
    """

    def test(self):
        """Test with a simple input.
        """
        self.assertEqual(helper.convert_date("1-2-3-4-5"), 12345)


class TestNormaloseRating(unittest.TestCase):
    """Test case for normalize_rating method.
    """

    def test(self):
        """Test with simple inputs.
        """
        self.assertEqual(helper.normalize_rating(5), 1.)
        self.assertEqual(helper.normalize_rating(1), 0.)
        self.assertEqual(helper.normalize_rating(3), 0.5)


class TestPrintParseState(unittest.TestCase):
    """Test case for print_state and parse_state method.
    """

    def setUp(self):
        """Create simple graph data.
        """
        self.reviewers = {}
        self.products = {}
        for i in range(10):
            rid = "r{0}".format(i)
            self.reviewers[rid] = Reviewer(rid, random.random())
            pid = "p{0}".format(i)
            self.products[pid] = Product(pid, random.random())
        self.graph = Graph(self.reviewers.values(), self.products.values())

    def test_print_state(self):
        """Test print_state with simple data.
        """
        i = "abs"
        output = StringIO()
        helper.print_state(self.graph, i, output)

        for line in output.getvalue().split("\n"):
            if not line:
                continue

            obj = json.loads(line)
            self.assertEqual(obj["iteration"], i)
            if "reviewer" in obj:
                rid = obj["reviewer"]["reviewer_id"]
                score = obj["reviewer"]["score"]
                self.assertIn(rid, self.reviewers)
                self.assertEqual(score, self.reviewers[rid].anomalous_score)

            else:
                pid = obj["product"]["product_id"]
                summary = helper.normalize_rating(obj["product"]["summary"])
                self.assertIn(pid, self.products)
                self.assertAlmostEqual(summary, self.products[pid].summary)

    def test_parse_state(self):
        """Test parse_state with simple data.
        """
        output = StringIO()
        for i in range(10):
            helper.print_state(self.graph, i, output)

        ask = 5

        def reviewer_handler(iteration, reviewer):
            """Reviewer handler.
            """
            self.assertEqual(iteration, ask)
            self.assertIn(reviewer.reviewer_id, self.reviewers)
            self.assertEqual(
                reviewer.score,
                self.reviewers[reviewer.reviewer_id].anomalous_score)

        def product_handler(iteration, product):
            """Product handler.
            """
            self.assertEqual(iteration, ask)
            self.assertIn(product.product_id, self.products)
            self.assertAlmostEqual(
                product.summary, self.products[product.product_id].summary)

        helper.parse_state(
            output.getvalue().split("\n"), reviewer_handler, product_handler, ask)


if __name__ == "__main__":
    unittest.main()
