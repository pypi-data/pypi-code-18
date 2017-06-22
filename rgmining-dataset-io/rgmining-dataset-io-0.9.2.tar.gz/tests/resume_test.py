#
# result_test.py
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
"""Unit tests for dataset_io.resume module.
"""
# pylint: disable=invalid-name
import random
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO
import unittest

from dataset_io import resume
from dataset_io.helper import normalize_rating
from dataset_io.helper import print_state

from tests.mock import Graph


class TestResume(unittest.TestCase):
    """Test case for resume method.
    """

    def setUp(self):
        """Create a sample graph and its JSON data.
        """
        self.graph = Graph()
        reviewers = {}
        products = {}
        for r in range(10):
            for p in range(5):
                if random.random() > 0.5:
                    continue

                member_id = "r{0}".format(r)
                product_id = "p{0}".format(p)
                rating = normalize_rating(random.randint(1, 5))

                if member_id not in reviewers:
                    reviewers[member_id] = self.graph.new_reviewer(member_id)
                if product_id not in products:
                    products[product_id] = self.graph.new_product(product_id)

                self.graph.add_review(
                    reviewers[member_id], products[product_id],
                    rating, "2014-01-01")

    def test(self):
        """Test resume method with a random graph and states.
        """
        output = StringIO()

        # Construct a target state.
        anomalous_score = random.random()
        summary = random.random()
        for r in self.graph.reviewers:
            r.anomalous_score = anomalous_score
        for p in self.graph.products:
            p.summary = summary
        print_state(self.graph, 1, output)

        # Update state.
        for i in range(5, 10):
            for r in self.graph.reviewers:
                r.anomalous_score = random.random()
            for p in self.graph.products:
                p.summary = random.random()
            print_state(self.graph, i, output)

        # Restore state.
        g = resume(self.graph, output.getvalue().split("\n"), 1)
        for r in g.reviewers:
            self.assertEqual(r.anomalous_score, anomalous_score)
        for p in g.products:
            self.assertAlmostEqual(p.summary, summary)


if __name__ == "__main__":
    unittest.main()
