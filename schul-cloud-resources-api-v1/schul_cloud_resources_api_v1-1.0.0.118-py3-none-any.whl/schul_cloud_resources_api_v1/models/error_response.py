# coding: utf-8

"""
    Schul-Cloud Content API

    This is the specification fo rthe content of Schul-Cloud. You can find more information in the [repository](https://github.com/schul-cloud/resources-api-v1). 

    OpenAPI spec version: 1.0.0
    
    Generated by: https://github.com/swagger-api/swagger-codegen.git
"""


from pprint import pformat
from six import iteritems
import re


class ErrorResponse(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, jsonapi=None, errors=None):
        """
        ErrorResponse - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'jsonapi': 'Jsonapi',
            'errors': 'list[ErrorElement]'
        }

        self.attribute_map = {
            'jsonapi': 'jsonapi',
            'errors': 'errors'
        }

        self._jsonapi = jsonapi
        self._errors = errors

    @property
    def jsonapi(self):
        """
        Gets the jsonapi of this ErrorResponse.

        :return: The jsonapi of this ErrorResponse.
        :rtype: Jsonapi
        """
        return self._jsonapi

    @jsonapi.setter
    def jsonapi(self, jsonapi):
        """
        Sets the jsonapi of this ErrorResponse.

        :param jsonapi: The jsonapi of this ErrorResponse.
        :type: Jsonapi
        """
        if jsonapi is None:
            raise ValueError("Invalid value for `jsonapi`, must not be `None`")

        self._jsonapi = jsonapi

    @property
    def errors(self):
        """
        Gets the errors of this ErrorResponse.

        :return: The errors of this ErrorResponse.
        :rtype: list[ErrorElement]
        """
        return self._errors

    @errors.setter
    def errors(self, errors):
        """
        Sets the errors of this ErrorResponse.

        :param errors: The errors of this ErrorResponse.
        :type: list[ErrorElement]
        """
        if errors is None:
            raise ValueError("Invalid value for `errors`, must not be `None`")

        self._errors = errors

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
        if not isinstance(other, ErrorResponse):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
