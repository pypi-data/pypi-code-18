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


class ApplicationGatewayBackendHealthPool(Model):
    """Application gateway BackendHealth pool.

    :param backend_address_pool: Reference of an
     ApplicationGatewayBackendAddressPool resource.
    :type backend_address_pool: :class:`ApplicationGatewayBackendAddressPool
     <azure.mgmt.network.v2016_09_01.models.ApplicationGatewayBackendAddressPool>`
    :param backend_http_settings_collection: List of
     ApplicationGatewayBackendHealthHttpSettings resources.
    :type backend_http_settings_collection: list of
     :class:`ApplicationGatewayBackendHealthHttpSettings
     <azure.mgmt.network.v2016_09_01.models.ApplicationGatewayBackendHealthHttpSettings>`
    """

    _attribute_map = {
        'backend_address_pool': {'key': 'backendAddressPool', 'type': 'ApplicationGatewayBackendAddressPool'},
        'backend_http_settings_collection': {'key': 'backendHttpSettingsCollection', 'type': '[ApplicationGatewayBackendHealthHttpSettings]'},
    }

    def __init__(self, backend_address_pool=None, backend_http_settings_collection=None):
        self.backend_address_pool = backend_address_pool
        self.backend_http_settings_collection = backend_http_settings_collection
