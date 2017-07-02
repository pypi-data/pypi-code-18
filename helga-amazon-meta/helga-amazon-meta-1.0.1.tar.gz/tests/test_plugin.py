import re
import sys
from unittest import TestCase
try:
    from unittest import mock
except ImportError:
    from mock import mock
sys.modules['helga.plugins'] = mock.Mock()

from helga_amazon_meta.plugin import PRODUCT_REGEX, SHORT_REGEX


class TestPlugin(TestCase):
    def test_product_regex(self):
        regex = re.compile(PRODUCT_REGEX)
        expected = 'ABCD0123456'
        product_url = 'amazon.com/product_description/dp/' + expected
        result = re.search(regex, product_url)
        self.assertEqual(expected, result.group(1))

    def test_product_short(self):
        regex = re.compile(SHORT_REGEX)
        expected = 'a.co/c5aX6WD'
        product_url = 'http://' + expected
        result = re.search(regex, product_url)
        self.assertEqual(expected, result.group(1))
