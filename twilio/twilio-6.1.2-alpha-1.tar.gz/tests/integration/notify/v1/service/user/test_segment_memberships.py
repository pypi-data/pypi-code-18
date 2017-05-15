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


class SegmentMembershipTestCase(IntegrationTestCase):

    def test_create_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.notify.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                 .users(identity="NUaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                 .segment_memberships.create(segment="segment")

        values = {
            'Segment': "segment",
        }

        self.holodeck.assert_has_request(Request(
            'post',
            'https://notify.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Users/NUaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/SegmentMemberships',
            data=values,
        ))

    def test_create_response(self):
        self.holodeck.mock(Response(
            201,
            '''
            {
                "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "identity": "identity",
                "segment": "segment",
                "service_sid": "ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "url": "https://notify.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Users/identity/SegmentMemberships/segment"
            }
            '''
        ))

        actual = self.client.notify.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .users(identity="NUaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .segment_memberships.create(segment="segment")

        self.assertIsNotNone(actual)

    def test_delete_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.notify.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                 .users(identity="NUaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                 .segment_memberships(segment="segment").delete()

        self.holodeck.assert_has_request(Request(
            'delete',
            'https://notify.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Users/NUaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/SegmentMemberships/segment',
        ))

    def test_delete_response(self):
        self.holodeck.mock(Response(
            204,
            None,
        ))

        actual = self.client.notify.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .users(identity="NUaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .segment_memberships(segment="segment").delete()

        self.assertTrue(actual)

    def test_fetch_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.notify.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                 .users(identity="NUaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                 .segment_memberships(segment="segment").fetch()

        self.holodeck.assert_has_request(Request(
            'get',
            'https://notify.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Users/NUaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/SegmentMemberships/segment',
        ))

    def test_fetch_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "identity": "identity",
                "segment": "segment",
                "service_sid": "ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                "url": "https://notify.twilio.com/v1/Services/ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Users/identity/SegmentMemberships/segment"
            }
            '''
        ))

        actual = self.client.notify.v1.services(sid="ISaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .users(identity="NUaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .segment_memberships(segment="segment").fetch()

        self.assertIsNotNone(actual)
