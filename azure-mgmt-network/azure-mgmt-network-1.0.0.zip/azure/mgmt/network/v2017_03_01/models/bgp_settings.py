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


class BgpSettings(Model):
    """BGP settings details.

    :param asn: The BGP speaker's ASN.
    :type asn: long
    :param bgp_peering_address: The BGP peering address and BGP identifier of
     this BGP speaker.
    :type bgp_peering_address: str
    :param peer_weight: The weight added to routes learned from this BGP
     speaker.
    :type peer_weight: int
    """

    _attribute_map = {
        'asn': {'key': 'asn', 'type': 'long'},
        'bgp_peering_address': {'key': 'bgpPeeringAddress', 'type': 'str'},
        'peer_weight': {'key': 'peerWeight', 'type': 'int'},
    }

    def __init__(self, asn=None, bgp_peering_address=None, peer_weight=None):
        self.asn = asn
        self.bgp_peering_address = bgp_peering_address
        self.peer_weight = peer_weight
