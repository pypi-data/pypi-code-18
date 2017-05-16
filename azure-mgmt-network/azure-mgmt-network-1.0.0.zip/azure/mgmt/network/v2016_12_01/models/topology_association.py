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


class TopologyAssociation(Model):
    """Resources that have an association with the parent resource.

    :param name: The name of the resource that is associated with the parent
     resource.
    :type name: str
    :param resource_id: The ID of the resource that is associated with the
     parent resource.
    :type resource_id: str
    :param association_type: The association type of the child resource to the
     parent resource. Possible values include: 'Associated', 'Contains'
    :type association_type: str or :class:`AssociationType
     <azure.mgmt.network.v2016_12_01.models.AssociationType>`
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'resource_id': {'key': 'resourceId', 'type': 'str'},
        'association_type': {'key': 'associationType', 'type': 'str'},
    }

    def __init__(self, name=None, resource_id=None, association_type=None):
        self.name = name
        self.resource_id = resource_id
        self.association_type = association_type
