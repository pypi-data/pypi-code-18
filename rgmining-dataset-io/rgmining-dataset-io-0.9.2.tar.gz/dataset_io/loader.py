#
# loader.py
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
"""Load review data formatted in JSON to a graph object.
"""
# pylint: disable=invalid-name
from __future__ import absolute_import
import json
try:
    from itertools import imap, ifilter
except ImportError:
    imap = map
    ifilter = filter
from dataset_io.helper import convert_date
from dataset_io.helper import normalize_rating
from dataset_io.helper import quiet
from dataset_io.constants import PRODUCT_ID
from dataset_io.constants import MEMBER_ID


def load(g, fp, anomalous=None, normalize=normalize_rating):
    """Load a review dataset to a given graph object.

    The graph object must implement the :ref:`graph-interface` i.e.
    it must have the following methods:

    new_reviewer(name, anomalous)
        create and register a new reviewer which has a given `name` and
        be initialized by a given `anomalous` score,
    new_product(name)
        create and register a new product which has a given `name`,
    find_reviewer(name)
        find and return a reviewer which has given `name`,
    find_product(name)
        find and return a product which has given `name`,
    add_review(self, reviewer, product, review, date)
        add a new review from `reviewer` to `product` issued in `date`,
        in which the review is a float value.

    and must have the following properties:

    reviewers (readable)
        a set of reviewers,
    products (readable)
        a set of products.

    `fp` is an iterative object which yields a JSON string representing a review.
    Each review must have the following elements::

        {
            "member_id": "A1AF30H2MPOO9",
            "product_id": "0001056530",
            "rating": 4.0,
            "date": "2000-08-21"
        }

    where `member_id` is a reviewer's id, i.e. name, `product_id` is a product's
    id which the reviewer posts a review. Rating is a five-star score for the
    product. Date is the date the review issued.

    Args:
      g: graph object where loaded review data are stored.
      fp: readable object containing JSON data of a loading table.
      anomalous: default anomalous scores (Default: None).
      normalize: normalize function of rating scores; if set Nont, scores are
        not normalized.

    Returns:
      The graph instance, which is as same as *g*.
    """
    if not normalize:
        normalize = lambda v: v

    reviewers = {r.name: r for r in g.reviewers}
    products = {p.name: p for p in g.products}
    for review in ifilter(bool, imap(quiet(json.loads), fp)):

        member_id = review[MEMBER_ID]
        product_id = review[PRODUCT_ID]
        rating = normalize(review["rating"])
        date = convert_date(review["date"])

        if member_id in reviewers:
            r = reviewers[member_id]
        else:
            r = g.new_reviewer(name=member_id, anomalous=anomalous)
            reviewers[member_id] = r

        if product_id in products:
            p = products[product_id]
        else:
            p = g.new_product(name=product_id.strip())
            products[product_id] = p

        g.add_review(r, p, rating, date)

    return g
