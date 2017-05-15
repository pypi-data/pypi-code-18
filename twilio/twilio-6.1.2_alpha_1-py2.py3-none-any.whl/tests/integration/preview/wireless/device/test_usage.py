# coding=utf-8
"""
This code was generated by
\ / _    _  _|   _  _
 | (_)\/(_)(_|\/| |(/_  v1.0.0
      /       /       
"""

from tests import IntegrationTestCase
from tests.holodeck import Request
from twilio.base.exceptions import TwilioException
from twilio.http.response import Response


class UsageTestCase(IntegrationTestCase):

    def test_fetch_request(self):
        self.holodeck.mock(Response(500, ''))
        
        with self.assertRaises(TwilioException):
            self.client.preview.wireless.devices(sid="DEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                        .usage().fetch()
        
        self.holodeck.assert_has_request(Request(
            'get',
            'https://preview.twilio.com/wireless/Devices/DEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Usage',
        ))
