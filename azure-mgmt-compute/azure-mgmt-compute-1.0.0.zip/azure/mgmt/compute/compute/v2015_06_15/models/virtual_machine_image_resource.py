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

from .sub_resource import SubResource


class VirtualMachineImageResource(SubResource):
    """Virtual machine image resource information.

    :param id: Resource Id
    :type id: str
    :param name: The name of the resource.
    :type name: str
    :param location: The supported Azure location of the resource.
    :type location: str
    :param tags: The tags attached to the resource.
    :type tags: dict
    """

    _validation = {
        'name': {'required': True},
        'location': {'required': True},
    }

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'name': {'key': 'name', 'type': 'str'},
        'location': {'key': 'location', 'type': 'str'},
        'tags': {'key': 'tags', 'type': '{str}'},
    }

    def __init__(self, name, location, id=None, tags=None):
        super(VirtualMachineImageResource, self).__init__(id=id)
        self.name = name
        self.location = location
        self.tags = tags
