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


class RecordTestCase(IntegrationTestCase):

    def test_list_request(self):
        self.holodeck.mock(Response(500, ''))

        with self.assertRaises(TwilioException):
            self.client.api.v2010.accounts(sid="ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                 .usage \
                                 .records.list()

        self.holodeck.assert_has_request(Request(
            'get',
            'https://api.twilio.com/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Usage/Records.json',
        ))

    def test_read_full_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "end": 0,
                "first_page_uri": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Usage/Records?Page=0&PageSize=1",
                "last_page_uri": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Usage/Records?Page=68&PageSize=1",
                "next_page_uri": null,
                "num_pages": 69,
                "page": 0,
                "page_size": 1,
                "previous_page_uri": null,
                "start": 0,
                "total": 69,
                "uri": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Usage/Records",
                "usage_records": [
                    {
                        "account_sid": "ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa",
                        "api_version": "2010-04-01",
                        "category": "totalprice",
                        "count": null,
                        "count_unit": "",
                        "description": "Total Price",
                        "end_date": "2015-09-04",
                        "price": "2192.84855",
                        "price_unit": "usd",
                        "start_date": "2011-08-23",
                        "subresource_uris": {
                            "all_time": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Usage/Records/AllTime.json?Category=totalprice",
                            "daily": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Usage/Records/Daily.json?Category=totalprice",
                            "last_month": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Usage/Records/LastMonth.json?Category=totalprice",
                            "monthly": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Usage/Records/Monthly.json?Category=totalprice",
                            "this_month": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Usage/Records/ThisMonth.json?Category=totalprice",
                            "today": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Usage/Records/Today.json?Category=totalprice",
                            "yearly": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Usage/Records/Yearly.json?Category=totalprice",
                            "yesterday": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Usage/Records/Yesterday.json?Category=totalprice"
                        },
                        "uri": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Usage/Records?Category=totalprice&StartDate=2011-08-23&EndDate=2015-09-04",
                        "usage": "2192.84855",
                        "usage_unit": "usd"
                    }
                ]
            }
            '''
        ))

        actual = self.client.api.v2010.accounts(sid="ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .usage \
                                      .records.list()

        self.assertIsNotNone(actual)

    def test_read_empty_response(self):
        self.holodeck.mock(Response(
            200,
            '''
            {
                "end": 0,
                "first_page_uri": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Usage/Records?Page=0&PageSize=1",
                "last_page_uri": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Usage/Records?Page=68&PageSize=1",
                "next_page_uri": null,
                "num_pages": 69,
                "page": 0,
                "page_size": 1,
                "previous_page_uri": null,
                "start": 0,
                "total": 69,
                "uri": "/2010-04-01/Accounts/ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa/Usage/Records",
                "usage_records": []
            }
            '''
        ))

        actual = self.client.api.v2010.accounts(sid="ACaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa") \
                                      .usage \
                                      .records.list()

        self.assertIsNotNone(actual)
