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


class InboundDomain(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        InboundDomain - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'mx_record_status': 'str',
            'sub_domain': 'bool',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'mx_record_status': 'mxRecordStatus',
            'sub_domain': 'subDomain',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._mx_record_status = None
        self._sub_domain = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this InboundDomain.
        The globally unique identifier for the object.

        :return: The id of this InboundDomain.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this InboundDomain.
        The globally unique identifier for the object.

        :param id: The id of this InboundDomain.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this InboundDomain.


        :return: The name of this InboundDomain.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this InboundDomain.


        :param name: The name of this InboundDomain.
        :type: str
        """
        
        self._name = name

    @property
    def mx_record_status(self):
        """
        Gets the mx_record_status of this InboundDomain.
        Mx Record Status

        :return: The mx_record_status of this InboundDomain.
        :rtype: str
        """
        return self._mx_record_status

    @mx_record_status.setter
    def mx_record_status(self, mx_record_status):
        """
        Sets the mx_record_status of this InboundDomain.
        Mx Record Status

        :param mx_record_status: The mx_record_status of this InboundDomain.
        :type: str
        """
        allowed_values = ["VALID", "INVALID", "NOT_AVAILABLE"]
        if mx_record_status.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for mx_record_status -> " + mx_record_status
            self._mx_record_status = "outdated_sdk_version"
        else:
            self._mx_record_status = mx_record_status

    @property
    def sub_domain(self):
        """
        Gets the sub_domain of this InboundDomain.
        Indicates if this a PureCloud sub-domain.  If true, then the appropriate DNS records are created for sending/receiving email.

        :return: The sub_domain of this InboundDomain.
        :rtype: bool
        """
        return self._sub_domain

    @sub_domain.setter
    def sub_domain(self, sub_domain):
        """
        Sets the sub_domain of this InboundDomain.
        Indicates if this a PureCloud sub-domain.  If true, then the appropriate DNS records are created for sending/receiving email.

        :param sub_domain: The sub_domain of this InboundDomain.
        :type: bool
        """
        
        self._sub_domain = sub_domain

    @property
    def self_uri(self):
        """
        Gets the self_uri of this InboundDomain.
        The URI for this object

        :return: The self_uri of this InboundDomain.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this InboundDomain.
        The URI for this object

        :param self_uri: The self_uri of this InboundDomain.
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

