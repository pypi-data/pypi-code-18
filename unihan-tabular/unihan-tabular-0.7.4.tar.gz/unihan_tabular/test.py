# -*- coding: utf-8 -*-
"""Test helpers functions for downloading and processing Unihan data."""

from __future__ import (absolute_import, division, print_function,
                        unicode_literals, with_statement)

import os


def get_datapath(filename):
    return os.path.join(
        os.path.dirname(__file__), '..', 'tests', 'fixtures', filename
    )


def assert_dict_contains_subset(subset, dictionary, msg=None):
    for key, value in subset.items():
        assert key in dictionary, msg
        assert dictionary[key] == value, msg
