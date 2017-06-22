#
# dataset_test.py
#
# Copyright (c) 2017 Junpei Kawamoto
#
# This file is part of rgmining-script.
#
# rgmining-script is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rgmining-script is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rgmining-script. If not, see <http://www.gnu.org/licenses/>.
#
# pylint: disable=import-error,no-member,invalid-name
"""Unit test for dataset command.
"""
from __future__ import absolute_import
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import json
import unittest

import dataset
import dataset_io
import numpy as np
import ria
from tests.dataset import store_dataset, SMALL_DATASET


class TestBase(unittest.TestCase):
    """Base test case which prepare creating a review graph.
    """

    def setUp(self):
        """Set up a review graph with the small dataset.
        """
        buf = StringIO()
        store_dataset(buf)
        self.graph = dataset_io.load(
            ria.one_graph(), buf.getvalue().split("\n"))


class TestRetrieveReviewers(TestBase):
    """Test case for retrieve_reviewers.
    """

    def test_product1(self):
        """Test retrieve_reviewers by finding reviewers reviewing product1.
        """
        buf = StringIO()
        dataset.retrieve_reviewers(self.graph, buf, ["product1"])
        res = {item for item in buf.getvalue().split("\n")}

        self.assertIn("reviewer1", res)
        self.assertNotIn("reviewer2", res)
        self.assertNotIn("reviewer3", res)

    def test_product2(self):
        """Test retrieve_reviewers by finding reviewers reviewing product2.
        """
        buf = StringIO()
        dataset.retrieve_reviewers(self.graph, buf, ["product2"])
        res = {item for item in buf.getvalue().split("\n")}

        self.assertIn("reviewer1", res)
        self.assertIn("reviewer2", res)
        self.assertIn("reviewer3", res)


class TestActiveReviewers(TestBase):
    """Test case for active_reviewers.
    """

    def test(self):
        """Test with a simple example.
        """
        buf = StringIO()
        dataset.active_reviewers(self.graph, buf, 2)
        res = {item for item in buf.getvalue().split("\n")}

        self.assertIn("reviewer1", res)
        self.assertNotIn("reviewer2", res)
        self.assertNotIn("reviewer3", res)


class TestReviewerSize(TestBase):
    """Test case for reviewer_size.
    """

    def test(self):
        """Test with a simple example.
        """
        buf = StringIO()
        dataset.reviewer_size(self.graph, buf, ["product1"])
        res = [json.loads(item) for item in buf.getvalue().split("\n") if item]

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["reviewer"], "reviewer1")
        self.assertEqual(res[0]["size"], 2)
        self.assertEqual(res[0]["product"], "product1")


class TestFilterReviewers(TestBase):
    """Test case for filter_reviewers.
    """

    def test(self):
        """Test with a simple example.
        """
        buf = StringIO()
        dataset.filter_reviewers(self.graph, buf, ["reviewer1"])
        res = [json.loads(item) for item in buf.getvalue().split("\n") if item]

        self.assertEqual(len(res), 2)
        for r in res:
            self.assertEqual(r["member_id"], "reviewer1")


class TestRatingAverage(TestBase):
    """Test case for rating_average.
    """

    def test(self):
        """Test with a simple example.
        """
        buf = StringIO()
        dataset.rating_average(self.graph, buf)
        res = [json.loads(item) for item in buf.getvalue().split("\n") if item]

        self.assertEqual(len(res), 2)
        for p in res:
            avg = np.mean([
                dataset_io.normalize_rating(review["rating"])
                for review in SMALL_DATASET if review["product_id"] == p["product_id"]
            ])
            self.assertAlmostEqual(p["summary"], avg)


class TestDistinctProduct(TestBase):
    """Test case for distinct_product.
    """

    def test(self):
        """Test with a simple example.
        """
        buf = StringIO()
        dataset.distinct_product(self.graph, buf)
        res = {item for item in buf.getvalue().split("\n") if item}
        expected = {r["product_id"] for r in SMALL_DATASET}

        self.assertSetEqual(res, expected)


class TestPopularProducts(TestBase):
    """Test case for popular_products.
    """

    def test(self):
        """Test with a simple example.
        """
        buf = StringIO()
        dataset.popular_products(self.graph, buf, 3)
        res = {item for item in buf.getvalue().split("\n") if item}
        expected = {"product2"}

        self.assertSetEqual(res, expected)


class TestFilterProduct(TestBase):
    """Test case for filter_product.
    """

    def test_one_product(self):
        """Test for retrieving one product.
        """
        buf = StringIO()
        dataset.filter_product(self.graph, buf, ["product1"])
        res = [json.loads(item) for item in buf.getvalue().split("\n") if item]

        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["product_id"], "product1")

    def test_two_products(self):
        """Test for retrieving two products.
        """
        buf = StringIO()
        dataset.filter_product(self.graph, buf, ["product1", "product2"])
        res = [json.loads(item) for item in buf.getvalue().split("\n") if item]

        self.assertEqual(len(res), 4)
        self.assertSetEqual(
            {item["product_id"] for item in res}, {"product1", "product2"})


class TestReviewVariance(TestBase):
    """Test case for review_variance.
    """

    def test(self):
        """Test with a simple example.
        """
        buf = StringIO()
        dataset.review_variance(self.graph, buf)
        res = [json.loads(item) for item in buf.getvalue().split("\n") if item]

        for r in res:
            scores = [
                dataset_io.normalize_rating(review["rating"])
                for review in SMALL_DATASET if review["product_id"] == r["product_id"]
            ]
            v = np.var(scores)
            self.assertEqual(r["size"], len(scores))
            self.assertAlmostEqual(r["variance"], v)

    def test_with_one_target(self):
        """Test for retrieving one product.
        """
        buf = StringIO()
        dataset.review_variance(self.graph, buf, ["product1"])
        res = [json.loads(item) for item in buf.getvalue().split("\n") if item]
        self.assertEqual(len(res), 1)
        self.assertEqual(res[0]["product_id"], "product1")

    def test_with_two_targets(self):
        """Test for retrieving two products.
        """
        buf = StringIO()
        targets = {"product1", "product2"}
        dataset.review_variance(self.graph, buf, targets)
        res = [json.loads(item) for item in buf.getvalue().split("\n") if item]
        self.assertEqual(len(res), 2)
        self.assertSetEqual({r["product_id"] for r in res}, targets)


if __name__ == "__main__":
    unittest.main()
