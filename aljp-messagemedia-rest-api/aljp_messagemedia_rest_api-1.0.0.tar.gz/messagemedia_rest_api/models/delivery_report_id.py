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


class DeliveryReportId(object):
    """
    Do not edit the class manually.
    """
    def __init__(self, delivery_report_ids=None):
        """
        DeliveryReportId - a model

        :param dict types: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.types = {
            'delivery_report_ids': 'list[str]'
        }

        self.attribute_map = {
            'delivery_report_ids': 'delivery_report_ids'
        }

        self._delivery_report_ids = delivery_report_ids

    @property
    def delivery_report_ids(self):
        """
        Gets the delivery_report_ids of this DeliveryReportId.


        :return: The delivery_report_ids of this DeliveryReportId.
        :rtype: list[str]
        """
        return self._delivery_report_ids

    @delivery_report_ids.setter
    def delivery_report_ids(self, delivery_report_ids):
        """
        Sets the delivery_report_ids of this DeliveryReportId.


        :param delivery_report_ids: The delivery_report_ids of this DeliveryReportId.
        :type: list[str]
        """

        self._delivery_report_ids = delivery_report_ids

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
