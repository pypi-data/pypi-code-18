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


class ReportingDetailPropertiesFilters(object):
    """
    Do not edit the class manually.
    """
    def __init__(self, delivery_report=None, destination_address_country=None, destination_address=None, message_format=None, metadata_key=None, metadata_value=None, source_address_country=None, source_address=None, status_code=None, status=None, action=None, accounts=None):
        """
        ReportingDetailPropertiesFilters - a model

        :param dict types: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.types = {
            'delivery_report': 'str',
            'destination_address_country': 'str',
            'destination_address': 'str',
            'message_format': 'str',
            'metadata_key': 'str',
            'metadata_value': 'str',
            'source_address_country': 'str',
            'source_address': 'str',
            'status_code': 'str',
            'status': 'str',
            'action': 'str',
            'accounts': 'list[str]'
        }

        self.attribute_map = {
            'delivery_report': 'delivery_report',
            'destination_address_country': 'destination_address_country',
            'destination_address': 'destination_address',
            'message_format': 'message_format',
            'metadata_key': 'metadata_key',
            'metadata_value': 'metadata_value',
            'source_address_country': 'source_address_country',
            'source_address': 'source_address',
            'status_code': 'status_code',
            'status': 'status',
            'action': 'action',
            'accounts': 'accounts'
        }

        self._delivery_report = delivery_report
        self._destination_address_country = destination_address_country
        self._destination_address = destination_address
        self._message_format = message_format
        self._metadata_key = metadata_key
        self._metadata_value = metadata_value
        self._source_address_country = source_address_country
        self._source_address = source_address
        self._status_code = status_code
        self._status = status
        self._action = action
        self._accounts = accounts

    @property
    def delivery_report(self):
        """
        Gets the delivery_report of this ReportingDetailPropertiesFilters.


        :return: The delivery_report of this ReportingDetailPropertiesFilters.
        :rtype: str
        """
        return self._delivery_report

    @delivery_report.setter
    def delivery_report(self, delivery_report):
        """
        Sets the delivery_report of this ReportingDetailPropertiesFilters.


        :param delivery_report: The delivery_report of this ReportingDetailPropertiesFilters.
        :type: str
        """

        self._delivery_report = delivery_report

    @property
    def destination_address_country(self):
        """
        Gets the destination_address_country of this ReportingDetailPropertiesFilters.


        :return: The destination_address_country of this ReportingDetailPropertiesFilters.
        :rtype: str
        """
        return self._destination_address_country

    @destination_address_country.setter
    def destination_address_country(self, destination_address_country):
        """
        Sets the destination_address_country of this ReportingDetailPropertiesFilters.


        :param destination_address_country: The destination_address_country of this ReportingDetailPropertiesFilters.
        :type: str
        """

        self._destination_address_country = destination_address_country

    @property
    def destination_address(self):
        """
        Gets the destination_address of this ReportingDetailPropertiesFilters.


        :return: The destination_address of this ReportingDetailPropertiesFilters.
        :rtype: str
        """
        return self._destination_address

    @destination_address.setter
    def destination_address(self, destination_address):
        """
        Sets the destination_address of this ReportingDetailPropertiesFilters.


        :param destination_address: The destination_address of this ReportingDetailPropertiesFilters.
        :type: str
        """

        self._destination_address = destination_address

    @property
    def message_format(self):
        """
        Gets the message_format of this ReportingDetailPropertiesFilters.


        :return: The message_format of this ReportingDetailPropertiesFilters.
        :rtype: str
        """
        return self._message_format

    @message_format.setter
    def message_format(self, message_format):
        """
        Sets the message_format of this ReportingDetailPropertiesFilters.


        :param message_format: The message_format of this ReportingDetailPropertiesFilters.
        :type: str
        """

        self._message_format = message_format

    @property
    def metadata_key(self):
        """
        Gets the metadata_key of this ReportingDetailPropertiesFilters.


        :return: The metadata_key of this ReportingDetailPropertiesFilters.
        :rtype: str
        """
        return self._metadata_key

    @metadata_key.setter
    def metadata_key(self, metadata_key):
        """
        Sets the metadata_key of this ReportingDetailPropertiesFilters.


        :param metadata_key: The metadata_key of this ReportingDetailPropertiesFilters.
        :type: str
        """

        self._metadata_key = metadata_key

    @property
    def metadata_value(self):
        """
        Gets the metadata_value of this ReportingDetailPropertiesFilters.


        :return: The metadata_value of this ReportingDetailPropertiesFilters.
        :rtype: str
        """
        return self._metadata_value

    @metadata_value.setter
    def metadata_value(self, metadata_value):
        """
        Sets the metadata_value of this ReportingDetailPropertiesFilters.


        :param metadata_value: The metadata_value of this ReportingDetailPropertiesFilters.
        :type: str
        """

        self._metadata_value = metadata_value

    @property
    def source_address_country(self):
        """
        Gets the source_address_country of this ReportingDetailPropertiesFilters.


        :return: The source_address_country of this ReportingDetailPropertiesFilters.
        :rtype: str
        """
        return self._source_address_country

    @source_address_country.setter
    def source_address_country(self, source_address_country):
        """
        Sets the source_address_country of this ReportingDetailPropertiesFilters.


        :param source_address_country: The source_address_country of this ReportingDetailPropertiesFilters.
        :type: str
        """

        self._source_address_country = source_address_country

    @property
    def source_address(self):
        """
        Gets the source_address of this ReportingDetailPropertiesFilters.


        :return: The source_address of this ReportingDetailPropertiesFilters.
        :rtype: str
        """
        return self._source_address

    @source_address.setter
    def source_address(self, source_address):
        """
        Sets the source_address of this ReportingDetailPropertiesFilters.


        :param source_address: The source_address of this ReportingDetailPropertiesFilters.
        :type: str
        """

        self._source_address = source_address

    @property
    def status_code(self):
        """
        Gets the status_code of this ReportingDetailPropertiesFilters.


        :return: The status_code of this ReportingDetailPropertiesFilters.
        :rtype: str
        """
        return self._status_code

    @status_code.setter
    def status_code(self, status_code):
        """
        Sets the status_code of this ReportingDetailPropertiesFilters.


        :param status_code: The status_code of this ReportingDetailPropertiesFilters.
        :type: str
        """

        self._status_code = status_code

    @property
    def status(self):
        """
        Gets the status of this ReportingDetailPropertiesFilters.


        :return: The status of this ReportingDetailPropertiesFilters.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this ReportingDetailPropertiesFilters.


        :param status: The status of this ReportingDetailPropertiesFilters.
        :type: str
        """

        self._status = status

    @property
    def action(self):
        """
        Gets the action of this ReportingDetailPropertiesFilters.


        :return: The action of this ReportingDetailPropertiesFilters.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """
        Sets the action of this ReportingDetailPropertiesFilters.


        :param action: The action of this ReportingDetailPropertiesFilters.
        :type: str
        """

        self._action = action

    @property
    def accounts(self):
        """
        Gets the accounts of this ReportingDetailPropertiesFilters.
        List of accounts that were used to generate this report

        :return: The accounts of this ReportingDetailPropertiesFilters.
        :rtype: list[str]
        """
        return self._accounts

    @accounts.setter
    def accounts(self, accounts):
        """
        Sets the accounts of this ReportingDetailPropertiesFilters.
        List of accounts that were used to generate this report

        :param accounts: The accounts of this ReportingDetailPropertiesFilters.
        :type: list[str]
        """

        self._accounts = accounts

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
