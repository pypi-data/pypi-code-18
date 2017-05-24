import os

from django.test import TestCase
from arcgis_marketplace import factories


class FieldsTests(TestCase):

    def test_compress_field(self):
        obj = factories.WebMapingAppFactory(file__from_path='tests/test.zip')
        outpath = os.path.splitext(obj.file.path)[0]

        self.assertTrue(os.path.isdir(outpath))
