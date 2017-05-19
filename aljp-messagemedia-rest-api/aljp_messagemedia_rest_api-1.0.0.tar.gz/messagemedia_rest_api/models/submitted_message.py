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


class SubmittedMessage(object):
    """
    Do not edit the class manually.
    """
    def __init__(self, callback_url=None, content=None, destination_number=None, delivery_report=False, format=None, message_expiry_timestamp=None, metadata=None, scheduled=None, source_number=None, source_number_type=None, message_id=None, status=None):
        """
        SubmittedMessage - a model

        :param dict types: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.types = {
            'callback_url': 'str',
            'content': 'str',
            'destination_number': 'str',
            'delivery_report': 'bool',
            'format': 'str',
            'message_expiry_timestamp': 'datetime',
            'metadata': 'object',
            'scheduled': 'datetime',
            'source_number': 'str',
            'source_number_type': 'str',
            'message_id': 'str',
            'status': 'str'
        }

        self.attribute_map = {
            'callback_url': 'callback_url',
            'content': 'content',
            'destination_number': 'destination_number',
            'delivery_report': 'delivery_report',
            'format': 'format',
            'message_expiry_timestamp': 'message_expiry_timestamp',
            'metadata': 'metadata',
            'scheduled': 'scheduled',
            'source_number': 'source_number',
            'source_number_type': 'source_number_type',
            'message_id': 'message_id',
            'status': 'status'
        }

        self._callback_url = callback_url
        self._content = content
        self._destination_number = destination_number
        self._delivery_report = delivery_report
        self._format = format
        self._message_expiry_timestamp = message_expiry_timestamp
        self._metadata = metadata
        self._scheduled = scheduled
        self._source_number = source_number
        self._source_number_type = source_number_type
        self._message_id = message_id
        self._status = status

    @property
    def callback_url(self):
        """
        Gets the callback_url of this SubmittedMessage.
        URL replies and delivery reports to this message will be pushed to

        :return: The callback_url of this SubmittedMessage.
        :rtype: str
        """
        return self._callback_url

    @callback_url.setter
    def callback_url(self, callback_url):
        """
        Sets the callback_url of this SubmittedMessage.
        URL replies and delivery reports to this message will be pushed to

        :param callback_url: The callback_url of this SubmittedMessage.
        :type: str
        """

        self._callback_url = callback_url

    @property
    def content(self):
        """
        Gets the content of this SubmittedMessage.
        Content of the message

        :return: The content of this SubmittedMessage.
        :rtype: str
        """
        return self._content

    @content.setter
    def content(self, content):
        """
        Sets the content of this SubmittedMessage.
        Content of the message

        :param content: The content of this SubmittedMessage.
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
    def destination_number(self):
        """
        Gets the destination_number of this SubmittedMessage.
        Destination number of the message

        :return: The destination_number of this SubmittedMessage.
        :rtype: str
        """
        return self._destination_number

    @destination_number.setter
    def destination_number(self, destination_number):
        """
        Sets the destination_number of this SubmittedMessage.
        Destination number of the message

        :param destination_number: The destination_number of this SubmittedMessage.
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
    def delivery_report(self):
        """
        Gets the delivery_report of this SubmittedMessage.
        Request a delivery report for this message

        :return: The delivery_report of this SubmittedMessage.
        :rtype: bool
        """
        return self._delivery_report

    @delivery_report.setter
    def delivery_report(self, delivery_report):
        """
        Sets the delivery_report of this SubmittedMessage.
        Request a delivery report for this message

        :param delivery_report: The delivery_report of this SubmittedMessage.
        :type: bool
        """

        self._delivery_report = delivery_report

    @property
    def format(self):
        """
        Gets the format of this SubmittedMessage.
        Format of message, SMS or TTS (Text To Speech).

        :return: The format of this SubmittedMessage.
        :rtype: str
        """
        return self._format

    @format.setter
    def format(self, format):
        """
        Sets the format of this SubmittedMessage.
        Format of message, SMS or TTS (Text To Speech).

        :param format: The format of this SubmittedMessage.
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
    def message_expiry_timestamp(self):
        """
        Gets the message_expiry_timestamp of this SubmittedMessage.
        Date time after which the message expires and will not be sent

        :return: The message_expiry_timestamp of this SubmittedMessage.
        :rtype: datetime
        """
        return self._message_expiry_timestamp

    @message_expiry_timestamp.setter
    def message_expiry_timestamp(self, message_expiry_timestamp):
        """
        Sets the message_expiry_timestamp of this SubmittedMessage.
        Date time after which the message expires and will not be sent

        :param message_expiry_timestamp: The message_expiry_timestamp of this SubmittedMessage.
        :type: datetime
        """

        self._message_expiry_timestamp = message_expiry_timestamp

    @property
    def metadata(self):
        """
        Gets the metadata of this SubmittedMessage.
        Metadata for the message specified as a set of key value pairs, each key can be up to 100 characters long and each value can be up to 256 characters long ``` {    \"myKey\": \"myValue\",    \"anotherKey\": \"anotherValue\" } ``` 

        :return: The metadata of this SubmittedMessage.
        :rtype: object
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this SubmittedMessage.
        Metadata for the message specified as a set of key value pairs, each key can be up to 100 characters long and each value can be up to 256 characters long ``` {    \"myKey\": \"myValue\",    \"anotherKey\": \"anotherValue\" } ``` 

        :param metadata: The metadata of this SubmittedMessage.
        :type: object
        """

        self._metadata = metadata

    @property
    def scheduled(self):
        """
        Gets the scheduled of this SubmittedMessage.
        Scheduled delivery date time of the message

        :return: The scheduled of this SubmittedMessage.
        :rtype: datetime
        """
        return self._scheduled

    @scheduled.setter
    def scheduled(self, scheduled):
        """
        Sets the scheduled of this SubmittedMessage.
        Scheduled delivery date time of the message

        :param scheduled: The scheduled of this SubmittedMessage.
        :type: datetime
        """

        self._scheduled = scheduled

    @property
    def source_number(self):
        """
        Gets the source_number of this SubmittedMessage.


        :return: The source_number of this SubmittedMessage.
        :rtype: str
        """
        return self._source_number

    @source_number.setter
    def source_number(self, source_number):
        """
        Sets the source_number of this SubmittedMessage.


        :param source_number: The source_number of this SubmittedMessage.
        :type: str
        """

        self._source_number = source_number

    @property
    def source_number_type(self):
        """
        Gets the source_number_type of this SubmittedMessage.
        Type of source address specified, this can be INTERNATIONAL, ALPHANUMERIC or SHORTCODE

        :return: The source_number_type of this SubmittedMessage.
        :rtype: str
        """
        return self._source_number_type

    @source_number_type.setter
    def source_number_type(self, source_number_type):
        """
        Sets the source_number_type of this SubmittedMessage.
        Type of source address specified, this can be INTERNATIONAL, ALPHANUMERIC or SHORTCODE

        :param source_number_type: The source_number_type of this SubmittedMessage.
        :type: str
        """
        allowed_values = ["INTERNATIONAL", "ALPHANUMERIC", "SHORTCODE"]
        if source_number_type not in allowed_values:
            raise ValueError(
                "Invalid value for `source_number_type` ({0}), must be one of {1}"
                .format(source_number_type, allowed_values)
            )

        self._source_number_type = source_number_type

    @property
    def message_id(self):
        """
        Gets the message_id of this SubmittedMessage.
        Unique ID of this message

        :return: The message_id of this SubmittedMessage.
        :rtype: str
        """
        return self._message_id

    @message_id.setter
    def message_id(self, message_id):
        """
        Sets the message_id of this SubmittedMessage.
        Unique ID of this message

        :param message_id: The message_id of this SubmittedMessage.
        :type: str
        """

        self._message_id = message_id

    @property
    def status(self):
        """
        Gets the status of this SubmittedMessage.
        The status of the message

        :return: The status of this SubmittedMessage.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this SubmittedMessage.
        The status of the message

        :param status: The status of this SubmittedMessage.
        :type: str
        """
        allowed_values = ["enroute", "submitted", "delivered", "expired", "rejected", "undeliverable", "queued", "cancelled", "scheduled", "failed"]
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status

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
