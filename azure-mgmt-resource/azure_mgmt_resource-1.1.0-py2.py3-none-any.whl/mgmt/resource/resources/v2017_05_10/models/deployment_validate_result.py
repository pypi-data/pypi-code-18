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


class DeploymentValidateResult(Model):
    """Information from validate template deployment response.

    :param error: Validation error.
    :type error: :class:`ResourceManagementErrorWithDetails
     <azure.mgmt.resource.resources.v2017_05_10.models.ResourceManagementErrorWithDetails>`
    :param properties: The template deployment properties.
    :type properties: :class:`DeploymentPropertiesExtended
     <azure.mgmt.resource.resources.v2017_05_10.models.DeploymentPropertiesExtended>`
    """

    _attribute_map = {
        'error': {'key': 'error', 'type': 'ResourceManagementErrorWithDetails'},
        'properties': {'key': 'properties', 'type': 'DeploymentPropertiesExtended'},
    }

    def __init__(self, error=None, properties=None):
        self.error = error
        self.properties = properties
