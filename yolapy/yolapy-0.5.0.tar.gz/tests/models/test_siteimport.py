import unittest

from mock import patch

from yolapy.models import siteimport


class SiteImportTestCase(unittest.TestCase):
    def setUp(self):
        patcher = patch.object(siteimport, 'Yola')
        self.yola = patcher.start().return_value
        self.addCleanup(patcher.stop)


class SiteImportCreate(SiteImportTestCase):
    """SiteImport.create"""
    def setUp(self):
        super(SiteImportCreate, self).setUp()
        self.url = 'url'
        self.user_id = 'user_id'
        self.siteimport = siteimport.SiteImport.create(self.url, self.user_id)

    def test_creates_site_import_with_passed_arguments(self):
        self.yola.create_site_import.assert_called_once_with(
            self.url, self.user_id)

    def test_returns_site_import_instance(self):
        self.assertIsInstance(self.siteimport, siteimport.SiteImport)


class SiteImportGet(SiteImportTestCase):
    def setUp(self):
        super(SiteImportGet, self).setUp()
        self.id = 'id'
        self.site_import_data = {'id': self.id}
        self.yola.get_site_import.return_value = self.site_import_data
        self.site_import = siteimport.SiteImport.get(self.id)

    def test_gets_specified_site_import(self):
        self.yola.get_site_import.assert_called_once_with(self.id)

    def test_returns_site_import_instance(self):
        self.assertIsInstance(self.site_import, siteimport.SiteImport)


class SiteImportList(SiteImportTestCase):
    def setUp(self):
        super(SiteImportList, self).setUp()
        self.site_imports_data = [{'id': 1}, {'id': 2}]
        self.yola.list_site_imports.return_value = {
            'results': self.site_imports_data}
        self.filters = {'one': 1, 'two': 2}
        self.site_imports = siteimport.SiteImport.list(**self.filters)

    def test_gets_specified_site_import_list(self):
        _, kwargs = self.yola.list_site_imports.call_args
        for filter, value in self.filters.items():
            self.assertEqual(kwargs[filter], value)

    def test_returns_site_import_list(self):
        for site_import in self.site_imports:
            self.assertIsInstance(site_import, siteimport.SiteImport)
