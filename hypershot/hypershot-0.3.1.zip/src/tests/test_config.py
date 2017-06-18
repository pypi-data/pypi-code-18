# pylint: disable=wildcard-import, unused-wildcard-import, unused-import, missing-docstring, invalid-name
"""Test 'config' module."""
import pytest

from hypershot.config import *

ITEMS = items()

@pytest.mark.parametrize('item', ['quiet', 'verbose'])
def test_item_is_in_config_items(item):
    assert item in ITEMS

@pytest.mark.parametrize('item', ['logging', 'items', 'log'])
def test_item_is_not_in_config_items(item):
    assert item not in ITEMS
