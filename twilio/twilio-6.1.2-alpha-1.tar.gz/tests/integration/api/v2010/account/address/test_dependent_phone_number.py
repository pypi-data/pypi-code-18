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


class DependentPhoneNumberTestCase(IntegrationTestCase):

    def test_list_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.api.v2010.accounts(sid="ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                 .addresses(sid="ADaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                 .dependent_phone_numbers.list()

        self.holodeck.assert_has_request(Request(
            'get',
            'https://api.twilio.com/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Addresses/ADaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/DependentPhoneNumbers.json',
        ))

    def test_read_full_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "dependent_phone_numbers": [
                    {
                        "address_requirements": "any",
                        "capabilities": {
                            "MMS": "false",
                            "SMS": "true",
                            "voice": "true"
                        },
                        "friendly_name": "(510) 555-1212",
                        "iso_country": "US",
                        "lata": "722",
                        "latitude": "37.780000",
                        "longitude": "-122.380000",
                        "phone_number": "+15105551212",
                        "postal_code": "94703",
                        "rate_center": "OKLD TRNID",
                        "region": "CA"
                    }
                ],
                "first_page_uri": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Addresses/ADaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/DependentPhoneNumbers.json?Page=0&PageSize=50",
                "next_page_uri": null,
                "page": 0,
                "page_size": 50,
                "previous_page_uri": null,
                "uri": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Addresses/ADaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/DependentPhoneNumbers.json"
            }
            '''
        ))

        actual = self.client.api.v2010.accounts(sid="ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .addresses(sid="ADaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .dependent_phone_numbers.list()

        self.assertIsNotNone(actual)

    def test_read_empty_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "dependent_phone_numbers": [],
                "first_page_uri": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Addresses/ADaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/DependentPhoneNumbers.json?Page=0&PageSize=50",
                "next_page_uri": null,
                "page": 0,
                "page_size": 50,
                "previous_page_uri": null,
                "uri": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Addresses/ADaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/DependentPhoneNumbers.json"
            }
            '''
        ))

        actual = self.client.api.v2010.accounts(sid="ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .addresses(sid="ADaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .dependent_phone_numbers.list()

        self.assertIsNotNone(actual)
