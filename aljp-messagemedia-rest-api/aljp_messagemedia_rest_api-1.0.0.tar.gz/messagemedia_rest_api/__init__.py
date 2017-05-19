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

# import models into sdk package
from .models.accounts_body import AccountsBody
from .models.action_body import ActionBody
from .models.async_delivery_report_detail_request import AsyncDeliveryReportDetailRequest
from .models.async_delivery_reports_summary_request import AsyncDeliveryReportsSummaryRequest
from .models.async_delivery_sent_messages_request import AsyncDeliverySentMessagesRequest
from .models.async_received_messages_detail_request import AsyncReceivedMessagesDetailRequest
from .models.async_received_messages_summary_request import AsyncReceivedMessagesSummaryRequest
from .models.async_report import AsyncReport
from .models.async_report_response import AsyncReportResponse
from .models.async_sent_messages_detail_request import AsyncSentMessagesDetailRequest
from .models.delivery_options_body import DeliveryOptionsBody
from .models.delivery_options_body_inner import DeliveryOptionsBodyInner
from .models.delivery_report import DeliveryReport
from .models.delivery_report_body import DeliveryReportBody
from .models.delivery_report_id import DeliveryReportId
from .models.delivery_reports import DeliveryReports
from .models.destination_address_body import DestinationAddressBody
from .models.destination_address_country_body import DestinationAddressCountryBody
from .models.end_date_body import EndDateBody
from .models.inline_response_200 import InlineResponse200
from .models.inline_response_400 import InlineResponse400
from .models.message_format_body import MessageFormatBody
from .models.message_status_code import MessageStatusCode
from .models.messages import Messages
from .models.metadata_key_body import MetadataKeyBody
from .models.metadata_keys_response import MetadataKeysResponse
from .models.metadata_keys_response_properties import MetadataKeysResponseProperties
from .models.metadata_value_body import MetadataValueBody
from .models.new_message import NewMessage
from .models.pagination import Pagination
from .models.received_message import ReceivedMessage
from .models.received_messages import ReceivedMessages
from .models.replies import Replies
from .models.reply import Reply
from .models.reply_id import ReplyId
from .models.reply_vendor_account_id import ReplyVendorAccountId
from .models.report import Report
from .models.reporting_detail_properties import ReportingDetailProperties
from .models.reporting_detail_properties_filters import ReportingDetailPropertiesFilters
from .models.reporting_detail_properties_sorting import ReportingDetailPropertiesSorting
from .models.reports import Reports
from .models.sent_message import SentMessage
from .models.sent_messages import SentMessages
from .models.sort_direction_body import SortDirectionBody
from .models.source_address_body import SourceAddressBody
from .models.source_address_country_body import SourceAddressCountryBody
from .models.start_date_body import StartDateBody
from .models.status import Status
from .models.status_body import StatusBody
from .models.status_code_body import StatusCodeBody
from .models.submitted_message import SubmittedMessage
from .models.submitted_messages import SubmittedMessages
from .models.summary_by_body import SummaryByBody
from .models.summary_field_body import SummaryFieldBody
from .models.summary_report import SummaryReport
from .models.summary_report_data import SummaryReportData
from .models.summary_report_properties import SummaryReportProperties
from .models.timezone_body import TimezoneBody

# import apis into sdk package
from .apis.delivery_reports_api import DeliveryReportsApi
from .apis.messaging_api import MessagingApi
from .apis.messaging_reports_api import MessagingReportsApi
from .apis.replies_api import RepliesApi

# import ApiClient
from .api_client import ApiClient

from .configuration import Configuration

configuration = Configuration()
