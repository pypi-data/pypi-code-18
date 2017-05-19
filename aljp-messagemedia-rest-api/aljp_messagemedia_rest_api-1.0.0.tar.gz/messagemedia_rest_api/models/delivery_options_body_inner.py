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


class DeliveryOptionsBodyInner(object):
    """
    Do not edit the class manually.
    """
    def __init__(self, delivery_type=None, delivery_addresses=None, delivery_format=None):
        """
        DeliveryOptionsBodyInner - a model

        :param dict types: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.types = {
            'delivery_type': 'str',
            'delivery_addresses': 'list[str]',
            'delivery_format': 'str'
        }

        self.attribute_map = {
            'delivery_type': 'delivery_type',
            'delivery_addresses': 'delivery_addresses',
            'delivery_format': 'delivery_format'
        }

        self._delivery_type = delivery_type
        self._delivery_addresses = delivery_addresses
        self._delivery_format = delivery_format

    @property
    def delivery_type(self):
        """
        Gets the delivery_type of this DeliveryOptionsBodyInner.
        How to deliver the report.

        :return: The delivery_type of this DeliveryOptionsBodyInner.
        :rtype: str
        """
        return self._delivery_type

    @delivery_type.setter
    def delivery_type(self, delivery_type):
        """
        Sets the delivery_type of this DeliveryOptionsBodyInner.
        How to deliver the report.

        :param delivery_type: The delivery_type of this DeliveryOptionsBodyInner.
        :type: str
        """
        allowed_values = ["EMAIL"]
        if delivery_type not in allowed_values:
            raise ValueError(
                "Invalid value for `delivery_type` ({0}), must be one of {1}"
                .format(delivery_type, allowed_values)
            )

        self._delivery_type = delivery_type

    @property
    def delivery_addresses(self):
        """
        Gets the delivery_addresses of this DeliveryOptionsBodyInner.
        A list of email addresses to use as the recipient of the email. Only works for EMAIL delivery type

        :return: The delivery_addresses of this DeliveryOptionsBodyInner.
        :rtype: list[str]
        """
        return self._delivery_addresses

    @delivery_addresses.setter
    def delivery_addresses(self, delivery_addresses):
        """
        Sets the delivery_addresses of this DeliveryOptionsBodyInner.
        A list of email addresses to use as the recipient of the email. Only works for EMAIL delivery type

        :param delivery_addresses: The delivery_addresses of this DeliveryOptionsBodyInner.
        :type: list[str]
        """

        self._delivery_addresses = delivery_addresses

    @property
    def delivery_format(self):
        """
        Gets the delivery_format of this DeliveryOptionsBodyInner.
        Format of the report.

        :return: The delivery_format of this DeliveryOptionsBodyInner.
        :rtype: str
        """
        return self._delivery_format

    @delivery_format.setter
    def delivery_format(self, delivery_format):
        """
        Sets the delivery_format of this DeliveryOptionsBodyInner.
        Format of the report.

        :param delivery_format: The delivery_format of this DeliveryOptionsBodyInner.
        :type: str
        """
        allowed_values = ["CSV"]
        if delivery_format not in allowed_values:
            raise ValueError(
                "Invalid value for `delivery_format` ({0}), must be one of {1}"
                .format(delivery_format, allowed_values)
            )

        self._delivery_format = delivery_format

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
