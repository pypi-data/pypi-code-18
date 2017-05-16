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


class TagValue(Model):
    """Tag information.

    :param id: The tag ID.
    :type id: str
    :param tag_value: The tag value.
    :type tag_value: str
    :param count: The tag value count.
    :type count: :class:`TagCount
     <azure.mgmt.resource.resources.v2016_02_01.models.TagCount>`
    """

    _attribute_map = {
        'id': {'key': 'id', 'type': 'str'},
        'tag_value': {'key': 'tagValue', 'type': 'str'},
        'count': {'key': 'count', 'type': 'TagCount'},
    }

    def __init__(self, id=None, tag_value=None, count=None):
        self.id = id
        self.tag_value = tag_value
        self.count = count
