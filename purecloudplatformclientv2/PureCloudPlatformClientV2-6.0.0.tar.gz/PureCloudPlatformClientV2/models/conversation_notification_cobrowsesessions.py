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


class ConversationNotificationCobrowsesessions(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        ConversationNotificationCobrowsesessions - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'state': 'str',
            'disconnect_type': 'str',
            'id': 'str',
            'pcSelf': 'ConversationNotificationAddress',
            'room_id': 'str',
            'cobrowse_session_id': 'str',
            'cobrowse_role': 'str',
            'controlling': 'list[str]',
            'viewer_url': 'str',
            'provider': 'str',
            'script_id': 'str',
            'provider_event_time': 'datetime',
            'connected_time': 'datetime',
            'disconnected_time': 'datetime',
            'additional_properties': 'object'
        }

        self.attribute_map = {
            'state': 'state',
            'disconnect_type': 'disconnectType',
            'id': 'id',
            'pcSelf': 'self',
            'room_id': 'roomId',
            'cobrowse_session_id': 'cobrowseSessionId',
            'cobrowse_role': 'cobrowseRole',
            'controlling': 'controlling',
            'viewer_url': 'viewerUrl',
            'provider': 'provider',
            'script_id': 'scriptId',
            'provider_event_time': 'providerEventTime',
            'connected_time': 'connectedTime',
            'disconnected_time': 'disconnectedTime',
            'additional_properties': 'additionalProperties'
        }

        self._state = None
        self._disconnect_type = None
        self._id = None
        self._pcSelf = None
        self._room_id = None
        self._cobrowse_session_id = None
        self._cobrowse_role = None
        self._controlling = None
        self._viewer_url = None
        self._provider = None
        self._script_id = None
        self._provider_event_time = None
        self._connected_time = None
        self._disconnected_time = None
        self._additional_properties = None

    @property
    def state(self):
        """
        Gets the state of this ConversationNotificationCobrowsesessions.


        :return: The state of this ConversationNotificationCobrowsesessions.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this ConversationNotificationCobrowsesessions.


        :param state: The state of this ConversationNotificationCobrowsesessions.
        :type: str
        """
        allowed_values = ["ALERTING", "DIALING", "CONTACTING", "OFFERING", "CONNECTED", "DISCONNECTED", "TERMINATED", "NONE"]
        if state.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for state -> " + state
            self._state = "outdated_sdk_version"
        else:
            self._state = state

    @property
    def disconnect_type(self):
        """
        Gets the disconnect_type of this ConversationNotificationCobrowsesessions.


        :return: The disconnect_type of this ConversationNotificationCobrowsesessions.
        :rtype: str
        """
        return self._disconnect_type

    @disconnect_type.setter
    def disconnect_type(self, disconnect_type):
        """
        Sets the disconnect_type of this ConversationNotificationCobrowsesessions.


        :param disconnect_type: The disconnect_type of this ConversationNotificationCobrowsesessions.
        :type: str
        """
        allowed_values = ["ENDPOINT", "CLIENT", "SYSTEM", "TIMEOUT", "TRANSFER", "TRANSFER_CONFERENCE", "TRANSFER_CONSULT", "TRANSFER_FORWARD", "TRANSPORT_FAILURE", "ERROR", "PEER", "OTHER", "SPAM", "UNCALLABLE"]
        if disconnect_type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for disconnect_type -> " + disconnect_type
            self._disconnect_type = "outdated_sdk_version"
        else:
            self._disconnect_type = disconnect_type

    @property
    def id(self):
        """
        Gets the id of this ConversationNotificationCobrowsesessions.


        :return: The id of this ConversationNotificationCobrowsesessions.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this ConversationNotificationCobrowsesessions.


        :param id: The id of this ConversationNotificationCobrowsesessions.
        :type: str
        """
        
        self._id = id

    @property
    def pcSelf(self):
        """
        Gets the pcSelf of this ConversationNotificationCobrowsesessions.


        :return: The pcSelf of this ConversationNotificationCobrowsesessions.
        :rtype: ConversationNotificationAddress
        """
        return self._pcSelf

    @pcSelf.setter
    def pcSelf(self, pcSelf):
        """
        Sets the pcSelf of this ConversationNotificationCobrowsesessions.


        :param pcSelf: The pcSelf of this ConversationNotificationCobrowsesessions.
        :type: ConversationNotificationAddress
        """
        
        self._pcSelf = pcSelf

    @property
    def room_id(self):
        """
        Gets the room_id of this ConversationNotificationCobrowsesessions.


        :return: The room_id of this ConversationNotificationCobrowsesessions.
        :rtype: str
        """
        return self._room_id

    @room_id.setter
    def room_id(self, room_id):
        """
        Sets the room_id of this ConversationNotificationCobrowsesessions.


        :param room_id: The room_id of this ConversationNotificationCobrowsesessions.
        :type: str
        """
        
        self._room_id = room_id

    @property
    def cobrowse_session_id(self):
        """
        Gets the cobrowse_session_id of this ConversationNotificationCobrowsesessions.


        :return: The cobrowse_session_id of this ConversationNotificationCobrowsesessions.
        :rtype: str
        """
        return self._cobrowse_session_id

    @cobrowse_session_id.setter
    def cobrowse_session_id(self, cobrowse_session_id):
        """
        Sets the cobrowse_session_id of this ConversationNotificationCobrowsesessions.


        :param cobrowse_session_id: The cobrowse_session_id of this ConversationNotificationCobrowsesessions.
        :type: str
        """
        
        self._cobrowse_session_id = cobrowse_session_id

    @property
    def cobrowse_role(self):
        """
        Gets the cobrowse_role of this ConversationNotificationCobrowsesessions.


        :return: The cobrowse_role of this ConversationNotificationCobrowsesessions.
        :rtype: str
        """
        return self._cobrowse_role

    @cobrowse_role.setter
    def cobrowse_role(self, cobrowse_role):
        """
        Sets the cobrowse_role of this ConversationNotificationCobrowsesessions.


        :param cobrowse_role: The cobrowse_role of this ConversationNotificationCobrowsesessions.
        :type: str
        """
        
        self._cobrowse_role = cobrowse_role

    @property
    def controlling(self):
        """
        Gets the controlling of this ConversationNotificationCobrowsesessions.


        :return: The controlling of this ConversationNotificationCobrowsesessions.
        :rtype: list[str]
        """
        return self._controlling

    @controlling.setter
    def controlling(self, controlling):
        """
        Sets the controlling of this ConversationNotificationCobrowsesessions.


        :param controlling: The controlling of this ConversationNotificationCobrowsesessions.
        :type: list[str]
        """
        
        self._controlling = controlling

    @property
    def viewer_url(self):
        """
        Gets the viewer_url of this ConversationNotificationCobrowsesessions.


        :return: The viewer_url of this ConversationNotificationCobrowsesessions.
        :rtype: str
        """
        return self._viewer_url

    @viewer_url.setter
    def viewer_url(self, viewer_url):
        """
        Sets the viewer_url of this ConversationNotificationCobrowsesessions.


        :param viewer_url: The viewer_url of this ConversationNotificationCobrowsesessions.
        :type: str
        """
        
        self._viewer_url = viewer_url

    @property
    def provider(self):
        """
        Gets the provider of this ConversationNotificationCobrowsesessions.


        :return: The provider of this ConversationNotificationCobrowsesessions.
        :rtype: str
        """
        return self._provider

    @provider.setter
    def provider(self, provider):
        """
        Sets the provider of this ConversationNotificationCobrowsesessions.


        :param provider: The provider of this ConversationNotificationCobrowsesessions.
        :type: str
        """
        
        self._provider = provider

    @property
    def script_id(self):
        """
        Gets the script_id of this ConversationNotificationCobrowsesessions.


        :return: The script_id of this ConversationNotificationCobrowsesessions.
        :rtype: str
        """
        return self._script_id

    @script_id.setter
    def script_id(self, script_id):
        """
        Sets the script_id of this ConversationNotificationCobrowsesessions.


        :param script_id: The script_id of this ConversationNotificationCobrowsesessions.
        :type: str
        """
        
        self._script_id = script_id

    @property
    def provider_event_time(self):
        """
        Gets the provider_event_time of this ConversationNotificationCobrowsesessions.


        :return: The provider_event_time of this ConversationNotificationCobrowsesessions.
        :rtype: datetime
        """
        return self._provider_event_time

    @provider_event_time.setter
    def provider_event_time(self, provider_event_time):
        """
        Sets the provider_event_time of this ConversationNotificationCobrowsesessions.


        :param provider_event_time: The provider_event_time of this ConversationNotificationCobrowsesessions.
        :type: datetime
        """
        
        self._provider_event_time = provider_event_time

    @property
    def connected_time(self):
        """
        Gets the connected_time of this ConversationNotificationCobrowsesessions.


        :return: The connected_time of this ConversationNotificationCobrowsesessions.
        :rtype: datetime
        """
        return self._connected_time

    @connected_time.setter
    def connected_time(self, connected_time):
        """
        Sets the connected_time of this ConversationNotificationCobrowsesessions.


        :param connected_time: The connected_time of this ConversationNotificationCobrowsesessions.
        :type: datetime
        """
        
        self._connected_time = connected_time

    @property
    def disconnected_time(self):
        """
        Gets the disconnected_time of this ConversationNotificationCobrowsesessions.


        :return: The disconnected_time of this ConversationNotificationCobrowsesessions.
        :rtype: datetime
        """
        return self._disconnected_time

    @disconnected_time.setter
    def disconnected_time(self, disconnected_time):
        """
        Sets the disconnected_time of this ConversationNotificationCobrowsesessions.


        :param disconnected_time: The disconnected_time of this ConversationNotificationCobrowsesessions.
        :type: datetime
        """
        
        self._disconnected_time = disconnected_time

    @property
    def additional_properties(self):
        """
        Gets the additional_properties of this ConversationNotificationCobrowsesessions.


        :return: The additional_properties of this ConversationNotificationCobrowsesessions.
        :rtype: object
        """
        return self._additional_properties

    @additional_properties.setter
    def additional_properties(self, additional_properties):
        """
        Sets the additional_properties of this ConversationNotificationCobrowsesessions.


        :param additional_properties: The additional_properties of this ConversationNotificationCobrowsesessions.
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

