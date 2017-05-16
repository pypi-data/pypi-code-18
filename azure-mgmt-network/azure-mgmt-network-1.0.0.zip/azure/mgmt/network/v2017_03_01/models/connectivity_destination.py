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


class ConnectivityDestination(Model):
    """Parameters that define destination of connection.

    :param resource_id: The ID of the resource to which a connection attempt
     will be made.
    :type resource_id: str
    :param address: The IP address or URI the resource to which a connection
     attempt will be made.
    :type address: str
    :param port: Port on which check connectivity will be performed.
    :type port: int
    """

    _attribute_map = {
        'resource_id': {'key': 'resourceId', 'type': 'str'},
        'address': {'key': 'address', 'type': 'str'},
        'port': {'key': 'port', 'type': 'int'},
    }

    def __init__(self, resource_id=None, address=None, port=None):
        self.resource_id = resource_id
        self.address = address
        self.port = port
