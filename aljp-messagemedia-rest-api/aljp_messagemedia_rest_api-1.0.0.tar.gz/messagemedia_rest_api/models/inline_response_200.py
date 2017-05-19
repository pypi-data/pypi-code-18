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


class InlineResponse200(object):
    """
    Do not edit the class manually.
    """
    def __init__(self, data=None, pagination=None):
        """
        InlineResponse200 - a model

        :param dict types: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.types = {
            'data': 'list[AsyncReport]',
            'pagination': 'Pagination'
        }

        self.attribute_map = {
            'data': 'data',
            'pagination': 'pagination'
        }

        self._data = data
        self._pagination = pagination

    @property
    def data(self):
        """
        Gets the data of this InlineResponse200.
        List of asynchronous reports

        :return: The data of this InlineResponse200.
        :rtype: list[AsyncReport]
        """
        return self._data

    @data.setter
    def data(self, data):
        """
        Sets the data of this InlineResponse200.
        List of asynchronous reports

        :param data: The data of this InlineResponse200.
        :type: list[AsyncReport]
        """

        self._data = data

    @property
    def pagination(self):
        """
        Gets the pagination of this InlineResponse200.


        :return: The pagination of this InlineResponse200.
        :rtype: Pagination
        """
        return self._pagination

    @pagination.setter
    def pagination(self, pagination):
        """
        Sets the pagination of this InlineResponse200.


        :param pagination: The pagination of this InlineResponse200.
        :type: Pagination
        """

        self._pagination = pagination

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
