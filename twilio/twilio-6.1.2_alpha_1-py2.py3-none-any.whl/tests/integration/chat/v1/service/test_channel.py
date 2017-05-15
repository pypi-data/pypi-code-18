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


class ChannelTestCase(IntegrationTestCase):

    def test_fetch_request(self):
        self.holodeck.mock(Response(500, ''))
        
        with self.assertRaises(TwilioException):
            self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                               .channels(sid="CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").fetch()
        
        self.holodeck.assert_has_request(Request(
            'get',
            'https://chat.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Channels/CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        ))

    def test_fetch_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "sid": "CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "service_sid": "ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "friendly_name": "d816d8da-51c0-44e1-928a-44822f49bc95",
                "unique_name": "c64ad6b0-0090-4cfc-b574-b1ce5208ac0b",
                "attributes": null,
                "type": "public",
                "date_created": "2015-12-16T22:18:37Z",
                "date_updated": "2015-12-16T22:18:37Z",
                "created_by": "system",
                "url": "https://ip-messaging.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Channels/CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "links": {
                    "members": "https://ip-messaging.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Channels/CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Members",
                    "messages": "https://ip-messaging.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Channels/CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Messages"
                }
            }
            '''
        ))
        
        actual = self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                    .channels(sid="CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").fetch()
        
        self.assertIsNotNone(actual)

    def test_delete_request(self):
        self.holodeck.mock(Response(500, ''))
        
        with self.assertRaises(TwilioException):
            self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                               .channels(sid="CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").delete()
        
        self.holodeck.assert_has_request(Request(
            'delete',
            'https://chat.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Channels/CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        ))

    def test_delete_response(self):
        self.holodeck.mock(Response(
            204,
            None,
        ))
        
        actual = self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                    .channels(sid="CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").delete()
        
        self.assertTrue(actual)

    def test_create_request(self):
        self.holodeck.mock(Response(500, ''))
        
        with self.assertRaises(TwilioException):
            self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                               .channels.create()
        
        self.holodeck.assert_has_request(Request(
            'post',
            'https://chat.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Channels',
        ))

    def test_create_response(self):
        self.holodeck.mock(Response(
            201,
            '''
            {
                "sid": "CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "service_sid": "ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "friendly_name": "d816d8da-51c0-44e1-928a-44822f49bc95",
                "unique_name": "c64ad6b0-0090-4cfc-b574-b1ce5208ac0b",
                "attributes": null,
                "type": "public",
                "date_created": "2015-12-16T22:18:37Z",
                "date_updated": "2015-12-16T22:18:37Z",
                "created_by": "system",
                "url": "https://ip-messaging.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Channels/CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "links": {
                    "members": "https://ip-messaging.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Channels/CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Members",
                    "messages": "https://ip-messaging.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Channels/CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Messages"
                }
            }
            '''
        ))
        
        actual = self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                    .channels.create()
        
        self.assertIsNotNone(actual)

    def test_list_request(self):
        self.holodeck.mock(Response(500, ''))
        
        with self.assertRaises(TwilioException):
            self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                               .channels.list()
        
        self.holodeck.assert_has_request(Request(
            'get',
            'https://chat.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Channels',
        ))

    def test_read_full_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "channels": [
                    {
                        "sid": "CHc12e6f1419b244fe8da312bc2cdebebc",
                        "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "service_sid": "IS034e4a0c83f94e10a2ab4a3c19a16a86",
                        "friendly_name": "d816d8da-51c0-44e1-928a-44822f49bc95",
                        "unique_name": "c64ad6b0-0090-4cfc-b574-b1ce5208ac0b",
                        "attributes": null,
                        "type": "public",
                        "date_created": "2015-12-16T22:18:37Z",
                        "date_updated": "2015-12-16T22:18:37Z",
                        "created_by": "system",
                        "url": "https://ip-messaging.twilio.com/v1/Services/IS034e4a0c83f94e10a2ab4a3c19a16a86/Channels/CHc12e6f1419b244fe8da312bc2cdebebc",
                        "links": {
                            "members": "https://ip-messaging.twilio.com/v1/Services/IS034e4a0c83f94e10a2ab4a3c19a16a86/Channels/CHc12e6f1419b244fe8da312bc2cdebebc/Members",
                            "messages": "https://ip-messaging.twilio.com/v1/Services/IS034e4a0c83f94e10a2ab4a3c19a16a86/Channels/CHc12e6f1419b244fe8da312bc2cdebebc/Messages"
                        }
                    }
                ],
                "meta": {
                    "page": 0,
                    "page_size": 1,
                    "first_page_url": "https://ip-messaging.twilio.com/v1/Services/IS034e4a0c83f94e10a2ab4a3c19a16a86/Channels?PageSize=1&Page=0",
                    "previous_page_url": null,
                    "url": "https://ip-messaging.twilio.com/v1/Services/IS034e4a0c83f94e10a2ab4a3c19a16a86/Channels?PageSize=1&Page=0",
                    "next_page_url": null,
                    "key": "channels"
                }
            }
            '''
        ))
        
        actual = self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                    .channels.list()
        
        self.assertIsNotNone(actual)

    def test_read_empty_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "channels": [],
                "meta": {
                    "page": 0,
                    "page_size": 1,
                    "first_page_url": "https://ip-messaging.twilio.com/v1/Services/IS034e4a0c83f94e10a2ab4a3c19a16a86/Channels?PageSize=1&Page=0",
                    "previous_page_url": null,
                    "url": "https://ip-messaging.twilio.com/v1/Services/IS034e4a0c83f94e10a2ab4a3c19a16a86/Channels?PageSize=1&Page=0",
                    "next_page_url": null,
                    "key": "channels"
                }
            }
            '''
        ))
        
        actual = self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                    .channels.list()
        
        self.assertIsNotNone(actual)

    def test_update_request(self):
        self.holodeck.mock(Response(500, ''))
        
        with self.assertRaises(TwilioException):
            self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                               .channels(sid="CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").update()
        
        self.holodeck.assert_has_request(Request(
            'post',
            'https://chat.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Channels/CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        ))

    def test_update_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "sid": "CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "service_sid": "ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "friendly_name": "d816d8da-51c0-44e1-928a-44822f49bc95",
                "unique_name": "c64ad6b0-0090-4cfc-b574-b1ce5208ac0b",
                "attributes": null,
                "type": "public",
                "date_created": "2015-12-16T22:18:37Z",
                "date_updated": "2015-12-16T22:18:37Z",
                "created_by": "system",
                "url": "https://ip-messaging.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Channels/CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "links": {
                    "members": "https://ip-messaging.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Channels/CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Members",
                    "messages": "https://ip-messaging.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Channels/CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Messages"
                }
            }
            '''
        ))
        
        actual = self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                    .channels(sid="CHaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").update()
        
        self.assertIsNotNone(actual)
