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


class Deployment(Model):
    """Deployment operation parameters.

    :param properties: The deployment properties.
    :type properties: :class:`DeploymentProperties
     <azure.mgmt.resource.resources.v2017_05_10.models.DeploymentProperties>`
    """

    _validation = {
        'properties': {'required': True},
    }

    _attribute_map = {
        'properties': {'key': 'properties', 'type': 'DeploymentProperties'},
    }

    def __init__(self, properties):
        self.properties = properties
