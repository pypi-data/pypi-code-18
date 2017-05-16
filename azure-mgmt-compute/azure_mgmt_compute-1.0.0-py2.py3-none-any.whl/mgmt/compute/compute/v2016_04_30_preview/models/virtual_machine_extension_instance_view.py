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


class VirtualMachineExtensionInstanceView(Model):
    """The instance view of a virtual machine extension.

    :param name: The virtual machine extension name.
    :type name: str
    :param type: The full type of the extension handler which includes both
     publisher and type.
    :type type: str
    :param type_handler_version: The type version of the extension handler.
    :type type_handler_version: str
    :param substatuses: The resource status information.
    :type substatuses: list of :class:`InstanceViewStatus
     <azure.mgmt.compute.compute.v2016_04_30_preview.models.InstanceViewStatus>`
    :param statuses: The resource status information.
    :type statuses: list of :class:`InstanceViewStatus
     <azure.mgmt.compute.compute.v2016_04_30_preview.models.InstanceViewStatus>`
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'type': {'key': 'type', 'type': 'str'},
        'type_handler_version': {'key': 'typeHandlerVersion', 'type': 'str'},
        'substatuses': {'key': 'substatuses', 'type': '[InstanceViewStatus]'},
        'statuses': {'key': 'statuses', 'type': '[InstanceViewStatus]'},
    }

    def __init__(self, name=None, type=None, type_handler_version=None, substatuses=None, statuses=None):
        self.name = name
        self.type = type
        self.type_handler_version = type_handler_version
        self.substatuses = substatuses
        self.statuses = statuses
