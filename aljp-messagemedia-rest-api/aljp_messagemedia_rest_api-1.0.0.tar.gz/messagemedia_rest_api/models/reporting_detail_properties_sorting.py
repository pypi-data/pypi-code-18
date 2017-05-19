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


class ReportingDetailPropertiesSorting(object):
    """
    Do not edit the class manually.
    """
    def __init__(self, field=None, order=None):
        """
        ReportingDetailPropertiesSorting - a model

        :param dict types: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.types = {
            'field': 'str',
            'order': 'str'
        }

        self.attribute_map = {
            'field': 'field',
            'order': 'order'
        }

        self._field = field
        self._order = order

    @property
    def field(self):
        """
        Gets the field of this ReportingDetailPropertiesSorting.
        The value of the sort_by field provided for this report

        :return: The field of this ReportingDetailPropertiesSorting.
        :rtype: str
        """
        return self._field

    @field.setter
    def field(self, field):
        """
        Sets the field of this ReportingDetailPropertiesSorting.
        The value of the sort_by field provided for this report

        :param field: The field of this ReportingDetailPropertiesSorting.
        :type: str
        """
        allowed_values = ["ACCOUNT", "DELIVERED_TIMESTAMP", "MESSAGE_EXPIRY_TIMESTAMP", "DELIVERY_REPORT", "DESTINATION_ADDRESS", "DESTINATION_ADDRESS_COUNTRY", "FORMAT", "SOURCE_ADDRESS", "SOURCE_ADDRESS_COUNTRY", "STATUS", "STATUS_CODE", "UNITS", "TIMESTAMP"]
        if field not in allowed_values:
            raise ValueError(
                "Invalid value for `field` ({0}), must be one of {1}"
                .format(field, allowed_values)
            )

        self._field = field

    @property
    def order(self):
        """
        Gets the order of this ReportingDetailPropertiesSorting.
        The value of the sort_direction field provided for this report

        :return: The order of this ReportingDetailPropertiesSorting.
        :rtype: str
        """
        return self._order

    @order.setter
    def order(self, order):
        """
        Sets the order of this ReportingDetailPropertiesSorting.
        The value of the sort_direction field provided for this report

        :param order: The order of this ReportingDetailPropertiesSorting.
        :type: str
        """
        allowed_values = ["ASCENDING", "DESCENDING"]
        if order not in allowed_values:
            raise ValueError(
                "Invalid value for `order` ({0}), must be one of {1}"
                .format(order, allowed_values)
            )

        self._order = order

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
