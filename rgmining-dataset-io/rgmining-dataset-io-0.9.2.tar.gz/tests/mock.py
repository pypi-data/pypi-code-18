#
# mock.py
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
"""Provide mock objects for testing dataset_io package.
"""
from collections import namedtuple


Review = namedtuple("Review", ("member_id", "product_id", "rating", "date"))
"""A mock of review object.
"""


class Reviewer(object):
    """A mock of reviewer object.
    """

    def __init__(self, name, anomalous_score):
        self.name = name
        self.anomalous_score = anomalous_score


class Product(object):
    """A mock of product object.
    """

    def __init__(self, name, summary):
        self.name = name
        self.summary = summary


class Graph(object):
    """A mock graph class to test loader.load.
    """

    def __init__(self):
        self._reviewers = {}
        self._products = {}
        self.review = set()

    @property
    def reviewers(self):
        """Return a set of reviewers.
        """
        return self._reviewers.values()

    @property
    def products(self):
        """Return a set of products.
        """
        return self._products.values()

    def new_reviewer(self, name, anomalous=0):
        """create and register a new reviewer.

        New reviewer has a given `name` and be initialized by a given
        `anomalous` score.
        """
        assert name not in self._reviewers
        res = Reviewer(name, anomalous)
        self._reviewers[name] = res
        return res

    def new_product(self, name):
        """create and register a new product which has a given `name`.
        """
        assert name not in self._products
        res = Product(name, 0)
        self._products[name] = res
        return res

    def find_reviewer(self, name):
        """find and return a reviewer which has given `name`.
        """
        return self._reviewers[name]

    def find_product(self, name):
        """find and return a product which has given `name`.
        """
        return self._products[name]

    def add_review(self, reviewer, product, review, date):
        """add a new review from `reviewer` to `product` issued in `date`.

        The review is a float value.
        """
        self.review.add(Review(reviewer.name, product.name, review, date))
