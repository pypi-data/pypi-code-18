from tests.test_integration.helpers import (
    create_user_with_subscription)
from tests.test_integration.test_case import YolaServiceTestCase


class TestYolaSiteImport(YolaServiceTestCase):
    """Yola: Site Import resource"""

    @classmethod
    def setUpClass(cls):
        super(TestYolaSiteImport, cls).setUpClass()
        cls.user = create_user_with_subscription(
            cls.service, **{'name': 'Kendrick Lamar'})
        cls.site_import = cls.service.create_site_import(
            **{'url': 'http://yola.com', 'user_id': cls.user['id']})

    def test_create_site_import(self):
        self.assertTrue(self.site_import)

    def test_get_site_import(self):
        self.assertEqual(
            self.service.get_site_import(self.site_import['id']),
            self.site_import)

    def test_get_user_site_imports(self):
        self.assertEqual(
            self.service.list_site_imports(user_id=self.user['id'])['results'],
            [self.site_import])
