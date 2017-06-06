from django.test import TestCase, override_settings
from maas.exceptions import *
from maas.models import *


class GenericTest(TestCase):

    def setUp(self):

        def buildMail():
            return Mail(sender='test@test.com', recipient='test@test.com', subject='subject', body='body')

        self.buildMail = buildMail

    def test_no_settings(self):
        with self.assertRaises(MaasConfigurationException):
            mail = self.buildMail()
            mail.send()

    @override_settings(MAAS={})
    def test_no_provider(self):
        with self.assertRaises(MaasConfigurationException):
            mail = self.buildMail()
            mail.send()

    @override_settings(MAAS={'PROVIDER': 'UNKNOWN'})
    def test_unknown_provider(self):
        with self.assertRaises(MaasConfigurationException):
            mail = self.buildMail()
            mail.send()