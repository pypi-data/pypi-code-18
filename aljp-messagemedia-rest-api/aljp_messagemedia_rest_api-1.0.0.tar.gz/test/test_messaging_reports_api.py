# coding: utf-8

"""
    MessageMedia REST API

    Australia's Leading Messaging Solutions for Business and Enterprise.

    OpenAPI spec version: 1.0.0
    Contact: support@messagemedia.com

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.
"""

from __future__ import absolute_import

import os
import sys
import unittest

import messagemedia_rest_api
from messagemedia_rest_api.rest import ApiException
from messagemedia_rest_api.apis.messaging_reports_api import MessagingReportsApi


class TestMessagingReportsApi(unittest.TestCase):
    """ MessagingReportsApi unit test stubs """

    def setUp(self):
        self.api = messagemedia_rest_api.apis.messaging_reports_api.MessagingReportsApi()

    def tearDown(self):
        pass

    def test_get_async_report_by_id(self):
        """
        Test case for get_async_report_by_id

        Gets a single asynchronous report.
        """
        pass

    def test_get_async_report_data_by_id(self):
        """
        Test case for get_async_report_data_by_id

        Gets the data of an asynchronous report.
        """
        pass

    def test_get_async_reports(self):
        """
        Test case for get_async_reports

        Lists asynchronous reports.
        """
        pass

    def test_get_delivery_reports_detail(self):
        """
        Test case for get_delivery_reports_detail

        Returns a list of delivery reports
        """
        pass

    def test_get_delivery_reports_summary(self):
        """
        Test case for get_delivery_reports_summary

        Returns a summarised report of delivery reports
        """
        pass

    def test_get_metadata_keys(self):
        """
        Test case for get_metadata_keys

        Returns a list of metadata keys
        """
        pass

    def test_get_received_messages_detail(self):
        """
        Test case for get_received_messages_detail

        Returns a list message received
        """
        pass

    def test_get_received_messages_summary(self):
        """
        Test case for get_received_messages_summary

        Returns a summarised report of messages received
        """
        pass

    def test_get_sent_messages_detail(self):
        """
        Test case for get_sent_messages_detail

        Returns a list of message sent
        """
        pass

    def test_get_sent_messages_summary(self):
        """
        Test case for get_sent_messages_summary

        Returns a summarised report of messages sent
        """
        pass

    def test_submit_async_delivery_reports_detail(self):
        """
        Test case for submit_async_delivery_reports_detail

        Submits a request to generate an async detail report
        """
        pass

    def test_submit_delivery_reports_summary(self):
        """
        Test case for submit_delivery_reports_summary

        Submits a summarised report of delivery reports
        """
        pass

    def test_submit_received_messages_detail(self):
        """
        Test case for submit_received_messages_detail

        Submits a request to generate an async detail report
        """
        pass

    def test_submit_received_messages_summary(self):
        """
        Test case for submit_received_messages_summary

        Submits a summarised report of received messages
        """
        pass

    def test_submit_sent_messages_detail(self):
        """
        Test case for submit_sent_messages_detail

        Submits a request to generate an async detail report
        """
        pass

    def test_submit_sent_messages_summary(self):
        """
        Test case for submit_sent_messages_summary

        Submits a summarised report of sent messages
        """
        pass


if __name__ == '__main__':
    unittest.main()
