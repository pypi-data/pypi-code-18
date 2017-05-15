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


class Edge(object):
    """
    NOTE: This class is auto generated by the swagger code generator program.
    Do not edit the class manually.
    """
    def __init__(self):
        """
        Edge - a model defined in Swagger

        :param dict swaggerTypes: The key is attribute name
                                  and the value is attribute type.
        :param dict attributeMap: The key is attribute name
                                  and the value is json key in definition.
        """
        self.swagger_types = {
            'id': 'str',
            'name': 'str',
            'description': 'str',
            'version': 'int',
            'date_created': 'datetime',
            'date_modified': 'datetime',
            'modified_by': 'str',
            'created_by': 'str',
            'state': 'str',
            'modified_by_app': 'str',
            'created_by_app': 'str',
            'interfaces': 'list[EdgeInterface]',
            'make': 'str',
            'model': 'str',
            'api_version': 'str',
            'software_version': 'str',
            'software_version_timestamp': 'str',
            'software_version_platform': 'str',
            'software_version_configuration': 'str',
            'full_software_version': 'str',
            'pairing_id': 'str',
            'fingerprint': 'str',
            'fingerprint_hint': 'str',
            'current_version': 'str',
            'staged_version': 'str',
            'patch': 'str',
            'status_code': 'str',
            'edge_group': 'EdgeGroup',
            'site': 'Site',
            'software_status': 'DomainEdgeSoftwareUpdateDto',
            'online_status': 'str',
            'serial_number': 'str',
            'physical_edge': 'bool',
            'managed': 'bool',
            'edge_deployment_type': 'str',
            'call_draining_state': 'str',
            'conversation_count': 'int',
            'proxy': 'str',
            'self_uri': 'str'
        }

        self.attribute_map = {
            'id': 'id',
            'name': 'name',
            'description': 'description',
            'version': 'version',
            'date_created': 'dateCreated',
            'date_modified': 'dateModified',
            'modified_by': 'modifiedBy',
            'created_by': 'createdBy',
            'state': 'state',
            'modified_by_app': 'modifiedByApp',
            'created_by_app': 'createdByApp',
            'interfaces': 'interfaces',
            'make': 'make',
            'model': 'model',
            'api_version': 'apiVersion',
            'software_version': 'softwareVersion',
            'software_version_timestamp': 'softwareVersionTimestamp',
            'software_version_platform': 'softwareVersionPlatform',
            'software_version_configuration': 'softwareVersionConfiguration',
            'full_software_version': 'fullSoftwareVersion',
            'pairing_id': 'pairingId',
            'fingerprint': 'fingerprint',
            'fingerprint_hint': 'fingerprintHint',
            'current_version': 'currentVersion',
            'staged_version': 'stagedVersion',
            'patch': 'patch',
            'status_code': 'statusCode',
            'edge_group': 'edgeGroup',
            'site': 'site',
            'software_status': 'softwareStatus',
            'online_status': 'onlineStatus',
            'serial_number': 'serialNumber',
            'physical_edge': 'physicalEdge',
            'managed': 'managed',
            'edge_deployment_type': 'edgeDeploymentType',
            'call_draining_state': 'callDrainingState',
            'conversation_count': 'conversationCount',
            'proxy': 'proxy',
            'self_uri': 'selfUri'
        }

        self._id = None
        self._name = None
        self._description = None
        self._version = None
        self._date_created = None
        self._date_modified = None
        self._modified_by = None
        self._created_by = None
        self._state = None
        self._modified_by_app = None
        self._created_by_app = None
        self._interfaces = None
        self._make = None
        self._model = None
        self._api_version = None
        self._software_version = None
        self._software_version_timestamp = None
        self._software_version_platform = None
        self._software_version_configuration = None
        self._full_software_version = None
        self._pairing_id = None
        self._fingerprint = None
        self._fingerprint_hint = None
        self._current_version = None
        self._staged_version = None
        self._patch = None
        self._status_code = None
        self._edge_group = None
        self._site = None
        self._software_status = None
        self._online_status = None
        self._serial_number = None
        self._physical_edge = None
        self._managed = None
        self._edge_deployment_type = None
        self._call_draining_state = None
        self._conversation_count = None
        self._proxy = None
        self._self_uri = None

    @property
    def id(self):
        """
        Gets the id of this Edge.
        The globally unique identifier for the object.

        :return: The id of this Edge.
        :rtype: str
        """
        return self._id

    @id.setter
    def id(self, id):
        """
        Sets the id of this Edge.
        The globally unique identifier for the object.

        :param id: The id of this Edge.
        :type: str
        """
        
        self._id = id

    @property
    def name(self):
        """
        Gets the name of this Edge.
        The name of the entity.

        :return: The name of this Edge.
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Sets the name of this Edge.
        The name of the entity.

        :param name: The name of this Edge.
        :type: str
        """
        
        self._name = name

    @property
    def description(self):
        """
        Gets the description of this Edge.


        :return: The description of this Edge.
        :rtype: str
        """
        return self._description

    @description.setter
    def description(self, description):
        """
        Sets the description of this Edge.


        :param description: The description of this Edge.
        :type: str
        """
        
        self._description = description

    @property
    def version(self):
        """
        Gets the version of this Edge.


        :return: The version of this Edge.
        :rtype: int
        """
        return self._version

    @version.setter
    def version(self, version):
        """
        Sets the version of this Edge.


        :param version: The version of this Edge.
        :type: int
        """
        
        self._version = version

    @property
    def date_created(self):
        """
        Gets the date_created of this Edge.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_created of this Edge.
        :rtype: datetime
        """
        return self._date_created

    @date_created.setter
    def date_created(self, date_created):
        """
        Sets the date_created of this Edge.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_created: The date_created of this Edge.
        :type: datetime
        """
        
        self._date_created = date_created

    @property
    def date_modified(self):
        """
        Gets the date_modified of this Edge.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :return: The date_modified of this Edge.
        :rtype: datetime
        """
        return self._date_modified

    @date_modified.setter
    def date_modified(self, date_modified):
        """
        Sets the date_modified of this Edge.
        Date time is represented as an ISO-8601 string. For example: yyyy-MM-ddTHH:mm:ss.SSSZ

        :param date_modified: The date_modified of this Edge.
        :type: datetime
        """
        
        self._date_modified = date_modified

    @property
    def modified_by(self):
        """
        Gets the modified_by of this Edge.


        :return: The modified_by of this Edge.
        :rtype: str
        """
        return self._modified_by

    @modified_by.setter
    def modified_by(self, modified_by):
        """
        Sets the modified_by of this Edge.


        :param modified_by: The modified_by of this Edge.
        :type: str
        """
        
        self._modified_by = modified_by

    @property
    def created_by(self):
        """
        Gets the created_by of this Edge.


        :return: The created_by of this Edge.
        :rtype: str
        """
        return self._created_by

    @created_by.setter
    def created_by(self, created_by):
        """
        Sets the created_by of this Edge.


        :param created_by: The created_by of this Edge.
        :type: str
        """
        
        self._created_by = created_by

    @property
    def state(self):
        """
        Gets the state of this Edge.


        :return: The state of this Edge.
        :rtype: str
        """
        return self._state

    @state.setter
    def state(self, state):
        """
        Sets the state of this Edge.


        :param state: The state of this Edge.
        :type: str
        """
        allowed_values = ["active", "inactive", "deleted"]
        if state.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for state -> " + state
            self._state = "outdated_sdk_version"
        else:
            self._state = state

    @property
    def modified_by_app(self):
        """
        Gets the modified_by_app of this Edge.


        :return: The modified_by_app of this Edge.
        :rtype: str
        """
        return self._modified_by_app

    @modified_by_app.setter
    def modified_by_app(self, modified_by_app):
        """
        Sets the modified_by_app of this Edge.


        :param modified_by_app: The modified_by_app of this Edge.
        :type: str
        """
        
        self._modified_by_app = modified_by_app

    @property
    def created_by_app(self):
        """
        Gets the created_by_app of this Edge.


        :return: The created_by_app of this Edge.
        :rtype: str
        """
        return self._created_by_app

    @created_by_app.setter
    def created_by_app(self, created_by_app):
        """
        Sets the created_by_app of this Edge.


        :param created_by_app: The created_by_app of this Edge.
        :type: str
        """
        
        self._created_by_app = created_by_app

    @property
    def interfaces(self):
        """
        Gets the interfaces of this Edge.


        :return: The interfaces of this Edge.
        :rtype: list[EdgeInterface]
        """
        return self._interfaces

    @interfaces.setter
    def interfaces(self, interfaces):
        """
        Sets the interfaces of this Edge.


        :param interfaces: The interfaces of this Edge.
        :type: list[EdgeInterface]
        """
        
        self._interfaces = interfaces

    @property
    def make(self):
        """
        Gets the make of this Edge.


        :return: The make of this Edge.
        :rtype: str
        """
        return self._make

    @make.setter
    def make(self, make):
        """
        Sets the make of this Edge.


        :param make: The make of this Edge.
        :type: str
        """
        
        self._make = make

    @property
    def model(self):
        """
        Gets the model of this Edge.


        :return: The model of this Edge.
        :rtype: str
        """
        return self._model

    @model.setter
    def model(self, model):
        """
        Sets the model of this Edge.


        :param model: The model of this Edge.
        :type: str
        """
        
        self._model = model

    @property
    def api_version(self):
        """
        Gets the api_version of this Edge.


        :return: The api_version of this Edge.
        :rtype: str
        """
        return self._api_version

    @api_version.setter
    def api_version(self, api_version):
        """
        Sets the api_version of this Edge.


        :param api_version: The api_version of this Edge.
        :type: str
        """
        
        self._api_version = api_version

    @property
    def software_version(self):
        """
        Gets the software_version of this Edge.


        :return: The software_version of this Edge.
        :rtype: str
        """
        return self._software_version

    @software_version.setter
    def software_version(self, software_version):
        """
        Sets the software_version of this Edge.


        :param software_version: The software_version of this Edge.
        :type: str
        """
        
        self._software_version = software_version

    @property
    def software_version_timestamp(self):
        """
        Gets the software_version_timestamp of this Edge.


        :return: The software_version_timestamp of this Edge.
        :rtype: str
        """
        return self._software_version_timestamp

    @software_version_timestamp.setter
    def software_version_timestamp(self, software_version_timestamp):
        """
        Sets the software_version_timestamp of this Edge.


        :param software_version_timestamp: The software_version_timestamp of this Edge.
        :type: str
        """
        
        self._software_version_timestamp = software_version_timestamp

    @property
    def software_version_platform(self):
        """
        Gets the software_version_platform of this Edge.


        :return: The software_version_platform of this Edge.
        :rtype: str
        """
        return self._software_version_platform

    @software_version_platform.setter
    def software_version_platform(self, software_version_platform):
        """
        Sets the software_version_platform of this Edge.


        :param software_version_platform: The software_version_platform of this Edge.
        :type: str
        """
        
        self._software_version_platform = software_version_platform

    @property
    def software_version_configuration(self):
        """
        Gets the software_version_configuration of this Edge.


        :return: The software_version_configuration of this Edge.
        :rtype: str
        """
        return self._software_version_configuration

    @software_version_configuration.setter
    def software_version_configuration(self, software_version_configuration):
        """
        Sets the software_version_configuration of this Edge.


        :param software_version_configuration: The software_version_configuration of this Edge.
        :type: str
        """
        
        self._software_version_configuration = software_version_configuration

    @property
    def full_software_version(self):
        """
        Gets the full_software_version of this Edge.


        :return: The full_software_version of this Edge.
        :rtype: str
        """
        return self._full_software_version

    @full_software_version.setter
    def full_software_version(self, full_software_version):
        """
        Sets the full_software_version of this Edge.


        :param full_software_version: The full_software_version of this Edge.
        :type: str
        """
        
        self._full_software_version = full_software_version

    @property
    def pairing_id(self):
        """
        Gets the pairing_id of this Edge.
        The pairing Id for a hardware Edge in the format: 00000-00000-00000-00000-00000. This field is only required when creating an Edge with a deployment type of HARDWARE.

        :return: The pairing_id of this Edge.
        :rtype: str
        """
        return self._pairing_id

    @pairing_id.setter
    def pairing_id(self, pairing_id):
        """
        Sets the pairing_id of this Edge.
        The pairing Id for a hardware Edge in the format: 00000-00000-00000-00000-00000. This field is only required when creating an Edge with a deployment type of HARDWARE.

        :param pairing_id: The pairing_id of this Edge.
        :type: str
        """
        
        self._pairing_id = pairing_id

    @property
    def fingerprint(self):
        """
        Gets the fingerprint of this Edge.


        :return: The fingerprint of this Edge.
        :rtype: str
        """
        return self._fingerprint

    @fingerprint.setter
    def fingerprint(self, fingerprint):
        """
        Sets the fingerprint of this Edge.


        :param fingerprint: The fingerprint of this Edge.
        :type: str
        """
        
        self._fingerprint = fingerprint

    @property
    def fingerprint_hint(self):
        """
        Gets the fingerprint_hint of this Edge.


        :return: The fingerprint_hint of this Edge.
        :rtype: str
        """
        return self._fingerprint_hint

    @fingerprint_hint.setter
    def fingerprint_hint(self, fingerprint_hint):
        """
        Sets the fingerprint_hint of this Edge.


        :param fingerprint_hint: The fingerprint_hint of this Edge.
        :type: str
        """
        
        self._fingerprint_hint = fingerprint_hint

    @property
    def current_version(self):
        """
        Gets the current_version of this Edge.


        :return: The current_version of this Edge.
        :rtype: str
        """
        return self._current_version

    @current_version.setter
    def current_version(self, current_version):
        """
        Sets the current_version of this Edge.


        :param current_version: The current_version of this Edge.
        :type: str
        """
        
        self._current_version = current_version

    @property
    def staged_version(self):
        """
        Gets the staged_version of this Edge.


        :return: The staged_version of this Edge.
        :rtype: str
        """
        return self._staged_version

    @staged_version.setter
    def staged_version(self, staged_version):
        """
        Sets the staged_version of this Edge.


        :param staged_version: The staged_version of this Edge.
        :type: str
        """
        
        self._staged_version = staged_version

    @property
    def patch(self):
        """
        Gets the patch of this Edge.


        :return: The patch of this Edge.
        :rtype: str
        """
        return self._patch

    @patch.setter
    def patch(self, patch):
        """
        Sets the patch of this Edge.


        :param patch: The patch of this Edge.
        :type: str
        """
        
        self._patch = patch

    @property
    def status_code(self):
        """
        Gets the status_code of this Edge.


        :return: The status_code of this Edge.
        :rtype: str
        """
        return self._status_code

    @status_code.setter
    def status_code(self, status_code):
        """
        Sets the status_code of this Edge.


        :param status_code: The status_code of this Edge.
        :type: str
        """
        allowed_values = ["NEW", "AWAITING_CONNECTION", "AWAITING_FINGERPRINT", "AWAITING_FINGERPRINT_VERIFICATION", "FINGERPRINT_VERIFIED", "AWAITING_BOOTSTRAP", "ACTIVE", "INACTIVE", "RMA", "UNPAIRING", "UNPAIRED"]
        if status_code.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for status_code -> " + status_code
            self._status_code = "outdated_sdk_version"
        else:
            self._status_code = status_code

    @property
    def edge_group(self):
        """
        Gets the edge_group of this Edge.


        :return: The edge_group of this Edge.
        :rtype: EdgeGroup
        """
        return self._edge_group

    @edge_group.setter
    def edge_group(self, edge_group):
        """
        Sets the edge_group of this Edge.


        :param edge_group: The edge_group of this Edge.
        :type: EdgeGroup
        """
        
        self._edge_group = edge_group

    @property
    def site(self):
        """
        Gets the site of this Edge.
        The Site to which the Edge is assigned.

        :return: The site of this Edge.
        :rtype: Site
        """
        return self._site

    @site.setter
    def site(self, site):
        """
        Sets the site of this Edge.
        The Site to which the Edge is assigned.

        :param site: The site of this Edge.
        :type: Site
        """
        
        self._site = site

    @property
    def software_status(self):
        """
        Gets the software_status of this Edge.


        :return: The software_status of this Edge.
        :rtype: DomainEdgeSoftwareUpdateDto
        """
        return self._software_status

    @software_status.setter
    def software_status(self, software_status):
        """
        Sets the software_status of this Edge.


        :param software_status: The software_status of this Edge.
        :type: DomainEdgeSoftwareUpdateDto
        """
        
        self._software_status = software_status

    @property
    def online_status(self):
        """
        Gets the online_status of this Edge.


        :return: The online_status of this Edge.
        :rtype: str
        """
        return self._online_status

    @online_status.setter
    def online_status(self, online_status):
        """
        Sets the online_status of this Edge.


        :param online_status: The online_status of this Edge.
        :type: str
        """
        allowed_values = ["ONLINE", "OFFLINE"]
        if online_status.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for online_status -> " + online_status
            self._online_status = "outdated_sdk_version"
        else:
            self._online_status = online_status

    @property
    def serial_number(self):
        """
        Gets the serial_number of this Edge.


        :return: The serial_number of this Edge.
        :rtype: str
        """
        return self._serial_number

    @serial_number.setter
    def serial_number(self, serial_number):
        """
        Sets the serial_number of this Edge.


        :param serial_number: The serial_number of this Edge.
        :type: str
        """
        
        self._serial_number = serial_number

    @property
    def physical_edge(self):
        """
        Gets the physical_edge of this Edge.


        :return: The physical_edge of this Edge.
        :rtype: bool
        """
        return self._physical_edge

    @physical_edge.setter
    def physical_edge(self, physical_edge):
        """
        Sets the physical_edge of this Edge.


        :param physical_edge: The physical_edge of this Edge.
        :type: bool
        """
        
        self._physical_edge = physical_edge

    @property
    def managed(self):
        """
        Gets the managed of this Edge.


        :return: The managed of this Edge.
        :rtype: bool
        """
        return self._managed

    @managed.setter
    def managed(self, managed):
        """
        Sets the managed of this Edge.


        :param managed: The managed of this Edge.
        :type: bool
        """
        
        self._managed = managed

    @property
    def edge_deployment_type(self):
        """
        Gets the edge_deployment_type of this Edge.


        :return: The edge_deployment_type of this Edge.
        :rtype: str
        """
        return self._edge_deployment_type

    @edge_deployment_type.setter
    def edge_deployment_type(self, edge_deployment_type):
        """
        Sets the edge_deployment_type of this Edge.


        :param edge_deployment_type: The edge_deployment_type of this Edge.
        :type: str
        """
        allowed_values = ["HARDWARE", "LDM", "CDM", "INVALID"]
        if edge_deployment_type.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for edge_deployment_type -> " + edge_deployment_type
            self._edge_deployment_type = "outdated_sdk_version"
        else:
            self._edge_deployment_type = edge_deployment_type

    @property
    def call_draining_state(self):
        """
        Gets the call_draining_state of this Edge.


        :return: The call_draining_state of this Edge.
        :rtype: str
        """
        return self._call_draining_state

    @call_draining_state.setter
    def call_draining_state(self, call_draining_state):
        """
        Sets the call_draining_state of this Edge.


        :param call_draining_state: The call_draining_state of this Edge.
        :type: str
        """
        allowed_values = ["NONE", "WAIT", "WAIT_TIMEOUT", "TERMINATE", "COMPLETE"]
        if call_draining_state.lower() not in map(str.lower, allowed_values):
            # print "Invalid value for call_draining_state -> " + call_draining_state
            self._call_draining_state = "outdated_sdk_version"
        else:
            self._call_draining_state = call_draining_state

    @property
    def conversation_count(self):
        """
        Gets the conversation_count of this Edge.


        :return: The conversation_count of this Edge.
        :rtype: int
        """
        return self._conversation_count

    @conversation_count.setter
    def conversation_count(self, conversation_count):
        """
        Sets the conversation_count of this Edge.


        :param conversation_count: The conversation_count of this Edge.
        :type: int
        """
        
        self._conversation_count = conversation_count

    @property
    def proxy(self):
        """
        Gets the proxy of this Edge.
        Edge HTTP proxy configuration for the WAN port. The field can be a hostname, FQDN, IPv4 or IPv6 address. If port is not included, port 80 is assumed.

        :return: The proxy of this Edge.
        :rtype: str
        """
        return self._proxy

    @proxy.setter
    def proxy(self, proxy):
        """
        Sets the proxy of this Edge.
        Edge HTTP proxy configuration for the WAN port. The field can be a hostname, FQDN, IPv4 or IPv6 address. If port is not included, port 80 is assumed.

        :param proxy: The proxy of this Edge.
        :type: str
        """
        
        self._proxy = proxy

    @property
    def self_uri(self):
        """
        Gets the self_uri of this Edge.
        The URI for this object

        :return: The self_uri of this Edge.
        :rtype: str
        """
        return self._self_uri

    @self_uri.setter
    def self_uri(self, self_uri):
        """
        Sets the self_uri of this Edge.
        The URI for this object

        :param self_uri: The self_uri of this Edge.
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

