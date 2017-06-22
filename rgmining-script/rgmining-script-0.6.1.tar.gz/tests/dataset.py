#
# dataset.py
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
"""Provides a small dataset for testing.

This module also provides a function which stores the small dataset to a file,
so that tests can load it via the dataset-io library.
"""
# pylint: disable=invalid-name
import json


SMALL_DATASET = [
    {
        "member_id": "reviewer1",
        "product_id": "product1",
        "rating": 4.0,
        "date": "2000-08-21"
    },
    {
        "member_id": "reviewer1",
        "product_id": "product2",
        "rating": 5.0,
        "date": "2000-08-21"
    },
    {
        "member_id": "reviewer2",
        "product_id": "product2",
        "rating": 1.0,
        "date": "2000-08-21"
    },
    {
        "member_id": "reviewer3",
        "product_id": "product2",
        "rating": 3.0,
        "date": "2000-08-21"
    },
]
"""Simple and small dataset.
"""


def store_dataset(fp):
    """Store the small dataset to a given file object.
    """
    for r in SMALL_DATASET:
        json.dump(r, fp)
        fp.write("\n")
