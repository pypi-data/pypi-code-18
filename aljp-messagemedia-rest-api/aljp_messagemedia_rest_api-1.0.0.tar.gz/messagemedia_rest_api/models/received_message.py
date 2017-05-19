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


class ReceivedMessage(object):
    """
    Do not edit the class manually.
    """
    def __init__(self, account=None, action=None, content=None, destination_address=None, destination_address_country=None, format=None, id=None, in_response_to=None, metadata=None, source_address=None, source_address_country=None, timestamp=None):
        """
        ReceivedMessage - a model

        :param dict types: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.types = {
            'account': 'str',
            'action': 'str',
            'content': 'str',
            'destination_address': 'str',
            'destination_address_country': 'str',
            'format': 'str',
            'id': 'str',
            'in_response_to': 'str',
            'metadata': 'object',
            'source_address': 'str',
            'source_address_country': 'str',
            'timestamp': 'datetime'
        }

        self.attribute_map = {
            'account': 'account',
            'action': 'action',
            'content': 'content',
            'destination_address': 'destination_address',
            'destination_address_country': 'destination_address_country',
            'format': 'format',
            'id': 'id',
            'in_response_to': 'in_response_to',
            'metadata': 'metadata',
            'source_address': 'source_address',
            'source_address_country': 'source_address_country',
            'timestamp': 'timestamp'
        }

        self._account = account
        self._action = action
        self._content = content
        self._destination_address = destination_address
        self._destination_address_country = destination_address_country
        self._format = format
        self._id = id
        self._in_response_to = in_response_to
        self._metadata = metadata
        self._source_address = source_address
        self._source_address_country = source_address_country
        self._timestamp = timestamp

    @property
    def account(self):
        """
        Gets the account of this ReceivedMessage.
        Account associated with this message

        :return: The account of this ReceivedMessage.
        :rtype: str
        """
        return self._account

    @account.setter
    def account(self, account):
        """
        Sets the account of this ReceivedMessage.
        Account associated with this message

        :param account: The account of this ReceivedMessage.
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
    def action(self):
        """
        Gets the action of this ReceivedMessage.
        Action that was invoked for this message if any, OPTOUT, OPTIN, GLOBALOPTOUT

        :return: The action of this ReceivedMessage.
        :rtype: str
        """
        return self._action

    @action.setter
    def action(self, action):
        """
        Sets the action of this ReceivedMessage.
        Action that was invoked for this message if any, OPTOUT, OPTIN, GLOBALOPTOUT

        :param action: The action of this ReceivedMessage.
        :type: str
        """
        allowed_values = ["OPTOUT", "OPTIN", "GLOBALOPTOUT"]
        if action not in allowed_values:
            raise ValueError(
                "Invalid value for `action` ({0}), must be one of {1}"
                .format(action, allowed_values)
            )

        self._action = action

    @property
    def content(self):
        """
        Gets the content of this ReceivedMessage.
        Content of the message

        :return: The content of this ReceivedMessage.
        :rtype: str
        """
        return self._content

    @content.setter
    def content(self, content):
        """
        Sets the content of this ReceivedMessage.
        Content of the message

        :param content: The content of this ReceivedMessage.
        :type: str
        """

        self._content = content

    @property
    def destination_address(self):
        """
        Gets the destination_address of this ReceivedMessage.
        Address this message was delivered to. If this message was received in response to a sent message, this is the source address of the sent message

        :return: The destination_address of this ReceivedMessage.
        :rtype: str
        """
        return self._destination_address

    @destination_address.setter
    def destination_address(self, destination_address):
        """
        Sets the destination_address of this ReceivedMessage.
        Address this message was delivered to. If this message was received in response to a sent message, this is the source address of the sent message

        :param destination_address: The destination_address of this ReceivedMessage.
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
        Gets the destination_address_country of this ReceivedMessage.
        Country associated with the destination address

        :return: The destination_address_country of this ReceivedMessage.
        :rtype: str
        """
        return self._destination_address_country

    @destination_address_country.setter
    def destination_address_country(self, destination_address_country):
        """
        Sets the destination_address_country of this ReceivedMessage.
        Country associated with the destination address

        :param destination_address_country: The destination_address_country of this ReceivedMessage.
        :type: str
        """

        self._destination_address_country = destination_address_country

    @property
    def format(self):
        """
        Gets the format of this ReceivedMessage.
        Format of message, SMS or TTS (Text To Speech)

        :return: The format of this ReceivedMessage.
        :rtype: str
        """
        return self._format

    @format.setter
    def format(self, format):
        """
        Sets the format of this ReceivedMessage.
        Format of message, SMS or TTS (Text To Speech)

        :param format: The format of this ReceivedMessage.
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
        Gets the id of this ReceivedMessage.
        Unique ID for this reply

        :return: The id of this ReceivedMessage.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ReceivedMessage.
        Unique ID for this reply

        :param id: The id of this ReceivedMessage.
        :type: str
        """

        self._id = id

    @property
    def in_response_to(self):
        """
        Gets the in_response_to of this ReceivedMessage.
        If this message was received in response to a sent message, this is the ID of the sent message

        :return: The in_response_to of this ReceivedMessage.
        :rtype: str
        """
        return self._in_response_to

    @in_response_to.setter
    def in_response_to(self, in_response_to):
        """
        Sets the in_response_to of this ReceivedMessage.
        If this message was received in response to a sent message, this is the ID of the sent message

        :param in_response_to: The in_response_to of this ReceivedMessage.
        :type: str
        """

        self._in_response_to = in_response_to

    @property
    def metadata(self):
        """
        Gets the metadata of this ReceivedMessage.
        If this message was received in response to a sent message, this is the metadata associated with the sent message

        :return: The metadata of this ReceivedMessage.
        :rtype: object
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this ReceivedMessage.
        If this message was received in response to a sent message, this is the metadata associated with the sent message

        :param metadata: The metadata of this ReceivedMessage.
        :type: object
        """

        self._metadata = metadata

    @property
    def source_address(self):
        """
        Gets the source_address of this ReceivedMessage.
        Address this message was received from. If this message was received in response to a sent message, this is the destination address of the sent message.

        :return: The source_address of this ReceivedMessage.
        :rtype: str
        """
        return self._source_address

    @source_address.setter
    def source_address(self, source_address):
        """
        Sets the source_address of this ReceivedMessage.
        Address this message was received from. If this message was received in response to a sent message, this is the destination address of the sent message.

        :param source_address: The source_address of this ReceivedMessage.
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
        Gets the source_address_country of this ReceivedMessage.
        Country associated with the source address

        :return: The source_address_country of this ReceivedMessage.
        :rtype: str
        """
        return self._source_address_country

    @source_address_country.setter
    def source_address_country(self, source_address_country):
        """
        Sets the source_address_country of this ReceivedMessage.
        Country associated with the source address

        :param source_address_country: The source_address_country of this ReceivedMessage.
        :type: str
        """

        self._source_address_country = source_address_country

    @property
    def timestamp(self):
        """
        Gets the timestamp of this ReceivedMessage.
        Date time at which this message was received

        :return: The timestamp of this ReceivedMessage.
        :rtype: datetime
        """
        return self._timestamp

    @timestamp.setter
    def timestamp(self, timestamp):
        """
        Sets the timestamp of this ReceivedMessage.
        Date time at which this message was received

        :param timestamp: The timestamp of this ReceivedMessage.
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
