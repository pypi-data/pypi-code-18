#
# algorithms_test.py
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
"""Unit tests for helper.algorithms module.
"""
import unittest
import ria
import helper

class TestGraph(unittest.TestCase):
    """Test case for function graph.
    """

    def test_ria_graph(self):
        """Test for creating a RIA graph with a small dataset.
        """
        graph = helper.graph("ria", ["alpha=2"])
        self.assertIsInstance(graph, ria.BipartiteGraph)
        self.assertEqual(graph.alpha, 2)


if __name__ == "__main__":
    unittest.main()
