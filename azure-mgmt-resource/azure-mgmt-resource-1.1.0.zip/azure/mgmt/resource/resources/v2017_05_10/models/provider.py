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


class Provider(Model):
    """Resource provider information.

    Variables are only populated by the server, and will be ignored when
    sending a request.

    :ivar id: The provider ID.
    :vartype id: str
    :param namespace: The namespace of the resource provider.
    :type namespace: str
    :ivar registration_state: The registration state of the provider.
    :vartype registration_state: str
    :ivar resource_types: The collection of provider resource types.
    :vartype resource_types: list of :class:`ProviderResourceType
     <azure.mgmt.resource.resources.v2017_05_10.models.ProviderResourceType>`
    """

    _validation = {
        'id': {'readonly': True},
        'registration_state': {'readonly': True},
        'resource_types': {'readonly': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'namespace': {'key': 'namespace', 'type': 'str'},
        'registration_state': {'key': 'registrationState', 'type': 'str'},
        'resource_types': {'key': 'resourceTypes', 'type': '[ProviderResourceType]'},
    }

    def __init__(self, namespace=None):
        self.id = None
        self.namespace = namespace
        self.registration_state = None
        self.resource_types = None
