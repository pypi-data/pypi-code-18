# coding=utf-8
# --------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for
# license information.
#
# Code generated by Microsoft (R) AutoRest Code Generator.
# Changes may cause incorrect behavior and will be lost if the code is
# regenerated.
# --------------------------------------------------------------------------

from msrest.serialization import Model


class DeploymentExtended(Model):
    """Deployment information.

    :param id: The ID of the deployment.
    :type id: str
    :param name: The name of the deployment.
    :type name: str
    :param properties: Deployment properties.
    :type properties: :class:`DeploymentPropertiesExtended
     <azure.mgmt.resource.resources.v2017_05_10.models.DeploymentPropertiesExtended>`
    """

    _validation = {
        'name': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'properties': {'key': 'properties', 'type': 'DeploymentPropertiesExtended'},
    }

    def __init__(self, name, id=None, properties=None):
        self.id = id
        self.name = name
        self.properties = properties
