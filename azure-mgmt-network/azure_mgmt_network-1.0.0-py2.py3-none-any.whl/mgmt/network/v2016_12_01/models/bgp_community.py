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


class BGPCommunity(Model):
    """Contains bgp community information offered in Service Community resources.

    :param service_supported_region: The region which the service support.
     e.g. For O365, region is Global.
    :type service_supported_region: str
    :param community_name: The name of the bgp community. e.g. Skype.
    :type community_name: str
    :param community_value: The value of the bgp community. For more
     information:
     https://docs.microsoft.com/en-us/azure/expressroute/expressroute-routing.
    :type community_value: str
    :param community_prefixes: The prefixes that the bgp community contains.
    :type community_prefixes: list of str
    """

    _attribute_map = {
        'service_supported_region': {'key': 'serviceSupportedRegion', 'type': 'str'},
        'community_name': {'key': 'communityName', 'type': 'str'},
        'community_value': {'key': 'communityValue', 'type': 'str'},
        'community_prefixes': {'key': 'communityPrefixes', 'type': '[str]'},
    }

    def __init__(self, service_supported_region=None, community_name=None, community_value=None, community_prefixes=None):
        self.service_supported_region = service_supported_region
        self.community_name = community_name
        self.community_value = community_value
        self.community_prefixes = community_prefixes
