# pylint: disable=missing-docstring
import unittest

from django.core.exceptions import ImproperlyConfigured, ValidationError
from django.test import override_settings

from rolca.frontend.tests.utils import get_image_field
from rolca.frontend.validators import (
    _humanize_size, validate_format, validate_long_edge, validate_size,
)


class ValidatorsTest(unittest.TestCase):
    def setUp(self):
        self.image_field = get_image_field()

    def test_humanize_size(self):
        self.assertEqual(_humanize_size(1024**5), '1024 GB')
        self.assertEqual(_humanize_size(1024 * 1024), '1 MB')
        self.assertEqual(_humanize_size(500 * 1024), '500 KB')
        self.assertEqual(_humanize_size(1000000), '976.56 KB')
        self.assertEqual(_humanize_size(1), '1 B')

    def test_validate_format(self):
        with override_settings(ROLCA_ACCEPTED_FORMATS=['JPEG']):
            validate_format(self.image_field)

        with override_settings(ROLCA_ACCEPTED_FORMATS=['PNG']):
            with self.assertRaises(ValidationError):
                validate_format(self.image_field)

        with override_settings(ROLCA_ACCEPTED_FORMATS='JPEG'):
            with self.assertRaises(ImproperlyConfigured):
                validate_format(self.image_field)

        with override_settings(ROLCA_ACCEPTED_FORMATS=None):
            validate_format(self.image_field)

    def test_validate_size(self):
        with override_settings(ROLCA_MAX_SIZE=1024):
            validate_size(self.image_field)

        with override_settings(ROLCA_MAX_SIZE=1):
            with self.assertRaises(ValidationError):
                validate_size(self.image_field)

        with override_settings(ROLCA_MAX_SIZE='1024'):
            with self.assertRaises(ImproperlyConfigured):
                validate_size(self.image_field)

        with override_settings(ROLCA_MAX_SIZE=None):
            validate_size(self.image_field)

    def test_validate_long_edge(self):
        with override_settings(ROLCA_MAX_LONG_EDGE=100):
            validate_long_edge(self.image_field)

        with override_settings(ROLCA_MAX_LONG_EDGE=50):
            with self.assertRaises(ValidationError):
                validate_long_edge(self.image_field)

        with override_settings(ROLCA_MAX_LONG_EDGE='100'):
            with self.assertRaises(ImproperlyConfigured):
                validate_long_edge(self.image_field)

        with override_settings(ROLCA_MAX_LONG_EDGE=None):
            validate_long_edge(self.image_field)
