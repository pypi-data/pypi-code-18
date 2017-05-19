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


class Report(object):
    """
    Do not edit the class manually.
    """
    def __init__(self, callback_url=None, date_received=None, delay=None, delivery_report_id=None, message_id=None, metadata=None, original_text=None, source_number=None, status=None, submitted_date=None, vendor_account_id=None):
        """
        Report - a model

        :param dict types: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.types = {
            'callback_url': 'str',
            'date_received': 'datetime',
            'delay': 'int',
            'delivery_report_id': 'str',
            'message_id': 'str',
            'metadata': 'object',
            'original_text': 'str',
            'source_number': 'str',
            'status': 'str',
            'submitted_date': 'datetime',
            'vendor_account_id': 'ReplyVendorAccountId'
        }

        self.attribute_map = {
            'callback_url': 'callback_url',
            'date_received': 'date_received',
            'delay': 'delay',
            'delivery_report_id': 'delivery_report_id',
            'message_id': 'message_id',
            'metadata': 'metadata',
            'original_text': 'original_text',
            'source_number': 'source_number',
            'status': 'status',
            'submitted_date': 'submitted_date',
            'vendor_account_id': 'vendor_account_id'
        }

        self._callback_url = callback_url
        self._date_received = date_received
        self._delay = delay
        self._delivery_report_id = delivery_report_id
        self._message_id = message_id
        self._metadata = metadata
        self._original_text = original_text
        self._source_number = source_number
        self._status = status
        self._submitted_date = submitted_date
        self._vendor_account_id = vendor_account_id

    @property
    def callback_url(self):
        """
        Gets the callback_url of this Report.
        The URL specified as the callback URL in the original submit message request

        :return: The callback_url of this Report.
        :rtype: str
        """
        return self._callback_url

    @callback_url.setter
    def callback_url(self, callback_url):
        """
        Sets the callback_url of this Report.
        The URL specified as the callback URL in the original submit message request

        :param callback_url: The callback_url of this Report.
        :type: str
        """

        self._callback_url = callback_url

    @property
    def date_received(self):
        """
        Gets the date_received of this Report.
        The date and time at which this delivery report was generated in UTC.

        :return: The date_received of this Report.
        :rtype: datetime
        """
        return self._date_received

    @date_received.setter
    def date_received(self, date_received):
        """
        Sets the date_received of this Report.
        The date and time at which this delivery report was generated in UTC.

        :param date_received: The date_received of this Report.
        :type: datetime
        """

        self._date_received = date_received

    @property
    def delay(self):
        """
        Gets the delay of this Report.
        Deprecated, no longer in use

        :return: The delay of this Report.
        :rtype: int
        """
        return self._delay

    @delay.setter
    def delay(self, delay):
        """
        Sets the delay of this Report.
        Deprecated, no longer in use

        :param delay: The delay of this Report.
        :type: int
        """

        self._delay = delay

    @property
    def delivery_report_id(self):
        """
        Gets the delivery_report_id of this Report.
        Unique ID for this delivery report

        :return: The delivery_report_id of this Report.
        :rtype: str
        """
        return self._delivery_report_id

    @delivery_report_id.setter
    def delivery_report_id(self, delivery_report_id):
        """
        Sets the delivery_report_id of this Report.
        Unique ID for this delivery report

        :param delivery_report_id: The delivery_report_id of this Report.
        :type: str
        """

        self._delivery_report_id = delivery_report_id

    @property
    def message_id(self):
        """
        Gets the message_id of this Report.
        Unique ID of the original message

        :return: The message_id of this Report.
        :rtype: str
        """
        return self._message_id

    @message_id.setter
    def message_id(self, message_id):
        """
        Sets the message_id of this Report.
        Unique ID of the original message

        :param message_id: The message_id of this Report.
        :type: str
        """

        self._message_id = message_id

    @property
    def metadata(self):
        """
        Gets the metadata of this Report.
        Any metadata that was included in the original submit message request

        :return: The metadata of this Report.
        :rtype: object
        """
        return self._metadata

    @metadata.setter
    def metadata(self, metadata):
        """
        Sets the metadata of this Report.
        Any metadata that was included in the original submit message request

        :param metadata: The metadata of this Report.
        :type: object
        """

        self._metadata = metadata

    @property
    def original_text(self):
        """
        Gets the original_text of this Report.
        Text of the original message.

        :return: The original_text of this Report.
        :rtype: str
        """
        return self._original_text

    @original_text.setter
    def original_text(self, original_text):
        """
        Sets the original_text of this Report.
        Text of the original message.

        :param original_text: The original_text of this Report.
        :type: str
        """

        self._original_text = original_text

    @property
    def source_number(self):
        """
        Gets the source_number of this Report.
        Address from which this delivery report was received

        :return: The source_number of this Report.
        :rtype: str
        """
        return self._source_number

    @source_number.setter
    def source_number(self, source_number):
        """
        Sets the source_number of this Report.
        Address from which this delivery report was received

        :param source_number: The source_number of this Report.
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
    def status(self):
        """
        Gets the status of this Report.
        The status of the message as per the delivery report

        :return: The status of this Report.
        :rtype: str
        """
        return self._status

    @status.setter
    def status(self, status):
        """
        Sets the status of this Report.
        The status of the message as per the delivery report

        :param status: The status of this Report.
        :type: str
        """
        allowed_values = ["enroute", "failed", "submitted", "delivered", "expired", "rejected", "undeliverable"]
        if status not in allowed_values:
            raise ValueError(
                "Invalid value for `status` ({0}), must be one of {1}"
                .format(status, allowed_values)
            )

        self._status = status

    @property
    def submitted_date(self):
        """
        Gets the submitted_date of this Report.
        The date and time when the message status changed in UTC. For a delivered DR this may indicate the time at which the message was received on the handset.

        :return: The submitted_date of this Report.
        :rtype: datetime
        """
        return self._submitted_date

    @submitted_date.setter
    def submitted_date(self, submitted_date):
        """
        Sets the submitted_date of this Report.
        The date and time when the message status changed in UTC. For a delivered DR this may indicate the time at which the message was received on the handset.

        :param submitted_date: The submitted_date of this Report.
        :type: datetime
        """

        self._submitted_date = submitted_date

    @property
    def vendor_account_id(self):
        """
        Gets the vendor_account_id of this Report.


        :return: The vendor_account_id of this Report.
        :rtype: ReplyVendorAccountId
        """
        return self._vendor_account_id

    @vendor_account_id.setter
    def vendor_account_id(self, vendor_account_id):
        """
        Sets the vendor_account_id of this Report.


        :param vendor_account_id: The vendor_account_id of this Report.
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
