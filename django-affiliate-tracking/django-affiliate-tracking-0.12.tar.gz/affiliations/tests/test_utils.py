from django.test import TestCase
from django.db.models import Model

from affiliations.utils import (
    strip_affiliate_part_from_url,
    convert_url_query_string_to_dict,
    import_from_path,
)


class TestUtils(TestCase):

    def test_strip_affiliate_part_from_url_just_one_param(self):
        url = 'https://example.com/some/?affiliate_id=1234wxyz'

        self.assertEqual(
            strip_affiliate_part_from_url(url),
            'https://example.com/some/'
        )

    def test_strip_affiliate_part_from_url_several_params(self):
        original_url = (
            'https://example.com/some/page?page_id=9&affiliate_id=1234wxyz'
            '&other=3'
        )
        expected_url = 'https://example.com/some/page?other=3&page_id=9'

        self.assertEqual(
            convert_url_query_string_to_dict(
                strip_affiliate_part_from_url(original_url)
            ),
            convert_url_query_string_to_dict(expected_url)
        )

    def test_convert_url_query_string_to_dict_no_params(self):
        url = 'https://example.com/some/page/'
        self.assertEqual(
            convert_url_query_string_to_dict(url),
            {}
        )

    def test_convert_url_query_string_to_dict_several_params(self):
        url = (
            'https://example.com/some/page?page_id=9&affiliate_id=1234wxyz'
            '&other=3'
        )
        self.assertEqual(
            convert_url_query_string_to_dict(url),
            {'page_id': '9', 'affiliate_id': '1234wxyz', 'other': '3'}
        )

    def test_import_from_path_module_exists(self):

        self.assertEqual(
            import_from_path('django.db.models.Model'),
            Model
        )
