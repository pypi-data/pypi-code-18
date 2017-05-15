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


class HeartBeatAlert(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        HeartBeatAlert - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'sender_id': 'str',
            'heart_beat_timeout_in_minutes': 'int',
            'rule_id': 'str',
            'start_date': 'datetime',
            'end_date': 'datetime',
            'notification_users': 'list[User]',
            'alert_types': 'list[str]',
            'rule_type': 'str',
            'rule_uri': 'str',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'sender_id': 'senderId',
            'heart_beat_timeout_in_minutes': 'heartBeatTimeoutInMinutes',
            'rule_id': 'ruleId',
            'start_date': 'startDate',
            'end_date': 'endDate',
            'notification_users': 'notificationUsers',
            'alert_types': 'alertTypes',
            'rule_type': 'ruleType',
            'rule_uri': 'ruleUri',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._sender_id = None
        self._heart_beat_timeout_in_minutes = None
        self._rule_id = None
        self._start_date = None
        self._end_date = None
        self._notification_users = None
        self._alert_types = None
        self._rule_type = None
        self._rule_uri = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this HeartBeatAlert.
        The globally unique identifier for the object.

        :return: The id of this HeartBeatAlert.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this HeartBeatAlert.
        The globally unique identifier for the object.

        :param id: The id of this HeartBeatAlert.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this HeartBeatAlert.
        Name of the rule

        :return: The name of this HeartBeatAlert.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this HeartBeatAlert.
        Name of the rule

        :param name: The name of this HeartBeatAlert.
        :type: str
        """
        
        self._name = name

    @property
    def sender_id(self):
        """
        Gets the sender_id of this HeartBeatAlert.
        The value that identifies the sender of the heartbeat.

        :return: The sender_id of this HeartBeatAlert.
        :rtype: str
        """
        return self._sender_id

    @sender_id.setter
    def sender_id(self, sender_id):
        """
        Sets the sender_id of this HeartBeatAlert.
        The value that identifies the sender of the heartbeat.

        :param sender_id: The sender_id of this HeartBeatAlert.
        :type: str
        """
        
        self._sender_id = sender_id

    @property
    def heart_beat_timeout_in_minutes(self):
        """
        Gets the heart_beat_timeout_in_minutes of this HeartBeatAlert.
        The number of minutes to wait before alerting missing heartbeats.

        :return: The heart_beat_timeout_in_minutes of this HeartBeatAlert.
        :rtype: int
        """
        return self._heart_beat_timeout_in_minutes

    @heart_beat_timeout_in_minutes.setter
    def heart_beat_timeout_in_minutes(self, heart_beat_timeout_in_minutes):
        """
        Sets the heart_beat_timeout_in_minutes of this HeartBeatAlert.
        The number of minutes to wait before alerting missing heartbeats.

        :param heart_beat_timeout_in_minutes: The heart_beat_timeout_in_minutes of this HeartBeatAlert.
        :type: int
        """
        
        self._heart_beat_timeout_in_minutes = heart_beat_timeout_in_minutes

    @property
    def rule_id(self):
        """
        Gets the rule_id of this HeartBeatAlert.
        The id of the rule.

        :return: The rule_id of this HeartBeatAlert.
        :rtype: str
        """
        return self._rule_id

    @rule_id.setter
    def rule_id(self, rule_id):
        """
        Sets the rule_id of this HeartBeatAlert.
        The id of the rule.

        :param rule_id: The rule_id of this HeartBeatAlert.
        :type: str
        """
        
        self._rule_id = rule_id

    @property
    def start_date(self):
        """
        Gets the start_date of this HeartBeatAlert.
        The date/time the alert was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The start_date of this HeartBeatAlert.
        :rtype: datetime
        """
        return self._start_date

    @start_date.setter
    def start_date(self, start_date):
        """
        Sets the start_date of this HeartBeatAlert.
        The date/time the alert was created. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param start_date: The start_date of this HeartBeatAlert.
        :type: datetime
        """
        
        self._start_date = start_date

    @property
    def end_date(self):
        """
        Gets the end_date of this HeartBeatAlert.
        The date/time the owning rule exiting in alarm status. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The end_date of this HeartBeatAlert.
        :rtype: datetime
        """
        return self._end_date

    @end_date.setter
    def end_date(self, end_date):
        """
        Sets the end_date of this HeartBeatAlert.
        The date/time the owning rule exiting in alarm status. Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param end_date: The end_date of this HeartBeatAlert.
        :type: datetime
        """
        
        self._end_date = end_date

    @property
    def notification_users(self):
        """
        Gets the notification_users of this HeartBeatAlert.
        The ids of users who were notified of alarm state change.

        :return: The notification_users of this HeartBeatAlert.
        :rtype: list[User]
        """
        return self._notification_users

    @notification_users.setter
    def notification_users(self, notification_users):
        """
        Sets the notification_users of this HeartBeatAlert.
        The ids of users who were notified of alarm state change.

        :param notification_users: The notification_users of this HeartBeatAlert.
        :type: list[User]
        """
        
        self._notification_users = notification_users

    @property
    def alert_types(self):
        """
        Gets the alert_types of this HeartBeatAlert.
        A collection of notification methods.

        :return: The alert_types of this HeartBeatAlert.
        :rtype: list[str]
        """
        return self._alert_types

    @alert_types.setter
    def alert_types(self, alert_types):
        """
        Sets the alert_types of this HeartBeatAlert.
        A collection of notification methods.

        :param alert_types: The alert_types of this HeartBeatAlert.
        :type: list[str]
        """
        
        self._alert_types = alert_types

    @property
    def rule_type(self):
        """
        Gets the rule_type of this HeartBeatAlert.
        The type of heartbeat rule that generated the alert

        :return: The rule_type of this HeartBeatAlert.
        :rtype: str
        """
        return self._rule_type

    @rule_type.setter
    def rule_type(self, rule_type):
        """
        Sets the rule_type of this HeartBeatAlert.
        The type of heartbeat rule that generated the alert

        :param rule_type: The rule_type of this HeartBeatAlert.
        :type: str
        """
        allowed_values = ["EDGE"]
        if rule_type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for rule_type -> " + rule_type
            self._rule_type = "outdated_sdk_version"
        else:
            self._rule_type = rule_type

    @property
    def rule_uri(self):
        """
        Gets the rule_uri of this HeartBeatAlert.


        :return: The rule_uri of this HeartBeatAlert.
        :rtype: str
        """
        return self._rule_uri

    @rule_uri.setter
    def rule_uri(self, rule_uri):
        """
        Sets the rule_uri of this HeartBeatAlert.


        :param rule_uri: The rule_uri of this HeartBeatAlert.
        :type: str
        """
        
        self._rule_uri = rule_uri

    @property
    def self_uri(self):
        """
        Gets the self_uri of this HeartBeatAlert.
        The URI for this object

        :return: The self_uri of this HeartBeatAlert.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this HeartBeatAlert.
        The URI for this object

        :param self_uri: The self_uri of this HeartBeatAlert.
        :type: str
        """
        
        self._self_uri = self_uri

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

