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

from pprint import pformat
from six import iteritems
import re


class AsyncDeliveryReportsSummaryRequest(object):
    """
    Do not edit the class manually.
    """
    def __init__(self, summary_by=None, summary_field=None, group_by=None, start_date=None, end_date=None, timezone=None, accounts=None, destination_address_country=None, destination_address=None, message_format=None, metadata_key=None, metadata_value=None, source_address_country=None, source_address=None, status=None, status_code=None, delivery_options=None):
        """
        AsyncDeliveryReportsSummaryRequest - a model

        :param dict types: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.types = {
            'summary_by': 'SummaryByBody',
            'summary_field': 'SummaryFieldBody',
            'group_by': 'str',
            'start_date': 'StartDateBody',
            'end_date': 'EndDateBody',
            'timezone': 'TimezoneBody',
            'accounts': 'AccountsBody',
            'destination_address_country': 'DestinationAddressCountryBody',
            'destination_address': 'DestinationAddressBody',
            'message_format': 'MessageFormatBody',
            'metadata_key': 'MetadataKeyBody',
            'metadata_value': 'MetadataValueBody',
            'source_address_country': 'SourceAddressCountryBody',
            'source_address': 'SourceAddressBody',
            'status': 'StatusBody',
            'status_code': 'StatusCodeBody',
            'delivery_options': 'DeliveryOptionsBody'
        }

        self.attribute_map = {
            'summary_by': 'summary_by',
            'summary_field': 'summary_field',
            'group_by': 'group_by',
            'start_date': 'start_date',
            'end_date': 'end_date',
            'timezone': 'timezone',
            'accounts': 'accounts',
            'destination_address_country': 'destination_address_country',
            'destination_address': 'destination_address',
            'message_format': 'message_format',
            'metadata_key': 'metadata_key',
            'metadata_value': 'metadata_value',
            'source_address_country': 'source_address_country',
            'source_address': 'source_address',
            'status': 'status',
            'status_code': 'status_code',
            'delivery_options': 'delivery_options'
        }

        self._summary_by = summary_by
        self._summary_field = summary_field
        self._group_by = group_by
        self._start_date = start_date
        self._end_date = end_date
        self._timezone = timezone
        self._accounts = accounts
        self._destination_address_country = destination_address_country
        self._destination_address = destination_address
        self._message_format = message_format
        self._metadata_key = metadata_key
        self._metadata_value = metadata_value
        self._source_address_country = source_address_country
        self._source_address = source_address
        self._status = status
        self._status_code = status_code
        self._delivery_options = delivery_options

    @property
    def summary_by(self):
        """
        Gets the summary_by of this AsyncDeliveryReportsSummaryRequest.


        :return: The summary_by of this AsyncDeliveryReportsSummaryRequest.
        :rtype: SummaryByBody
        """
        return self._summary_by

    @summary_by.setter
    def summary_by(self, summary_by):
        """
        Sets the summary_by of this AsyncDeliveryReportsSummaryRequest.


        :param summary_by: The summary_by of this AsyncDeliveryReportsSummaryRequest.
        :type: SummaryByBody
        """

        self._summary_by = summary_by

    @property
    def summary_field(self):
        """
        Gets the summary_field of this AsyncDeliveryReportsSummaryRequest.


        :return: The summary_field of this AsyncDeliveryReportsSummaryRequest.
        :rtype: SummaryFieldBody
        """
        return self._summary_field

    @summary_field.setter
    def summary_field(self, summary_field):
        """
        Sets the summary_field of this AsyncDeliveryReportsSummaryRequest.


        :param summary_field: The summary_field of this AsyncDeliveryReportsSummaryRequest.
        :type: SummaryFieldBody
        """

        self._summary_field = summary_field

    @property
    def group_by(self):
        """
        Gets the group_by of this AsyncDeliveryReportsSummaryRequest.
        Field to group results set by

        :return: The group_by of this AsyncDeliveryReportsSummaryRequest.
        :rtype: str
        """
        return self._group_by

    @group_by.setter
    def group_by(self, group_by):
        """
        Sets the group_by of this AsyncDeliveryReportsSummaryRequest.
        Field to group results set by

        :param group_by: The group_by of this AsyncDeliveryReportsSummaryRequest.
        :type: str
        """
        allowed_values = ["DAY", "DESTINATION_ADDRESS", "DESTINATION_ADDRESS_COUNTRY", "FORMAT", "HOUR", "METADATA_KEY", "METADATA_VALUE", "MINUTE", "MONTH", "SOURCE_ADDRESS", "SOURCE_ADDRESS_COUNTRY", "STATUS", "STATUS_CODE", "YEAR"]
        if group_by not in allowed_values:
            raise ValueError(
                "Invalid value for `group_by` ({0}), must be one of {1}"
                .format(group_by, allowed_values)
            )

        self._group_by = group_by

    @property
    def start_date(self):
        """
        Gets the start_date of this AsyncDeliveryReportsSummaryRequest.


        :return: The start_date of this AsyncDeliveryReportsSummaryRequest.
        :rtype: StartDateBody
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """
        Sets the start_date of this AsyncDeliveryReportsSummaryRequest.


        :param start_date: The start_date of this AsyncDeliveryReportsSummaryRequest.
        :type: StartDateBody
        """

        self._start_date = start_date

    @property
    def end_date(self):
        """
        Gets the end_date of this AsyncDeliveryReportsSummaryRequest.


        :return: The end_date of this AsyncDeliveryReportsSummaryRequest.
        :rtype: EndDateBody
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """
        Sets the end_date of this AsyncDeliveryReportsSummaryRequest.


        :param end_date: The end_date of this AsyncDeliveryReportsSummaryRequest.
        :type: EndDateBody
        """

        self._end_date = end_date

    @property
    def timezone(self):
        """
        Gets the timezone of this AsyncDeliveryReportsSummaryRequest.


        :return: The timezone of this AsyncDeliveryReportsSummaryRequest.
        :rtype: TimezoneBody
        """
        return self._timezone

    @timezone.setter
    def timezone(self, timezone):
        """
        Sets the timezone of this AsyncDeliveryReportsSummaryRequest.


        :param timezone: The timezone of this AsyncDeliveryReportsSummaryRequest.
        :type: TimezoneBody
        """

        self._timezone = timezone

    @property
    def accounts(self):
        """
        Gets the accounts of this AsyncDeliveryReportsSummaryRequest.


        :return: The accounts of this AsyncDeliveryReportsSummaryRequest.
        :rtype: AccountsBody
        """
        return self._accounts

    @accounts.setter
    def accounts(self, accounts):
        """
        Sets the accounts of this AsyncDeliveryReportsSummaryRequest.


        :param accounts: The accounts of this AsyncDeliveryReportsSummaryRequest.
        :type: AccountsBody
        """

        self._accounts = accounts

    @property
    def destination_address_country(self):
        """
        Gets the destination_address_country of this AsyncDeliveryReportsSummaryRequest.


        :return: The destination_address_country of this AsyncDeliveryReportsSummaryRequest.
        :rtype: DestinationAddressCountryBody
        """
        return self._destination_address_country

    @destination_address_country.setter
    def destination_address_country(self, destination_address_country):
        """
        Sets the destination_address_country of this AsyncDeliveryReportsSummaryRequest.


        :param destination_address_country: The destination_address_country of this AsyncDeliveryReportsSummaryRequest.
        :type: DestinationAddressCountryBody
        """

        self._destination_address_country = destination_address_country

    @property
    def destination_address(self):
        """
        Gets the destination_address of this AsyncDeliveryReportsSummaryRequest.


        :return: The destination_address of this AsyncDeliveryReportsSummaryRequest.
        :rtype: DestinationAddressBody
        """
        return self._destination_address

    @destination_address.setter
    def destination_address(self, destination_address):
        """
        Sets the destination_address of this AsyncDeliveryReportsSummaryRequest.


        :param destination_address: The destination_address of this AsyncDeliveryReportsSummaryRequest.
        :type: DestinationAddressBody
        """

        self._destination_address = destination_address

    @property
    def message_format(self):
        """
        Gets the message_format of this AsyncDeliveryReportsSummaryRequest.


        :return: The message_format of this AsyncDeliveryReportsSummaryRequest.
        :rtype: MessageFormatBody
        """
        return self._message_format

    @message_format.setter
    def message_format(self, message_format):
        """
        Sets the message_format of this AsyncDeliveryReportsSummaryRequest.


        :param message_format: The message_format of this AsyncDeliveryReportsSummaryRequest.
        :type: MessageFormatBody
        """

        self._message_format = message_format

    @property
    def metadata_key(self):
        """
        Gets the metadata_key of this AsyncDeliveryReportsSummaryRequest.


        :return: The metadata_key of this AsyncDeliveryReportsSummaryRequest.
        :rtype: MetadataKeyBody
        """
        return self._metadata_key

    @metadata_key.setter
    def metadata_key(self, metadata_key):
        """
        Sets the metadata_key of this AsyncDeliveryReportsSummaryRequest.


        :param metadata_key: The metadata_key of this AsyncDeliveryReportsSummaryRequest.
        :type: MetadataKeyBody
        """

        self._metadata_key = metadata_key

    @property
    def metadata_value(self):
        """
        Gets the metadata_value of this AsyncDeliveryReportsSummaryRequest.


        :return: The metadata_value of this AsyncDeliveryReportsSummaryRequest.
        :rtype: MetadataValueBody
        """
        return self._metadata_value

    @metadata_value.setter
    def metadata_value(self, metadata_value):
        """
        Sets the metadata_value of this AsyncDeliveryReportsSummaryRequest.


        :param metadata_value: The metadata_value of this AsyncDeliveryReportsSummaryRequest.
        :type: MetadataValueBody
        """

        self._metadata_value = metadata_value

    @property
    def source_address_country(self):
        """
        Gets the source_address_country of this AsyncDeliveryReportsSummaryRequest.


        :return: The source_address_country of this AsyncDeliveryReportsSummaryRequest.
        :rtype: SourceAddressCountryBody
        """
        return self._source_address_country

    @source_address_country.setter
    def source_address_country(self, source_address_country):
        """
        Sets the source_address_country of this AsyncDeliveryReportsSummaryRequest.


        :param source_address_country: The source_address_country of this AsyncDeliveryReportsSummaryRequest.
        :type: SourceAddressCountryBody
        """

        self._source_address_country = source_address_country

    @property
    def source_address(self):
        """
        Gets the source_address of this AsyncDeliveryReportsSummaryRequest.


        :return: The source_address of this AsyncDeliveryReportsSummaryRequest.
        :rtype: SourceAddressBody
        """
        return self._source_address

    @source_address.setter
    def source_address(self, source_address):
        """
        Sets the source_address of this AsyncDeliveryReportsSummaryRequest.


        :param source_address: The source_address of this AsyncDeliveryReportsSummaryRequest.
        :type: SourceAddressBody
        """

        self._source_address = source_address

    @property
    def status(self):
        """
        Gets the status of this AsyncDeliveryReportsSummaryRequest.


        :return: The status of this AsyncDeliveryReportsSummaryRequest.
        :rtype: StatusBody
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this AsyncDeliveryReportsSummaryRequest.


        :param status: The status of this AsyncDeliveryReportsSummaryRequest.
        :type: StatusBody
        """

        self._status = status

    @property
    def status_code(self):
        """
        Gets the status_code of this AsyncDeliveryReportsSummaryRequest.


        :return: The status_code of this AsyncDeliveryReportsSummaryRequest.
        :rtype: StatusCodeBody
        """
        return self._status_code

    @status_code.setter
    def status_code(self, status_code):
        """
        Sets the status_code of this AsyncDeliveryReportsSummaryRequest.


        :param status_code: The status_code of this AsyncDeliveryReportsSummaryRequest.
        :type: StatusCodeBody
        """

        self._status_code = status_code

    @property
    def delivery_options(self):
        """
        Gets the delivery_options of this AsyncDeliveryReportsSummaryRequest.


        :return: The delivery_options of this AsyncDeliveryReportsSummaryRequest.
        :rtype: DeliveryOptionsBody
        """
        return self._delivery_options

    @delivery_options.setter
    def delivery_options(self, delivery_options):
        """
        Sets the delivery_options of this AsyncDeliveryReportsSummaryRequest.


        :param delivery_options: The delivery_options of this AsyncDeliveryReportsSummaryRequest.
        :type: DeliveryOptionsBody
        """

        self._delivery_options = delivery_options

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.types):
            value = getattr(self, attr)
            if isinstance(value, list):
                result[attr] = list(map(
                    lambda x: x.to_dict() if hasattr(x, "to_dict") else x,
                    value
                ))
            elif hasattr(value, "to_dict"):
                result[attr] = value.to_dict()
            elif isinstance(value, dict):
                result[attr] = dict(map(
                    lambda item: (item[0], item[1].to_dict())
                    if hasattr(item[1], "to_dict") else item,
                    value.items()
                ))
            else:
                result[attr] = value

        return result

    def to_str(self):
        """
        Returns the string representation of the model
        """
        return pformat(self.to_dict())

    def __repr__(self):
        """
        For `print` and `pprint`
        """
        return self.to_str()

    def __eq__(self, other):
        """
        Returns true if both objects are equal
        """
        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
