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


class ExpressRouteCircuitPeeringConfig(Model):
    """Specifies the peering configuration.

    :param advertised_public_prefixes: The reference of
     AdvertisedPublicPrefixes.
    :type advertised_public_prefixes: list of str
    :param advertised_public_prefixes_state: AdvertisedPublicPrefixState of
     the Peering resource. Possible values are 'NotConfigured', 'Configuring',
     'Configured', and 'ValidationNeeded'. Possible values include:
     'NotConfigured', 'Configuring', 'Configured', 'ValidationNeeded'
    :type advertised_public_prefixes_state: str or
     :class:`ExpressRouteCircuitPeeringAdvertisedPublicPrefixState
     <azure.mgmt.network.v2015_06_15.models.ExpressRouteCircuitPeeringAdvertisedPublicPrefixState>`
    :param customer_asn: The CustomerASN of the peering.
    :type customer_asn: int
    :param routing_registry_name: The RoutingRegistryName of the
     configuration.
    :type routing_registry_name: str
    """

    _attribute_map = {
        'advertised_public_prefixes': {'key': 'advertisedPublicPrefixes', 'type': '[str]'},
        'advertised_public_prefixes_state': {'key': 'advertisedPublicPrefixesState', 'type': 'str'},
        'customer_asn': {'key': 'customerASN', 'type': 'int'},
        'routing_registry_name': {'key': 'routingRegistryName', 'type': 'str'},
    }

    def __init__(self, advertised_public_prefixes=None, advertised_public_prefixes_state=None, customer_asn=None, routing_registry_name=None):
        self.advertised_public_prefixes = advertised_public_prefixes
        self.advertised_public_prefixes_state = advertised_public_prefixes_state
        self.customer_asn = customer_asn
        self.routing_registry_name = routing_registry_name
