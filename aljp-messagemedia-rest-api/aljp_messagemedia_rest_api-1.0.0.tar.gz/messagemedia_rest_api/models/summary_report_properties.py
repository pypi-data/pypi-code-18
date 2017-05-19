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


class SummaryReportProperties(object):
    """
    Do not edit the class manually.
    """
    def __init__(self, end_date=None, filters=None, grouping=None, start_date=None, summary=None, summary_field=None, timezone=None):
        """
        SummaryReportProperties - a model

        :param dict types: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.types = {
            'end_date': 'datetime',
            'filters': 'object',
            'grouping': 'str',
            'start_date': 'datetime',
            'summary': 'str',
            'summary_field': 'str',
            'timezone': 'str'
        }

        self.attribute_map = {
            'end_date': 'end_date',
            'filters': 'filters',
            'grouping': 'grouping',
            'start_date': 'start_date',
            'summary': 'summary',
            'summary_field': 'summary_field',
            'timezone': 'timezone'
        }

        self._end_date = end_date
        self._filters = filters
        self._grouping = grouping
        self._start_date = start_date
        self._summary = summary
        self._summary_field = summary_field
        self._timezone = timezone

    @property
    def end_date(self):
        """
        Gets the end_date of this SummaryReportProperties.
        The end date provided as a parameter for this report

        :return: The end_date of this SummaryReportProperties.
        :rtype: datetime
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """
        Sets the end_date of this SummaryReportProperties.
        The end date provided as a parameter for this report

        :param end_date: The end_date of this SummaryReportProperties.
        :type: datetime
        """

        self._end_date = end_date

    @property
    def filters(self):
        """
        Gets the filters of this SummaryReportProperties.
        Any filters provided as parameters for this report

        :return: The filters of this SummaryReportProperties.
        :rtype: object
        """
        return self._filters

    @filters.setter
    def filters(self, filters):
        """
        Sets the filters of this SummaryReportProperties.
        Any filters provided as parameters for this report

        :param filters: The filters of this SummaryReportProperties.
        :type: object
        """

        self._filters = filters

    @property
    def grouping(self):
        """
        Gets the grouping of this SummaryReportProperties.
        The value of the group by parameter provided for this report

        :return: The grouping of this SummaryReportProperties.
        :rtype: str
        """
        return self._grouping

    @grouping.setter
    def grouping(self, grouping):
        """
        Sets the grouping of this SummaryReportProperties.
        The value of the group by parameter provided for this report

        :param grouping: The grouping of this SummaryReportProperties.
        :type: str
        """
        allowed_values = ["DAY", "DELIVERY_REPORT", "DESTINATION_ADDRESS", "DESTINATION_ADDRESS_COUNTRY", "FORMAT", "HOUR", "METADATA_KEY", "METADATA_VALUE", "MINUTE", "MONTH", "SOURCE_ADDRESS", "SOURCE_ADDRESS_COUNTRY", "STATUS", "STATUS_CODE", "YEAR"]
        if grouping not in allowed_values:
            raise ValueError(
                "Invalid value for `grouping` ({0}), must be one of {1}"
                .format(grouping, allowed_values)
            )

        self._grouping = grouping

    @property
    def start_date(self):
        """
        Gets the start_date of this SummaryReportProperties.
        The end date provided as a parameter for this report

        :return: The start_date of this SummaryReportProperties.
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """
        Sets the start_date of this SummaryReportProperties.
        The end date provided as a parameter for this report

        :param start_date: The start_date of this SummaryReportProperties.
        :type: datetime
        """

        self._start_date = start_date

    @property
    def summary(self):
        """
        Gets the summary of this SummaryReportProperties.
        The value of the summary_by parameter provided for this report

        :return: The summary of this SummaryReportProperties.
        :rtype: str
        """
        return self._summary

    @summary.setter
    def summary(self, summary):
        """
        Sets the summary of this SummaryReportProperties.
        The value of the summary_by parameter provided for this report

        :param summary: The summary of this SummaryReportProperties.
        :type: str
        """
        allowed_values = ["COUNT", "SUM"]
        if summary not in allowed_values:
            raise ValueError(
                "Invalid value for `summary` ({0}), must be one of {1}"
                .format(summary, allowed_values)
            )

        self._summary = summary

    @property
    def summary_field(self):
        """
        Gets the summary_field of this SummaryReportProperties.
        The value of the summary_field parameter provided for this report

        :return: The summary_field of this SummaryReportProperties.
        :rtype: str
        """
        return self._summary_field

    @summary_field.setter
    def summary_field(self, summary_field):
        """
        Sets the summary_field of this SummaryReportProperties.
        The value of the summary_field parameter provided for this report

        :param summary_field: The summary_field of this SummaryReportProperties.
        :type: str
        """
        allowed_values = ["UNITS", "MESSAGE_ID"]
        if summary_field not in allowed_values:
            raise ValueError(
                "Invalid value for `summary_field` ({0}), must be one of {1}"
                .format(summary_field, allowed_values)
            )

        self._summary_field = summary_field

    @property
    def timezone(self):
        """
        Gets the timezone of this SummaryReportProperties.


        :return: The timezone of this SummaryReportProperties.
        :rtype: str
        """
        return self._timezone

    @timezone.setter
    def timezone(self, timezone):
        """
        Sets the timezone of this SummaryReportProperties.


        :param timezone: The timezone of this SummaryReportProperties.
        :type: str
        """

        self._timezone = timezone

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
