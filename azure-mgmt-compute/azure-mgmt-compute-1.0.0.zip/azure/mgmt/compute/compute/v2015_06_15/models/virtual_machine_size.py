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


class VirtualMachineSize(Model):
    """Describes the properties of a VM size.

    :param name: The name of the virtual machine size.
    :type name: str
    :param number_of_cores: The number of cores supported by the virtual
     machine size.
    :type number_of_cores: int
    :param os_disk_size_in_mb: The OS disk size, in MB, allowed by the virtual
     machine size.
    :type os_disk_size_in_mb: int
    :param resource_disk_size_in_mb: The resource disk size, in MB, allowed by
     the virtual machine size.
    :type resource_disk_size_in_mb: int
    :param memory_in_mb: The amount of memory, in MB, supported by the virtual
     machine size.
    :type memory_in_mb: int
    :param max_data_disk_count: The maximum number of data disks that can be
     attached to the virtual machine size.
    :type max_data_disk_count: int
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'number_of_cores': {'key': 'numberOfCores', 'type': 'int'},
        'os_disk_size_in_mb': {'key': 'osDiskSizeInMB', 'type': 'int'},
        'resource_disk_size_in_mb': {'key': 'resourceDiskSizeInMB', 'type': 'int'},
        'memory_in_mb': {'key': 'memoryInMB', 'type': 'int'},
        'max_data_disk_count': {'key': 'maxDataDiskCount', 'type': 'int'},
    }

    def __init__(self, name=None, number_of_cores=None, os_disk_size_in_mb=None, resource_disk_size_in_mb=None, memory_in_mb=None, max_data_disk_count=None):
        self.name = name
        self.number_of_cores = number_of_cores
        self.os_disk_size_in_mb = os_disk_size_in_mb
        self.resource_disk_size_in_mb = resource_disk_size_in_mb
        self.memory_in_mb = memory_in_mb
        self.max_data_disk_count = max_data_disk_count
