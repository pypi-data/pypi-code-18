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


class AddressSpace(Model):
    """AddressSpace contains an array of IP address ranges that can be used by
    subnets of the virtual network.

    :param address_prefixes: A list of address blocks reserved for this
     virtual network in CIDR notation.
    :type address_prefixes: list of str
    """

    _attribute_map = {
        'address_prefixes': {'key': 'addressPrefixes', 'type': '[str]'},
    }

    def __init__(self, address_prefixes=None):
        self.address_prefixes = address_prefixes
