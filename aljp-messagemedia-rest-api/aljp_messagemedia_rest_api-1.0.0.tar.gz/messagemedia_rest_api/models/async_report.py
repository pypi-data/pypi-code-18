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


class AsyncReport(object):
    """
    Do not edit the class manually.
    """
    def __init__(self, id=None, message_type=None, type=None, report_status=None, created_datetime=None, last_modified_datetime=None):
        """
        AsyncReport - a model

        :param dict types: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.types = {
            'id': 'str',
            'message_type': 'str',
            'type': 'str',
            'report_status': 'str',
            'created_datetime': 'datetime',
            'last_modified_datetime': 'datetime'
        }

        self.attribute_map = {
            'id': 'id',
            'message_type': 'message_type',
            'type': 'type',
            'report_status': 'report_status',
            'created_datetime': 'created_datetime',
            'last_modified_datetime': 'last_modified_datetime'
        }

        self._id = id
        self._message_type = message_type
        self._type = type
        self._report_status = report_status
        self._created_datetime = created_datetime
        self._last_modified_datetime = last_modified_datetime

    @property
    def id(self):
        """
        Gets the id of this AsyncReport.
        Unique ID for this reply

        :return: The id of this AsyncReport.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this AsyncReport.
        Unique ID for this reply

        :param id: The id of this AsyncReport.
        :type: str
        """

        self._id = id

    @property
    def message_type(self):
        """
        Gets the message_type of this AsyncReport.


        :return: The message_type of this AsyncReport.
        :rtype: str
        """
        return self._message_type

    @message_type.setter
    def message_type(self, message_type):
        """
        Sets the message_type of this AsyncReport.


        :param message_type: The message_type of this AsyncReport.
        :type: str
        """
        allowed_values = ["SENT_MESSAGES", "RECEIVED_MESSAGES", "DELIVERY_REPORTS"]
        if message_type not in allowed_values:
            raise ValueError(
                "Invalid value for `message_type` ({0}), must be one of {1}"
                .format(message_type, allowed_values)
            )

        self._message_type = message_type

    @property
    def type(self):
        """
        Gets the type of this AsyncReport.


        :return: The type of this AsyncReport.
        :rtype: str
        """
        return self._type

    @type.setter
    def type(self, type):
        """
        Sets the type of this AsyncReport.


        :param type: The type of this AsyncReport.
        :type: str
        """
        allowed_values = ["SUMMARY", "DETAIL"]
        if type not in allowed_values:
            raise ValueError(
                "Invalid value for `type` ({0}), must be one of {1}"
                .format(type, allowed_values)
            )

        self._type = type

    @property
    def report_status(self):
        """
        Gets the report_status of this AsyncReport.


        :return: The report_status of this AsyncReport.
        :rtype: str
        """
        return self._report_status

    @report_status.setter
    def report_status(self, report_status):
        """
        Sets the report_status of this AsyncReport.


        :param report_status: The report_status of this AsyncReport.
        :type: str
        """
        allowed_values = ["REQUESTED", "RUNNING", "CANCELLED", "DONE"]
        if report_status not in allowed_values:
            raise ValueError(
                "Invalid value for `report_status` ({0}), must be one of {1}"
                .format(report_status, allowed_values)
            )

        self._report_status = report_status

    @property
    def created_datetime(self):
        """
        Gets the created_datetime of this AsyncReport.
        Date time at which this report was created.

        :return: The created_datetime of this AsyncReport.
        :rtype: datetime
        """
        return self._created_datetime

    @created_datetime.setter
    def created_datetime(self, created_datetime):
        """
        Sets the created_datetime of this AsyncReport.
        Date time at which this report was created.

        :param created_datetime: The created_datetime of this AsyncReport.
        :type: datetime
        """

        self._created_datetime = created_datetime

    @property
    def last_modified_datetime(self):
        """
        Gets the last_modified_datetime of this AsyncReport.
        Date time at which this report was last modified.

        :return: The last_modified_datetime of this AsyncReport.
        :rtype: datetime
        """
        return self._last_modified_datetime

    @last_modified_datetime.setter
    def last_modified_datetime(self, last_modified_datetime):
        """
        Sets the last_modified_datetime of this AsyncReport.
        Date time at which this report was last modified.

        :param last_modified_datetime: The last_modified_datetime of this AsyncReport.
        :type: datetime
        """

        self._last_modified_datetime = last_modified_datetime

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
