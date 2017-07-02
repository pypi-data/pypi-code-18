import re
import sys
from unittest import TestCase
try:
    from unittest import mock
except ImportError:
    from mock import mock
sys.modules['helga.plugins'] = mock.Mock()

from helga_amazon_meta.plugin import PRODUCT_REGEX


class TestPlugin(TestCase):
    def test_product_regex(self):
        regex = re.compile(PRODUCT_REGEX)
        rasppi_product = 'https://www.amazon.com/Raspberry-Model-A1-2GHz-64-bit-quad-core/dp/B01CD5VC92'
        result = re.search(regex, rasppi_product)
        self.assertEqual('B01CD5VC92', result.group(1))
