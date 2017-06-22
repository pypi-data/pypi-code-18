# -*- coding_ utf-8 -*-
import unittest.mock as mock

from botocore.exceptions import ClientError
from django.core.mail import send_mail, send_mass_mail
from django.test import TestCase, override_settings

from ..backend import SESEmailBackend


@override_settings(EMAIL_BACKEND='sebs.backend.SESEmailBackend')
class SESBackendTestCase(TestCase):

    @mock.patch('sebs.backend.boto3')
    def test_email_sent(self, boto_mock):
        num_sent = send_mail('hello test',
                             "yoyo, this's a test",
                             'admin@example.com',
                             ['success@simulator.amazonses.com'],
                             fail_silently=False)

        self.assertEqual(num_sent, 1)

    @mock.patch('sebs.backend.boto3')
    def test_bad_email_fails(self, boto_mock):
        connection_mock = mock.Mock()
        connection_mock.send_email.side_effect = ClientError({'Error': {'Code': ''}}, '')
        boto_mock.client.return_value = connection_mock

        with self.assertRaises(ClientError):
            send_mail('hello test',
                      "yoyo, this's a test",
                      'admin@example.com',
                      ['successsimulator.amazonses.com'],
                      fail_silently=False)

    def test_bad_email_fails_silently(self):
        num_sent = send_mail('hello test',
                             "yoyo, this's a test",
                             'admin@example.com',
                             ['successsimulator.amazonses.com'],
                             fail_silently=True)

        self.assertEqual(num_sent, 0)

    def test_send_multiple_messages(self):
        with mock.patch.object(SESEmailBackend, 'open'):
            with mock.patch.object(SESEmailBackend, '_send'):
                num_sent = send_mass_mail((
                    ('hello test',
                     "yoyo, this's a test",
                     'admin@example.com',
                     ['success@simulator.amazonses.com']),
                    ('hello 2',
                     'another message',
                     'admin@example.com',
                     ['success@simulator.amazonses.com'])),
                    fail_silently=False)

        self.assertEqual(num_sent, 2)
