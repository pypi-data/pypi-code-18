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


class SentMessage(object):
    """
    Do not edit the class manually.
    """
    def __init__(self, account=None, content=None, delivered_timestamp=None, delivery_report=None, destination_address=None, destination_address_country=None, format=None, id=None, in_response_to=None, metadata=None, source_address=None, source_address_country=None, units=None, timestamp=None):
        """
        SentMessage - a model

        :param dict types: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.types = {
            'account': 'str',
            'content': 'str',
            'delivered_timestamp': 'datetime',
            'delivery_report': 'bool',
            'destination_address': 'str',
            'destination_address_country': 'str',
            'format': 'str',
            'id': 'str',
            'in_response_to': 'str',
            'metadata': 'object',
            'source_address': 'str',
            'source_address_country': 'str',
            'units': 'int',
            'timestamp': 'datetime'
        }

        self.attribute_map = {
            'account': 'account',
            'content': 'content',
            'delivered_timestamp': 'delivered_timestamp',
            'delivery_report': 'delivery_report',
            'destination_address': 'destination_address',
            'destination_address_country': 'destination_address_country',
            'format': 'format',
            'id': 'id',
            'in_response_to': 'in_response_to',
            'metadata': 'metadata',
            'source_address': 'source_address',
            'source_address_country': 'source_address_country',
            'units': 'units',
            'timestamp': 'timestamp'
        }

        self._account = account
        self._content = content
        self._delivered_timestamp = delivered_timestamp
        self._delivery_report = delivery_report
        self._destination_address = destination_address
        self._destination_address_country = destination_address_country
        self._format = format
        self._id = id
        self._in_response_to = in_response_to
        self._metadata = metadata
        self._source_address = source_address
        self._source_address_country = source_address_country
        self._units = units
        self._timestamp = timestamp

    @property
    def account(self):
        """
        Gets the account of this SentMessage.
        Account associated with this message

        :return: The account of this SentMessage.
        :rtype: str
        """
        return self._account

    @account.setter
    def account(self, account):
        """
        Sets the account of this SentMessage.
        Account associated with this message

        :param account: The account of this SentMessage.
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
    def content(self):
        """
        Gets the content of this SentMessage.
        Content of the message

        :return: The content of this SentMessage.
        :rtype: str
        """
        return self._content

    @content.setter
    def content(self, content):
        """
        Sets the content of this SentMessage.
        Content of the message

        :param content: The content of this SentMessage.
        :type: str
        """

        self._content = content

    @property
    def delivered_timestamp(self):
        """
        Gets the delivered_timestamp of this SentMessage.
        If a delivery report was requested for this message, this is the time at which the message was delivered (or failed to be delivered) to the destination address.

        :return: The delivered_timestamp of this SentMessage.
        :rtype: datetime
        """
        return self._delivered_timestamp

    @delivered_timestamp.setter
    def delivered_timestamp(self, delivered_timestamp):
        """
        Sets the delivered_timestamp of this SentMessage.
        If a delivery report was requested for this message, this is the time at which the message was delivered (or failed to be delivered) to the destination address.

        :param delivered_timestamp: The delivered_timestamp of this SentMessage.
        :type: datetime
        """

        self._delivered_timestamp = delivered_timestamp

    @property
    def delivery_report(self):
        """
        Gets the delivery_report of this SentMessage.
        Indicates if a delivery report was requested for this message

        :return: The delivery_report of this SentMessage.
        :rtype: bool
        """
        return self._delivery_report

    @delivery_report.setter
    def delivery_report(self, delivery_report):
        """
        Sets the delivery_report of this SentMessage.
        Indicates if a delivery report was requested for this message

        :param delivery_report: The delivery_report of this SentMessage.
        :type: bool
        """

        self._delivery_report = delivery_report

    @property
    def destination_address(self):
        """
        Gets the destination_address of this SentMessage.
        Address this message was delivered to

        :return: The destination_address of this SentMessage.
        :rtype: str
        """
        return self._destination_address

    @destination_address.setter
    def destination_address(self, destination_address):
        """
        Sets the destination_address of this SentMessage.
        Address this message was delivered to

        :param destination_address: The destination_address of this SentMessage.
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
        Gets the destination_address_country of this SentMessage.
        Country associated with the destination address

        :return: The destination_address_country of this SentMessage.
        :rtype: str
        """
        return self._destination_address_country

    @destination_address_country.setter
    def destination_address_country(self, destination_address_country):
        """
        Sets the destination_address_country of this SentMessage.
        Country associated with the destination address

        :param destination_address_country: The destination_address_country of this SentMessage.
        :type: str
        """

        self._destination_address_country = destination_address_country

    @property
    def format(self):
        """
        Gets the format of this SentMessage.
        Format of message, SMS or TTS (Text To Speech)

        :return: The format of this SentMessage.
        :rtype: str
        """
        return self._format

    @format.setter
    def format(self, format):
        """
        Sets the format of this SentMessage.
        Format of message, SMS or TTS (Text To Speech)

        :param format: The format of this SentMessage.
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
        Gets the id of this SentMessage.
        Unique ID for this message

        :return: The id of this SentMessage.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this SentMessage.
        Unique ID for this message

        :param id: The id of this SentMessage.
        :type: str
        """

        self._id = id

    @property
    def in_response_to(self):
        """
        Gets the in_response_to of this SentMessage.
        If this message was sent in response to a received message (an auto response message for example) this is the ID of the received message.

        :return: The in_response_to of this SentMessage.
        :rtype: str
        """
        return self._in_response_to

    @in_response_to.setter
    def in_response_to(self, in_response_to):
        """
        Sets the in_response_to of this SentMessage.
        If this message was sent in response to a received message (an auto response message for example) this is the ID of the received message.

        :param in_response_to: The in_response_to of this SentMessage.
        :type: str
        """

        self._in_response_to = in_response_to

    @property
    def metadata(self):
        """
        Gets the metadata of this SentMessage.
        Metadata associated with this message

        :return: The metadata of this SentMessage.
        :rtype: object
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this SentMessage.
        Metadata associated with this message

        :param metadata: The metadata of this SentMessage.
        :type: object
        """

        self._metadata = metadata

    @property
    def source_address(self):
        """
        Gets the source_address of this SentMessage.
        Address this message was sent from

        :return: The source_address of this SentMessage.
        :rtype: str
        """
        return self._source_address

    @source_address.setter
    def source_address(self, source_address):
        """
        Sets the source_address of this SentMessage.
        Address this message was sent from

        :param source_address: The source_address of this SentMessage.
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
        Gets the source_address_country of this SentMessage.
        Country associated with the source address

        :return: The source_address_country of this SentMessage.
        :rtype: str
        """
        return self._source_address_country

    @source_address_country.setter
    def source_address_country(self, source_address_country):
        """
        Sets the source_address_country of this SentMessage.
        Country associated with the source address

        :param source_address_country: The source_address_country of this SentMessage.
        :type: str
        """

        self._source_address_country = source_address_country

    @property
    def units(self):
        """
        Gets the units of this SentMessage.
        The total number of calculated SMS units this message cost. 1 SMS unit is defined as 160 GSM characters, or 153 GSM characters for multi-part messages as some characters are used to concatenate the message on the receiving handset. Messages with one or more non-GSM characters will be submitted using UCS-2 encoding. UCS-2 encoding means the message has a maximum of 70 characters per SMS, or 67 characters for multi-part messages.

        :return: The units of this SentMessage.
        :rtype: int
        """
        return self._units

    @units.setter
    def units(self, units):
        """
        Sets the units of this SentMessage.
        The total number of calculated SMS units this message cost. 1 SMS unit is defined as 160 GSM characters, or 153 GSM characters for multi-part messages as some characters are used to concatenate the message on the receiving handset. Messages with one or more non-GSM characters will be submitted using UCS-2 encoding. UCS-2 encoding means the message has a maximum of 70 characters per SMS, or 67 characters for multi-part messages.

        :param units: The units of this SentMessage.
        :type: int
        """

        self._units = units

    @property
    def timestamp(self):
        """
        Gets the timestamp of this SentMessage.
        Date time at which this message was submitted to the API, refer to the delivered timestamp for the time at which the message was delivered (or failed to be delivered) to the destination address.

        :return: The timestamp of this SentMessage.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """
        Sets the timestamp of this SentMessage.
        Date time at which this message was submitted to the API, refer to the delivered timestamp for the time at which the message was delivered (or failed to be delivered) to the destination address.

        :param timestamp: The timestamp of this SentMessage.
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
