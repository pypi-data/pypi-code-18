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


class SummaryReport(object):
    """
    Do not edit the class manually.
    """
    def __init__(self, properties=None, data=None):
        """
        SummaryReport - a model

        :param dict types: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.types = {
            'properties': 'SummaryReportProperties',
            'data': 'list[SummaryReportData]'
        }

        self.attribute_map = {
            'properties': 'properties',
            'data': 'data'
        }

        self._properties = properties
        self._data = data

    @property
    def properties(self):
        """
        Gets the properties of this SummaryReport.


        :return: The properties of this SummaryReport.
        :rtype: SummaryReportProperties
        """
        return self._properties

    @properties.setter
    def properties(self, properties):
        """
        Sets the properties of this SummaryReport.


        :param properties: The properties of this SummaryReport.
        :type: SummaryReportProperties
        """

        self._properties = properties

    @property
    def data(self):
        """
        Gets the data of this SummaryReport.


        :return: The data of this SummaryReport.
        :rtype: list[SummaryReportData]
        """
        return self._data

    @data.setter
    def data(self, data):
        """
        Sets the data of this SummaryReport.


        :param data: The data of this SummaryReport.
        :type: list[SummaryReportData]
        """

        self._data = data

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
