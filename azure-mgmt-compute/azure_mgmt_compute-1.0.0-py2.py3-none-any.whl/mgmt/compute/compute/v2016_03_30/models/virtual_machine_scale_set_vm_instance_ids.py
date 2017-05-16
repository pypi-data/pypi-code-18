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


class VirtualMachineScaleSetVMInstanceIDs(Model):
    """Specifies a list of virtual machine instance IDs from the VM scale set.

    :param instance_ids: The virtual machine scale set instance ids.
    :type instance_ids: list of str
    """

    _attribute_map = {
        'instance_ids': {'key': 'instanceIds', 'type': '[str]'},
    }

    def __init__(self, instance_ids=None):
        self.instance_ids = instance_ids
