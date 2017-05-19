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


class DeliveryReport(object):
    """
    Do not edit the class manually.
    """
    def __init__(self, account=None, destination_address=None, destination_address_country=None, format=None, id=None, in_response_to=None, metadata=None, source_address=None, source_address_country=None, status=None, status_code=None, timestamp=None):
        """
        DeliveryReport - a model

        :param dict types: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.types = {
            'account': 'str',
            'destination_address': 'str',
            'destination_address_country': 'str',
            'format': 'str',
            'id': 'str',
            'in_response_to': 'str',
            'metadata': 'object',
            'source_address': 'str',
            'source_address_country': 'str',
            'status': 'str',
            'status_code': 'MessageStatusCode',
            'timestamp': 'datetime'
        }

        self.attribute_map = {
            'account': 'account',
            'destination_address': 'destination_address',
            'destination_address_country': 'destination_address_country',
            'format': 'format',
            'id': 'id',
            'in_response_to': 'in_response_to',
            'metadata': 'metadata',
            'source_address': 'source_address',
            'source_address_country': 'source_address_country',
            'status': 'status',
            'status_code': 'status_code',
            'timestamp': 'timestamp'
        }

        self._account = account
        self._destination_address = destination_address
        self._destination_address_country = destination_address_country
        self._format = format
        self._id = id
        self._in_response_to = in_response_to
        self._metadata = metadata
        self._source_address = source_address
        self._source_address_country = source_address_country
        self._status = status
        self._status_code = status_code
        self._timestamp = timestamp

    @property
    def account(self):
        """
        Gets the account of this DeliveryReport.
        Account associated with this delivery report

        :return: The account of this DeliveryReport.
        :rtype: str
        """
        return self._account

    @account.setter
    def account(self, account):
        """
        Sets the account of this DeliveryReport.
        Account associated with this delivery report

        :param account: The account of this DeliveryReport.
        :type: str
        """

        if not account:
            raise ValueError("Invalid value for `account`, must not be `None`")
        if len(account) > 200:
            raise ValueError("Invalid value for `account`, length must be less than `200`")
        if len(account) < 1:
            raise ValueError("Invalid value for `account`, length must be greater than or equal to `1`")

        self._account = account

    @property
    def destination_address(self):
        """
        Gets the destination_address of this DeliveryReport.
        Address this delivery report was delivered to. This is the source address of the sent message that this delivery report is in response to

        :return: The destination_address of this DeliveryReport.
        :rtype: str
        """
        return self._destination_address

    @destination_address.setter
    def destination_address(self, destination_address):
        """
        Sets the destination_address of this DeliveryReport.
        Address this delivery report was delivered to. This is the source address of the sent message that this delivery report is in response to

        :param destination_address: The destination_address of this DeliveryReport.
        :type: str
        """

        if not destination_address:
            raise ValueError("Invalid value for `destination_address`, must not be `None`")
        if len(destination_address) > 15:
            raise ValueError("Invalid value for `destination_address`, length must be less than `15`")
        if len(destination_address) < 1:
            raise ValueError("Invalid value for `destination_address`, length must be greater than or equal to `1`")

        self._destination_address = destination_address

    @property
    def destination_address_country(self):
        """
        Gets the destination_address_country of this DeliveryReport.
        Country associated with the destination address

        :return: The destination_address_country of this DeliveryReport.
        :rtype: str
        """
        return self._destination_address_country

    @destination_address_country.setter
    def destination_address_country(self, destination_address_country):
        """
        Sets the destination_address_country of this DeliveryReport.
        Country associated with the destination address

        :param destination_address_country: The destination_address_country of this DeliveryReport.
        :type: str
        """

        self._destination_address_country = destination_address_country

    @property
    def format(self):
        """
        Gets the format of this DeliveryReport.
        Format of message, SMS or TTS (Text To Speech)

        :return: The format of this DeliveryReport.
        :rtype: str
        """
        return self._format

    @format.setter
    def format(self, format):
        """
        Sets the format of this DeliveryReport.
        Format of message, SMS or TTS (Text To Speech)

        :param format: The format of this DeliveryReport.
        :type: str
        """
        allowed_values = ["SMS", "TTS"]
        if format not in allowed_values:
            raise ValueError(
                "Invalid value for `format` ({0}), must be one of {1}"
                .format(format, allowed_values)
            )

        self._format = format

    @property
    def id(self):
        """
        Gets the id of this DeliveryReport.
        Unique ID for this delivery report

        :return: The id of this DeliveryReport.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this DeliveryReport.
        Unique ID for this delivery report

        :param id: The id of this DeliveryReport.
        :type: str
        """

        self._id = id

    @property
    def in_response_to(self):
        """
        Gets the in_response_to of this DeliveryReport.
        Unique ID of the sent message that this delivery report is in response to

        :return: The in_response_to of this DeliveryReport.
        :rtype: str
        """
        return self._in_response_to

    @in_response_to.setter
    def in_response_to(self, in_response_to):
        """
        Sets the in_response_to of this DeliveryReport.
        Unique ID of the sent message that this delivery report is in response to

        :param in_response_to: The in_response_to of this DeliveryReport.
        :type: str
        """

        self._in_response_to = in_response_to

    @property
    def metadata(self):
        """
        Gets the metadata of this DeliveryReport.
        Metadata associated with the sent message

        :return: The metadata of this DeliveryReport.
        :rtype: object
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this DeliveryReport.
        Metadata associated with the sent message

        :param metadata: The metadata of this DeliveryReport.
        :type: object
        """

        self._metadata = metadata

    @property
    def source_address(self):
        """
        Gets the source_address of this DeliveryReport.
        Address this delivery report was received from, the destination address of the sent message that this delivery report is in response to

        :return: The source_address of this DeliveryReport.
        :rtype: str
        """
        return self._source_address

    @source_address.setter
    def source_address(self, source_address):
        """
        Sets the source_address of this DeliveryReport.
        Address this delivery report was received from, the destination address of the sent message that this delivery report is in response to

        :param source_address: The source_address of this DeliveryReport.
        :type: str
        """

        if not source_address:
            raise ValueError("Invalid value for `source_address`, must not be `None`")
        if len(source_address) > 15:
            raise ValueError("Invalid value for `source_address`, length must be less than `15`")
        if len(source_address) < 1:
            raise ValueError("Invalid value for `source_address`, length must be greater than or equal to `1`")

        self._source_address = source_address

    @property
    def source_address_country(self):
        """
        Gets the source_address_country of this DeliveryReport.
        Country associated with the source address

        :return: The source_address_country of this DeliveryReport.
        :rtype: str
        """
        return self._source_address_country

    @source_address_country.setter
    def source_address_country(self, source_address_country):
        """
        Sets the source_address_country of this DeliveryReport.
        Country associated with the source address

        :param source_address_country: The source_address_country of this DeliveryReport.
        :type: str
        """

        self._source_address_country = source_address_country

    @property
    def status(self):
        """
        Gets the status of this DeliveryReport.
        Status of the message

        :return: The status of this DeliveryReport.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this DeliveryReport.
        Status of the message

        :param status: The status of this DeliveryReport.
        :type: str
        """
        allowed_values = ["queued", "processing", "processed", "scheduled", "cancelled", "enroute", "held", "submitted", "delivered", "expired", "rejected"]
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def status_code(self):
        """
        Gets the status_code of this DeliveryReport.


        :return: The status_code of this DeliveryReport.
        :rtype: MessageStatusCode
        """
        return self._status_code

    @status_code.setter
    def status_code(self, status_code):
        """
        Sets the status_code of this DeliveryReport.


        :param status_code: The status_code of this DeliveryReport.
        :type: MessageStatusCode
        """

        self._status_code = status_code

    @property
    def timestamp(self):
        """
        Gets the timestamp of this DeliveryReport.
        Date time at which this delivery report was received

        :return: The timestamp of this DeliveryReport.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """
        Sets the timestamp of this DeliveryReport.
        Date time at which this delivery report was received

        :param timestamp: The timestamp of this DeliveryReport.
        :type: datetime
        """

        self._timestamp = timestamp

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
