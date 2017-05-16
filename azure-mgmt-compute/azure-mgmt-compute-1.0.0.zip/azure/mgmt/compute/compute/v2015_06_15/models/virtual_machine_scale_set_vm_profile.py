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


class VirtualMachineScaleSetVMProfile(Model):
    """Describes a virtual machine scale set virtual machine profile.

    :param os_profile: The virtual machine scale set OS profile.
    :type os_profile: :class:`VirtualMachineScaleSetOSProfile
     <azure.mgmt.compute.compute.v2015_06_15.models.VirtualMachineScaleSetOSProfile>`
    :param storage_profile: The virtual machine scale set storage profile.
    :type storage_profile: :class:`VirtualMachineScaleSetStorageProfile
     <azure.mgmt.compute.compute.v2015_06_15.models.VirtualMachineScaleSetStorageProfile>`
    :param network_profile: The virtual machine scale set network profile.
    :type network_profile: :class:`VirtualMachineScaleSetNetworkProfile
     <azure.mgmt.compute.compute.v2015_06_15.models.VirtualMachineScaleSetNetworkProfile>`
    :param extension_profile: The virtual machine scale set extension profile.
    :type extension_profile: :class:`VirtualMachineScaleSetExtensionProfile
     <azure.mgmt.compute.compute.v2015_06_15.models.VirtualMachineScaleSetExtensionProfile>`
    """

    _attribute_map = {
        'os_profile': {'key': 'osProfile', 'type': 'VirtualMachineScaleSetOSProfile'},
        'storage_profile': {'key': 'storageProfile', 'type': 'VirtualMachineScaleSetStorageProfile'},
        'network_profile': {'key': 'networkProfile', 'type': 'VirtualMachineScaleSetNetworkProfile'},
        'extension_profile': {'key': 'extensionProfile', 'type': 'VirtualMachineScaleSetExtensionProfile'},
    }

    def __init__(self, os_profile=None, storage_profile=None, network_profile=None, extension_profile=None):
        self.os_profile = os_profile
        self.storage_profile = storage_profile
        self.network_profile = network_profile
        self.extension_profile = extension_profile
