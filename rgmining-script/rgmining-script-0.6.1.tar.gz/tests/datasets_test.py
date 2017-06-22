#
# datasets_test.py
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
"""Unit tests for helper.datasets module.
"""
import tempfile
import unittest

import ria

from helper import datasets
from tests.dataset import store_dataset, SMALL_DATASET


class TestLoad(unittest.TestCase):
    """Test case for function load.
    """

    def test(self):
        """Test for creating a RIA graph with a small dataset.
        """
        reviewer_names = {review["member_id"] for review in SMALL_DATASET}
        product_names = {review["product_id"] for review in SMALL_DATASET}

        graph = ria.one_graph()
        with tempfile.NamedTemporaryFile("w") as fp:
            store_dataset(fp)
            fp.flush()
            datasets.load(graph, "file", ["file={0}".format(fp.name)])

        self.assertTrue(graph.reviewers)
        for r in graph.reviewers:
            self.assertIn(r.name, reviewer_names)

        self.assertTrue(graph.products)
        for p in graph.products:
            self.assertIn(p.name, product_names)


if __name__ == "__main__":
    unittest.main()
