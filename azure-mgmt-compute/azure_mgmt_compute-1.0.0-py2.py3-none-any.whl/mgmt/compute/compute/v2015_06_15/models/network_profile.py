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


class NetworkProfile(Model):
    """Describes a network profile.

    :param network_interfaces: Specifies the list of resource IDs for the
     network interfaces associated with the virtual machine.
    :type network_interfaces: list of :class:`NetworkInterfaceReference
     <azure.mgmt.compute.compute.v2015_06_15.models.NetworkInterfaceReference>`
    """

    _attribute_map = {
        'network_interfaces': {'key': 'networkInterfaces', 'type': '[NetworkInterfaceReference]'},
    }

    def __init__(self, network_interfaces=None):
        self.network_interfaces = network_interfaces
