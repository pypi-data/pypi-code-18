# coding: utf-8

"""
Copyright 2016 SmartBear Software

    Licensed under the Apache License, Version 2.0 (the "License");
    you may not use this file except in compliance with the License.
    You may obtain a copy of the License at

        http://www.apache.org/licenses/LICENSE-2.0

    Unless required by applicable law or agreed to in writing, software
    distributed under the License is distributed on an "AS IS" BASIS,
    WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
    See the License for the specific language governing permissions and
    limitations under the License.

    Ref: https://github.com/swagger-api/swagger-codegen
"""

from pprint import pformat
from six import iteritems
import re


class CampaignScheduleNotification(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        CampaignScheduleNotification - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'date_created': 'datetime',
            'date_modified': 'datetime',
            'version': 'int',
            'intervals': 'list[CampaignScheduleNotificationIntervals]',
            'time_zone': 'str',
            'campaign': 'DependencyTrackingBuildNotificationNotificationUser',
            'additional_properties': 'object'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'date_created': 'dateCreated',
            'date_modified': 'dateModified',
            'version': 'version',
            'intervals': 'intervals',
            'time_zone': 'timeZone',
            'campaign': 'campaign',
            'additional_properties': 'additionalProperties'
        }

        self._id = None
        self._name = None
        self._date_created = None
        self._date_modified = None
        self._version = None
        self._intervals = None
        self._time_zone = None
        self._campaign = None
        self._additional_properties = None

    @property
    def id(self):
        """
        Gets the id of this CampaignScheduleNotification.


        :return: The id of this CampaignScheduleNotification.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this CampaignScheduleNotification.


        :param id: The id of this CampaignScheduleNotification.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this CampaignScheduleNotification.


        :return: The name of this CampaignScheduleNotification.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this CampaignScheduleNotification.


        :param name: The name of this CampaignScheduleNotification.
        :type: str
        """
        
        self._name = name

    @property
    def date_created(self):
        """
        Gets the date_created of this CampaignScheduleNotification.


        :return: The date_created of this CampaignScheduleNotification.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this CampaignScheduleNotification.


        :param date_created: The date_created of this CampaignScheduleNotification.
        :type: datetime
        """
        
        self._date_created = date_created

    @property
    def date_modified(self):
        """
        Gets the date_modified of this CampaignScheduleNotification.


        :return: The date_modified of this CampaignScheduleNotification.
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """
        Sets the date_modified of this CampaignScheduleNotification.


        :param date_modified: The date_modified of this CampaignScheduleNotification.
        :type: datetime
        """
        
        self._date_modified = date_modified

    @property
    def version(self):
        """
        Gets the version of this CampaignScheduleNotification.


        :return: The version of this CampaignScheduleNotification.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this CampaignScheduleNotification.


        :param version: The version of this CampaignScheduleNotification.
        :type: int
        """
        
        self._version = version

    @property
    def intervals(self):
        """
        Gets the intervals of this CampaignScheduleNotification.


        :return: The intervals of this CampaignScheduleNotification.
        :rtype: list[CampaignScheduleNotificationIntervals]
        """
        return self._intervals

    @intervals.setter
    def intervals(self, intervals):
        """
        Sets the intervals of this CampaignScheduleNotification.


        :param intervals: The intervals of this CampaignScheduleNotification.
        :type: list[CampaignScheduleNotificationIntervals]
        """
        
        self._intervals = intervals

    @property
    def time_zone(self):
        """
        Gets the time_zone of this CampaignScheduleNotification.


        :return: The time_zone of this CampaignScheduleNotification.
        :rtype: str
        """
        return self._time_zone

    @time_zone.setter
    def time_zone(self, time_zone):
        """
        Sets the time_zone of this CampaignScheduleNotification.


        :param time_zone: The time_zone of this CampaignScheduleNotification.
        :type: str
        """
        
        self._time_zone = time_zone

    @property
    def campaign(self):
        """
        Gets the campaign of this CampaignScheduleNotification.


        :return: The campaign of this CampaignScheduleNotification.
        :rtype: DependencyTrackingBuildNotificationNotificationUser
        """
        return self._campaign

    @campaign.setter
    def campaign(self, campaign):
        """
        Sets the campaign of this CampaignScheduleNotification.


        :param campaign: The campaign of this CampaignScheduleNotification.
        :type: DependencyTrackingBuildNotificationNotificationUser
        """
        
        self._campaign = campaign

    @property
    def additional_properties(self):
        """
        Gets the additional_properties of this CampaignScheduleNotification.


        :return: The additional_properties of this CampaignScheduleNotification.
        :rtype: object
        """
        return self._additional_properties

    @additional_properties.setter
    def additional_properties(self, additional_properties):
        """
        Sets the additional_properties of this CampaignScheduleNotification.


        :param additional_properties: The additional_properties of this CampaignScheduleNotification.
        :type: object
        """
        
        self._additional_properties = additional_properties

    def to_dict(self):
        """
        Returns the model properties as a dict
        """
        result = {}

        for attr, _ in iteritems(self.swagger_types):
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

