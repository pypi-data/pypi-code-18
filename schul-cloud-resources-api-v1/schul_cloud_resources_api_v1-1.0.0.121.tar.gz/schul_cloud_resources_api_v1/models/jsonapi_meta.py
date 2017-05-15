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


class JsonapiMeta(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self, name=None, source=None, description=None):
        """
        JsonapiMeta - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'name': 'str',
            'source': 'str',
            'description': 'str'
        }

        self.attribute_map = {
            'name': 'name',
            'source': 'source',
            'description': 'description'
        }

        self._name = name
        self._source = source
        self._description = description

    @property
    def name(self):
        """
        Gets the name of this JsonapiMeta.
        The name of the server.

        :return: The name of this JsonapiMeta.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this JsonapiMeta.
        The name of the server.

        :param name: The name of this JsonapiMeta.
        :type: str
        """
        if name is None:
            raise ValueError("Invalid value for `name`, must not be `None`")

        self._name = name

    @property
    def source(self):
        """
        Gets the source of this JsonapiMeta.
        The implementation of ther server, i.e. the repository.

        :return: The source of this JsonapiMeta.
        :rtype: str
        """
        return self._source

    @source.setter
    def source(self, source):
        """
        Sets the source of this JsonapiMeta.
        The implementation of ther server, i.e. the repository.

        :param source: The source of this JsonapiMeta.
        :type: str
        """
        if source is None:
            raise ValueError("Invalid value for `source`, must not be `None`")

        self._source = source

    @property
    def description(self):
        """
        Gets the description of this JsonapiMeta.
        A description of the server.

        :return: The description of this JsonapiMeta.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this JsonapiMeta.
        A description of the server.

        :param description: The description of this JsonapiMeta.
        :type: str
        """
        if description is None:
            raise ValueError("Invalid value for `description`, must not be `None`")

        self._description = description

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
        if not isinstance(other, JsonapiMeta):
            return False

        return self.__dict__ == other.__dict__

    def __ne__(self, other):
        """
        Returns true if both objects are not equal
        """
        return not self == other
