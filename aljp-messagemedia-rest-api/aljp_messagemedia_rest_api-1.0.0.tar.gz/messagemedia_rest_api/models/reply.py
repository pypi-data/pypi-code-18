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


class Reply(object):
    """
    Do not edit the class manually.
    """
    def __init__(self, callback_url=None, content=None, date_received=None, destination_number=None, message_id=None, metadata=None, reply_id=None, source_number=None, vendor_account_id=None):
        """
        Reply - a model

        :param dict types: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.types = {
            'callback_url': 'str',
            'content': 'str',
            'date_received': 'datetime',
            'destination_number': 'str',
            'message_id': 'str',
            'metadata': 'object',
            'reply_id': 'str',
            'source_number': 'str',
            'vendor_account_id': 'ReplyVendorAccountId'
        }

        self.attribute_map = {
            'callback_url': 'callback_url',
            'content': 'content',
            'date_received': 'date_received',
            'destination_number': 'destination_number',
            'message_id': 'message_id',
            'metadata': 'metadata',
            'reply_id': 'reply_id',
            'source_number': 'source_number',
            'vendor_account_id': 'vendor_account_id'
        }

        self._callback_url = callback_url
        self._content = content
        self._date_received = date_received
        self._destination_number = destination_number
        self._message_id = message_id
        self._metadata = metadata
        self._reply_id = reply_id
        self._source_number = source_number
        self._vendor_account_id = vendor_account_id

    @property
    def callback_url(self):
        """
        Gets the callback_url of this Reply.
        The URL specified as the callback URL in the original submit message request

        :return: The callback_url of this Reply.
        :rtype: str
        """
        return self._callback_url

    @callback_url.setter
    def callback_url(self, callback_url):
        """
        Sets the callback_url of this Reply.
        The URL specified as the callback URL in the original submit message request

        :param callback_url: The callback_url of this Reply.
        :type: str
        """

        self._callback_url = callback_url

    @property
    def content(self):
        """
        Gets the content of this Reply.
        Content of the reply

        :return: The content of this Reply.
        :rtype: str
        """
        return self._content

    @content.setter
    def content(self, content):
        """
        Sets the content of this Reply.
        Content of the reply

        :param content: The content of this Reply.
        :type: str
        """

        if not content:
            raise ValueError("Invalid value for `content`, must not be `None`")
        if len(content) > 5000:
            raise ValueError("Invalid value for `content`, length must be less than `5000`")
        if len(content) < 1:
            raise ValueError("Invalid value for `content`, length must be greater than or equal to `1`")

        self._content = content

    @property
    def date_received(self):
        """
        Gets the date_received of this Reply.
        Date time when the reply was received

        :return: The date_received of this Reply.
        :rtype: datetime
        """
        return self._date_received

    @date_received.setter
    def date_received(self, date_received):
        """
        Sets the date_received of this Reply.
        Date time when the reply was received

        :param date_received: The date_received of this Reply.
        :type: datetime
        """

        self._date_received = date_received

    @property
    def destination_number(self):
        """
        Gets the destination_number of this Reply.
        Address from which this reply was sent to

        :return: The destination_number of this Reply.
        :rtype: str
        """
        return self._destination_number

    @destination_number.setter
    def destination_number(self, destination_number):
        """
        Sets the destination_number of this Reply.
        Address from which this reply was sent to

        :param destination_number: The destination_number of this Reply.
        :type: str
        """

        if not destination_number:
            raise ValueError("Invalid value for `destination_number`, must not be `None`")
        if len(destination_number) > 15:
            raise ValueError("Invalid value for `destination_number`, length must be less than `15`")
        if len(destination_number) < 1:
            raise ValueError("Invalid value for `destination_number`, length must be greater than or equal to `1`")

        self._destination_number = destination_number

    @property
    def message_id(self):
        """
        Gets the message_id of this Reply.
        Unique ID of the original message

        :return: The message_id of this Reply.
        :rtype: str
        """
        return self._message_id

    @message_id.setter
    def message_id(self, message_id):
        """
        Sets the message_id of this Reply.
        Unique ID of the original message

        :param message_id: The message_id of this Reply.
        :type: str
        """

        self._message_id = message_id

    @property
    def metadata(self):
        """
        Gets the metadata of this Reply.
        Any metadata that was included in the original submit message request

        :return: The metadata of this Reply.
        :rtype: object
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this Reply.
        Any metadata that was included in the original submit message request

        :param metadata: The metadata of this Reply.
        :type: object
        """

        self._metadata = metadata

    @property
    def reply_id(self):
        """
        Gets the reply_id of this Reply.
        Unique ID of this reply

        :return: The reply_id of this Reply.
        :rtype: str
        """
        return self._reply_id

    @reply_id.setter
    def reply_id(self, reply_id):
        """
        Sets the reply_id of this Reply.
        Unique ID of this reply

        :param reply_id: The reply_id of this Reply.
        :type: str
        """

        self._reply_id = reply_id

    @property
    def source_number(self):
        """
        Gets the source_number of this Reply.
        Address from which this reply was received from

        :return: The source_number of this Reply.
        :rtype: str
        """
        return self._source_number

    @source_number.setter
    def source_number(self, source_number):
        """
        Sets the source_number of this Reply.
        Address from which this reply was received from

        :param source_number: The source_number of this Reply.
        :type: str
        """

        if not source_number:
            raise ValueError("Invalid value for `source_number`, must not be `None`")
        if len(source_number) > 15:
            raise ValueError("Invalid value for `source_number`, length must be less than `15`")
        if len(source_number) < 1:
            raise ValueError("Invalid value for `source_number`, length must be greater than or equal to `1`")

        self._source_number = source_number

    @property
    def vendor_account_id(self):
        """
        Gets the vendor_account_id of this Reply.


        :return: The vendor_account_id of this Reply.
        :rtype: ReplyVendorAccountId
        """
        return self._vendor_account_id

    @vendor_account_id.setter
    def vendor_account_id(self, vendor_account_id):
        """
        Sets the vendor_account_id of this Reply.


        :param vendor_account_id: The vendor_account_id of this Reply.
        :type: ReplyVendorAccountId
        """

        self._vendor_account_id = vendor_account_id

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
