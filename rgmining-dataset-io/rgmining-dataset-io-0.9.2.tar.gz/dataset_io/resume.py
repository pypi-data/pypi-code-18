#
# resume.py
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
"""Provide a function to resume mining.
"""
from __future__ import absolute_import
from dataset_io.helper import parse_state


def resume(graph, state, iteration="final"):
    """Reconstruct a bipertite graph from original file and outputed state file.

    Args:
      graph: A empty bipertite graph object.
      state: A readable object containing state data outputed by helper.print_state.
      iteration: Loading iteration. (Default: final)

    Returns:
      The graph instance. This is as same as *graph*.
    """
    def reviewer_handler(_, reviewer):
        """Parse reviewers.

        Args:
          reviewer: New reviewer.
        """
        r = graph.find_reviewer(reviewer.reviewer_id)
        if r:
            r.anomalous_score = reviewer.score

    def product_handler(_, product):
        """Parse product.

        Args:
          product: New product.
        """
        p = graph.find_product(product.product_id)
        if p:
            p.summary = product.summary

    parse_state(state, reviewer_handler, product_handler, iteration)
    return graph
