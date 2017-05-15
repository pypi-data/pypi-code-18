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


class InstalledAddOnTestCase(IntegrationTestCase):

    def test_create_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.preview.marketplace.installed_add_ons.create(available_add_on_sid="XBaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", accept_terms_of_service=True)

        values = {
            'AvailableAddOnSid': "XBaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
            'AcceptTermsOfService': True,
        }

        self.holodeck.assert_has_request(Request(
            'post',
            'https://preview.twilio.com/marketplace/InstalledAddOns',
            data=values,
        ))

    def test_create_response(self):
        self.holodeck.mock(Response(
            201,
            '''
            {
                "sid": "XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "friendly_name": "VoiceBase High Accuracy Transcription",
                "description": "Automatic Transcription and Keyword Extract...",
                "configuration": {
                    "bad_words": true
                },
                "unique_name": "voicebase_high_accuracy_transcription_1",
                "date_created": "2016-04-07T23:52:28Z",
                "date_updated": "2016-04-07T23:52:28Z",
                "url": "https://preview.twilio.com/marketplace/InstalledAddOns/XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "links": {
                    "extensions": "https://preview.twilio.com/marketplace/InstalledAddOns/XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Extensions",
                    "available_add_on": "https://preview.twilio.com/marketplace/AvailableAddOns/XBaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                }
            }
            '''
        ))

        actual = self.client.preview.marketplace.installed_add_ons.create(available_add_on_sid="XBaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa", accept_terms_of_service=True)

        self.assertIsNotNone(actual)

    def test_delete_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.preview.marketplace.installed_add_ons(sid="XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").delete()

        self.holodeck.assert_has_request(Request(
            'delete',
            'https://preview.twilio.com/marketplace/InstalledAddOns/XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        ))

    def test_delete_response(self):
        self.holodeck.mock(Response(
            204,
            None,
        ))

        actual = self.client.preview.marketplace.installed_add_ons(sid="XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").delete()

        self.assertTrue(actual)

    def test_fetch_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.preview.marketplace.installed_add_ons(sid="XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").fetch()

        self.holodeck.assert_has_request(Request(
            'get',
            'https://preview.twilio.com/marketplace/InstalledAddOns/XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        ))

    def test_fetch_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "sid": "XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "friendly_name": "VoiceBase High Accuracy Transcription",
                "description": "Automatic Transcription and Keyword Extract...",
                "configuration": {
                    "bad_words": true
                },
                "unique_name": "voicebase_high_accuracy_transcription",
                "date_created": "2016-04-07T23:52:28Z",
                "date_updated": "2016-04-07T23:52:28Z",
                "url": "https://preview.twilio.com/marketplace/InstalledAddOns/XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "links": {
                    "extensions": "https://preview.twilio.com/marketplace/InstalledAddOns/XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Extensions",
                    "available_add_on": "https://preview.twilio.com/marketplace/AvailableAddOns/XBaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                }
            }
            '''
        ))

        actual = self.client.preview.marketplace.installed_add_ons(sid="XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").fetch()

        self.assertIsNotNone(actual)

    def test_update_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.preview.marketplace.installed_add_ons(sid="XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").update()

        self.holodeck.assert_has_request(Request(
            'post',
            'https://preview.twilio.com/marketplace/InstalledAddOns/XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        ))

    def test_update_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "sid": "XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "friendly_name": "VoiceBase High Accuracy Transcription",
                "description": "Automatic Transcription and Keyword Extract...",
                "configuration": {
                    "bad_words": true
                },
                "unique_name": "voicebase_high_accuracy_transcription_2",
                "date_created": "2016-04-07T23:52:28Z",
                "date_updated": "2016-04-07T23:52:28Z",
                "url": "https://preview.twilio.com/marketplace/InstalledAddOns/XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "links": {
                    "extensions": "https://preview.twilio.com/marketplace/InstalledAddOns/XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Extensions",
                    "available_add_on": "https://preview.twilio.com/marketplace/AvailableAddOns/XBaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                }
            }
            '''
        ))

        actual = self.client.preview.marketplace.installed_add_ons(sid="XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").update()

        self.assertIsNotNone(actual)

    def test_list_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.preview.marketplace.installed_add_ons.list()

        self.holodeck.assert_has_request(Request(
            'get',
            'https://preview.twilio.com/marketplace/InstalledAddOns',
        ))

    def test_read_full_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "installed_add_ons": [
                    {
                        "sid": "XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "friendly_name": "VoiceBase High Accuracy Transcription",
                        "description": "Automatic Transcription and Keyword Extract...",
                        "configuration": {
                            "bad_words": true
                        },
                        "unique_name": "voicebase_high_accuracy_transcription",
                        "date_created": "2016-04-07T23:52:28Z",
                        "date_updated": "2016-04-07T23:52:28Z",
                        "url": "https://preview.twilio.com/marketplace/InstalledAddOns/XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "links": {
                            "extensions": "https://preview.twilio.com/marketplace/InstalledAddOns/XEaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Extensions",
                            "available_add_on": "https://preview.twilio.com/marketplace/AvailableAddOns/XBaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                        }
                    }
                ],
                "meta": {
                    "page": 0,
                    "page_size": 50,
                    "first_page_url": "https://preview.twilio.com/marketplace/InstalledAddOns?PageSize=50&Page=0",
                    "previous_page_url": null,
                    "url": "https://preview.twilio.com/marketplace/InstalledAddOns?PageSize=50&Page=0",
                    "next_page_url": null,
                    "key": "installed_add_ons"
                }
            }
            '''
        ))

        actual = self.client.preview.marketplace.installed_add_ons.list()

        self.assertIsNotNone(actual)

    def test_read_empty_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "installed_add_ons": [],
                "meta": {
                    "page": 0,
                    "page_size": 50,
                    "first_page_url": "https://preview.twilio.com/marketplace/InstalledAddOns?PageSize=50&Page=0",
                    "previous_page_url": null,
                    "url": "https://preview.twilio.com/marketplace/InstalledAddOns?PageSize=50&Page=0",
                    "next_page_url": null,
                    "key": "installed_add_ons"
                }
            }
            '''
        ))

        actual = self.client.preview.marketplace.installed_add_ons.list()

        self.assertIsNotNone(actual)
