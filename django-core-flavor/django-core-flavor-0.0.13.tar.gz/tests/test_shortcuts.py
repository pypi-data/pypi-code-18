from django.test import TestCase
from django.test.client import RequestFactory

from core_flavor import shortcuts


class ShortcutsTests(TestCase):

    def test_camel_to_dashed(self):
        self.assertIn('my_test', shortcuts.camel_to_dashed({
            'myTest': {'camelToDashed': True}
        }))

    def test_client_ip(self):
        factory = RequestFactory()
        request = factory.get('/')
        self.assertEqual(shortcuts.get_client_ip(request), '127.0.0.1')

        forwarder_ip = '0.0.0.1'
        request = factory.get('/', HTTP_X_FORWARDED_FOR=forwarder_ip)
        self.assertEqual(shortcuts.get_client_ip(request), forwarder_ip)

    def test_sizeof_fmt(self):
        self.assertEqual(shortcuts.sizeof_fmt(1024 ** 2), '1.0MB')
        self.assertEqual(shortcuts.sizeof_fmt(1024 ** 4), '1.0TB')
