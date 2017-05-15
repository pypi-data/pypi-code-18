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


class UserTestCase(IntegrationTestCase):

    def test_fetch_request(self):
        self.holodeck.mock(Response(500, ''))
        
        with self.assertRaises(TwilioException):
            self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                               .users(sid="USaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").fetch()
        
        self.holodeck.assert_has_request(Request(
            'get',
            'https://chat.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Users/USaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        ))

    def test_fetch_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "sid": "USaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "service_sid": "ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "role_sid": "RLaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "identity": "jing",
                "attributes": null,
                "friendly_name": null,
                "date_created": "2016-03-24T21:05:19Z",
                "date_updated": "2016-03-24T21:05:19Z",
                "url": "https://ip-messaging.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Users/USaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            }
            '''
        ))
        
        actual = self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                    .users(sid="USaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").fetch()
        
        self.assertIsNotNone(actual)

    def test_delete_request(self):
        self.holodeck.mock(Response(500, ''))
        
        with self.assertRaises(TwilioException):
            self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                               .users(sid="USaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").delete()
        
        self.holodeck.assert_has_request(Request(
            'delete',
            'https://chat.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Users/USaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        ))

    def test_delete_response(self):
        self.holodeck.mock(Response(
            204,
            None,
        ))
        
        actual = self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                    .users(sid="USaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").delete()
        
        self.assertTrue(actual)

    def test_create_request(self):
        self.holodeck.mock(Response(500, ''))
        
        with self.assertRaises(TwilioException):
            self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                               .users.create(identity="identity")
        
        values = {
            'Identity': "identity",
        }
        
        self.holodeck.assert_has_request(Request(
            'post',
            'https://chat.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Users',
            data=values,
        ))

    def test_create_response(self):
        self.holodeck.mock(Response(
            201,
            '''
            {
                "sid": "USaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "service_sid": "ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "role_sid": "RLaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "identity": "jing",
                "attributes": null,
                "friendly_name": null,
                "date_created": "2016-03-24T21:05:19Z",
                "date_updated": "2016-03-24T21:05:19Z",
                "url": "https://ip-messaging.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Users/USaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            }
            '''
        ))
        
        actual = self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                    .users.create(identity="identity")
        
        self.assertIsNotNone(actual)

    def test_list_request(self):
        self.holodeck.mock(Response(500, ''))
        
        with self.assertRaises(TwilioException):
            self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                               .users.list()
        
        self.holodeck.assert_has_request(Request(
            'get',
            'https://chat.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Users',
        ))

    def test_read_full_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "meta": {
                    "page": 0,
                    "page_size": 1,
                    "first_page_url": "https://ip-messaging.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Users?PageSize=1&Page=0",
                    "previous_page_url": null,
                    "url": "https://ip-messaging.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Users?PageSize=1&Page=0",
                    "next_page_url": null,
                    "key": "users"
                },
                "users": [
                    {
                        "sid": "USaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "service_sid": "ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "role_sid": "RLaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "identity": "jing",
                        "attributes": null,
                        "friendly_name": null,
                        "date_created": "2016-03-24T21:05:19Z",
                        "date_updated": "2016-03-24T21:05:19Z",
                        "url": "https://ip-messaging.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Users/USaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
                    }
                ]
            }
            '''
        ))
        
        actual = self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                    .users.list()
        
        self.assertIsNotNone(actual)

    def test_read_empty_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "meta": {
                    "page": 0,
                    "page_size": 1,
                    "first_page_url": "https://ip-messaging.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Users?PageSize=1&Page=0",
                    "previous_page_url": null,
                    "url": "https://ip-messaging.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Users?PageSize=1&Page=0",
                    "next_page_url": null,
                    "key": "users"
                },
                "users": []
            }
            '''
        ))
        
        actual = self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                    .users.list()
        
        self.assertIsNotNone(actual)

    def test_update_request(self):
        self.holodeck.mock(Response(500, ''))
        
        with self.assertRaises(TwilioException):
            self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                               .users(sid="USaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").update()
        
        self.holodeck.assert_has_request(Request(
            'post',
            'https://chat.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Users/USaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa',
        ))

    def test_update_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "sid": "USaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "service_sid": "ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "role_sid": "RLaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "identity": "jing",
                "attributes": null,
                "friendly_name": null,
                "date_created": "2016-03-24T21:05:19Z",
                "date_updated": "2016-03-24T21:05:19Z",
                "url": "https://ip-messaging.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Users/USaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
            }
            '''
        ))
        
        actual = self.client.chat.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                    .users(sid="USaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa").update()
        
        self.assertIsNotNone(actual)
