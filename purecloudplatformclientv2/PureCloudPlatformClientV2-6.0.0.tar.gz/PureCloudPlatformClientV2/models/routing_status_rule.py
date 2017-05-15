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


class RoutingStatusRule(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        RoutingStatusRule - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'agent': 'User',
            'routing_status': 'str',
            'routing_limit_in_seconds': 'int',
            'enabled': 'bool',
            'in_alarm': 'bool',
            'notification_users': 'list[User]',
            'alert_types': 'list[str]',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'agent': 'agent',
            'routing_status': 'routingStatus',
            'routing_limit_in_seconds': 'routingLimitInSeconds',
            'enabled': 'enabled',
            'in_alarm': 'inAlarm',
            'notification_users': 'notificationUsers',
            'alert_types': 'alertTypes',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._agent = None
        self._routing_status = None
        self._routing_limit_in_seconds = None
        self._enabled = None
        self._in_alarm = None
        self._notification_users = None
        self._alert_types = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this RoutingStatusRule.
        The globally unique identifier for the object.

        :return: The id of this RoutingStatusRule.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this RoutingStatusRule.
        The globally unique identifier for the object.

        :param id: The id of this RoutingStatusRule.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this RoutingStatusRule.
        Name of the rule

        :return: The name of this RoutingStatusRule.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this RoutingStatusRule.
        Name of the rule

        :param name: The name of this RoutingStatusRule.
        :type: str
        """
        
        self._name = name

    @property
    def agent(self):
        """
        Gets the agent of this RoutingStatusRule.
        The agent whose routing status will be watched.

        :return: The agent of this RoutingStatusRule.
        :rtype: User
        """
        return self._agent

    @agent.setter
    def agent(self, agent):
        """
        Sets the agent of this RoutingStatusRule.
        The agent whose routing status will be watched.

        :param agent: The agent of this RoutingStatusRule.
        :type: User
        """
        
        self._agent = agent

    @property
    def routing_status(self):
        """
        Gets the routing_status of this RoutingStatusRule.
        The routing status on which to alert.

        :return: The routing_status of this RoutingStatusRule.
        :rtype: str
        """
        return self._routing_status

    @routing_status.setter
    def routing_status(self, routing_status):
        """
        Sets the routing_status of this RoutingStatusRule.
        The routing status on which to alert.

        :param routing_status: The routing_status of this RoutingStatusRule.
        :type: str
        """
        allowed_values = ["OFF_QUEUE", "IDLE", "INTERACTING", "NOT_RESPONDING", "COMMUNICATING"]
        if routing_status.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for routing_status -> " + routing_status
            self._routing_status = "outdated_sdk_version"
        else:
            self._routing_status = routing_status

    @property
    def routing_limit_in_seconds(self):
        """
        Gets the routing_limit_in_seconds of this RoutingStatusRule.
        The number of seconds to wait before alerting based upon the agent's routing status.

        :return: The routing_limit_in_seconds of this RoutingStatusRule.
        :rtype: int
        """
        return self._routing_limit_in_seconds

    @routing_limit_in_seconds.setter
    def routing_limit_in_seconds(self, routing_limit_in_seconds):
        """
        Sets the routing_limit_in_seconds of this RoutingStatusRule.
        The number of seconds to wait before alerting based upon the agent's routing status.

        :param routing_limit_in_seconds: The routing_limit_in_seconds of this RoutingStatusRule.
        :type: int
        """
        
        self._routing_limit_in_seconds = routing_limit_in_seconds

    @property
    def enabled(self):
        """
        Gets the enabled of this RoutingStatusRule.
        Indicates if the rule is enabled.

        :return: The enabled of this RoutingStatusRule.
        :rtype: bool
        """
        return self._enabled

    @enabled.setter
    def enabled(self, enabled):
        """
        Sets the enabled of this RoutingStatusRule.
        Indicates if the rule is enabled.

        :param enabled: The enabled of this RoutingStatusRule.
        :type: bool
        """
        
        self._enabled = enabled

    @property
    def in_alarm(self):
        """
        Gets the in_alarm of this RoutingStatusRule.
        Indicates if the rule is in alarm state.

        :return: The in_alarm of this RoutingStatusRule.
        :rtype: bool
        """
        return self._in_alarm

    @in_alarm.setter
    def in_alarm(self, in_alarm):
        """
        Sets the in_alarm of this RoutingStatusRule.
        Indicates if the rule is in alarm state.

        :param in_alarm: The in_alarm of this RoutingStatusRule.
        :type: bool
        """
        
        self._in_alarm = in_alarm

    @property
    def notification_users(self):
        """
        Gets the notification_users of this RoutingStatusRule.
        The ids of users who will be notified of alarm state change.

        :return: The notification_users of this RoutingStatusRule.
        :rtype: list[User]
        """
        return self._notification_users

    @notification_users.setter
    def notification_users(self, notification_users):
        """
        Sets the notification_users of this RoutingStatusRule.
        The ids of users who will be notified of alarm state change.

        :param notification_users: The notification_users of this RoutingStatusRule.
        :type: list[User]
        """
        
        self._notification_users = notification_users

    @property
    def alert_types(self):
        """
        Gets the alert_types of this RoutingStatusRule.
        A collection of notification methods.

        :return: The alert_types of this RoutingStatusRule.
        :rtype: list[str]
        """
        return self._alert_types

    @alert_types.setter
    def alert_types(self, alert_types):
        """
        Sets the alert_types of this RoutingStatusRule.
        A collection of notification methods.

        :param alert_types: The alert_types of this RoutingStatusRule.
        :type: list[str]
        """
        
        self._alert_types = alert_types

    @property
    def self_uri(self):
        """
        Gets the self_uri of this RoutingStatusRule.
        The URI for this object

        :return: The self_uri of this RoutingStatusRule.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this RoutingStatusRule.
        The URI for this object

        :param self_uri: The self_uri of this RoutingStatusRule.
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

