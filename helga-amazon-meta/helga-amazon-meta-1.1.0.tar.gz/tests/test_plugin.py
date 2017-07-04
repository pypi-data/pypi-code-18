import re
import sys
import unittest
try:
    from unittest import mock
except ImportError:
    from mock import mock
sys.modules['helga.plugins'] = mock.Mock()

from helga_amazon_meta.plugin import parse_response, PRODUCT_REGEX, SHORT_REGEX


def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, title, price):
            self.text = """
            <html>
              <head>
                <title>{title}</title>
              </head>
              <body>
                <div id="title">{title}</div>
                <div id="priceblock_ourprice">${price}</div>
              </body>
            </html>
            """.format(title=title, price=price)

    return MockResponse(title='Raspberry PI 3', price=35)


class TestPlugin(unittest.TestCase):
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

    @mock.patch('helga_amazon_meta.plugin.requests.get', side_effect=mocked_requests_get)
    def test_parse_response(self, mock_get):
        response = parse_response('B01CD5VC92')
        self.assertIn('Raspberry PI 3', response)
        self.assertIn('$35', response)


if __name__ == '__main__':
    unittest.main()
