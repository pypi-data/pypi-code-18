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


class Pagination(object):
    """
    Do not edit the class manually.
    """
    def __init__(self, page=None, page_size=None, total_count=None, page_count=None, next_uri=None, previous_uri=None):
        """
        Pagination - a model

        :param dict types: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.types = {
            'page': 'int',
            'page_size': 'int',
            'total_count': 'int',
            'page_count': 'int',
            'next_uri': 'str',
            'previous_uri': 'str'
        }

        self.attribute_map = {
            'page': 'page',
            'page_size': 'page_size',
            'total_count': 'total_count',
            'page_count': 'page_count',
            'next_uri': 'next_uri',
            'previous_uri': 'previous_uri'
        }

        self._page = page
        self._page_size = page_size
        self._total_count = total_count
        self._page_count = page_count
        self._next_uri = next_uri
        self._previous_uri = previous_uri

    @property
    def page(self):
        """
        Gets the page of this Pagination.
        The current page of results

        :return: The page of this Pagination.
        :rtype: int
        """
        return self._page

    @page.setter
    def page(self, page):
        """
        Sets the page of this Pagination.
        The current page of results

        :param page: The page of this Pagination.
        :type: int
        """

        self._page = page

    @property
    def page_size(self):
        """
        Gets the page_size of this Pagination.
        The amount of results returned per page

        :return: The page_size of this Pagination.
        :rtype: int
        """
        return self._page_size

    @page_size.setter
    def page_size(self, page_size):
        """
        Sets the page_size of this Pagination.
        The amount of results returned per page

        :param page_size: The page_size of this Pagination.
        :type: int
        """

        self._page_size = page_size

    @property
    def total_count(self):
        """
        Gets the total_count of this Pagination.
        The total number of results in the results set

        :return: The total_count of this Pagination.
        :rtype: int
        """
        return self._total_count

    @total_count.setter
    def total_count(self, total_count):
        """
        Sets the total_count of this Pagination.
        The total number of results in the results set

        :param total_count: The total_count of this Pagination.
        :type: int
        """

        self._total_count = total_count

    @property
    def page_count(self):
        """
        Gets the page_count of this Pagination.
        The total number of pages in the results set

        :return: The page_count of this Pagination.
        :rtype: int
        """
        return self._page_count

    @page_count.setter
    def page_count(self, page_count):
        """
        Sets the page_count of this Pagination.
        The total number of pages in the results set

        :param page_count: The page_count of this Pagination.
        :type: int
        """

        self._page_count = page_count

    @property
    def next_uri(self):
        """
        Gets the next_uri of this Pagination.
        Link to the next page of results

        :return: The next_uri of this Pagination.
        :rtype: str
        """
        return self._next_uri

    @next_uri.setter
    def next_uri(self, next_uri):
        """
        Sets the next_uri of this Pagination.
        Link to the next page of results

        :param next_uri: The next_uri of this Pagination.
        :type: str
        """

        self._next_uri = next_uri

    @property
    def previous_uri(self):
        """
        Gets the previous_uri of this Pagination.
        Link to the previous page of results

        :return: The previous_uri of this Pagination.
        :rtype: str
        """
        return self._previous_uri

    @previous_uri.setter
    def previous_uri(self, previous_uri):
        """
        Sets the previous_uri of this Pagination.
        Link to the previous page of results

        :param previous_uri: The previous_uri of this Pagination.
        :type: str
        """

        self._previous_uri = previous_uri

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
