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


class NotificationTestCase(IntegrationTestCase):

    def test_create_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.notify.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                 .notifications.create()

        self.holodeck.assert_has_request(Request(
            'post',
            'https://notify.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Notifications',
        ))

    def test_create_response(self):
        self.holodeck.mock(Response(
            201,
            '''
            {
                "sid": "NOb8021351170b4e1286adaac3fdd6d082",
                "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "service_sid": "IS699b53e02da45a1ba9d13b7d7d2766af",
                "date_created": "2016-03-24T23:42:28Z",
                "identities": [
                    "jing"
                ],
                "tags": [],
                "segments": [],
                "priority": "high",
                "ttl": 2419200,
                "title": "test",
                "body": "body",
                "sound": null,
                "action": null,
                "data": null,
                "apn": null,
                "fcm": null,
                "gcm": null,
                "sms": null,
                "facebook_messenger": null
            }
            '''
        ))

        actual = self.client.notify.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .notifications.create()

        self.assertIsNotNone(actual)
