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


class EffectiveNetworkSecurityRule(Model):
    """Effective network security rules.

    :param name: The name of the security rule specified by the user (if
     created by the user).
    :type name: str
    :param protocol: The network protocol this rule applies to. Possible
     values are: 'Tcp', 'Udp', and '*'. Possible values include: 'Tcp', 'Udp',
     '*'
    :type protocol: str or :class:`SecurityRuleProtocol
     <azure.mgmt.network.v2016_09_01.models.SecurityRuleProtocol>`
    :param source_port_range: The source port or range.
    :type source_port_range: str
    :param destination_port_range: The destination port or range.
    :type destination_port_range: str
    :param source_address_prefix: The source address prefix.
    :type source_address_prefix: str
    :param destination_address_prefix: The destination address prefix.
    :type destination_address_prefix: str
    :param expanded_source_address_prefix: The expanded source address prefix.
    :type expanded_source_address_prefix: list of str
    :param expanded_destination_address_prefix: Expanded destination address
     prefix.
    :type expanded_destination_address_prefix: list of str
    :param access: Whether network traffic is allowed or denied. Possible
     values are: 'Allow' and 'Deny'. Possible values include: 'Allow', 'Deny'
    :type access: str or :class:`SecurityRuleAccess
     <azure.mgmt.network.v2016_09_01.models.SecurityRuleAccess>`
    :param priority: The priority of the rule.
    :type priority: int
    :param direction: The direction of the rule. Possible values are: 'Inbound
     and Outbound'. Possible values include: 'Inbound', 'Outbound'
    :type direction: str or :class:`SecurityRuleDirection
     <azure.mgmt.network.v2016_09_01.models.SecurityRuleDirection>`
    """

    _attribute_map = {
        'name': {'key': 'name', 'type': 'str'},
        'protocol': {'key': 'protocol', 'type': 'str'},
        'source_port_range': {'key': 'sourcePortRange', 'type': 'str'},
        'destination_port_range': {'key': 'destinationPortRange', 'type': 'str'},
        'source_address_prefix': {'key': 'sourceAddressPrefix', 'type': 'str'},
        'destination_address_prefix': {'key': 'destinationAddressPrefix', 'type': 'str'},
        'expanded_source_address_prefix': {'key': 'expandedSourceAddressPrefix', 'type': '[str]'},
        'expanded_destination_address_prefix': {'key': 'expandedDestinationAddressPrefix', 'type': '[str]'},
        'access': {'key': 'access', 'type': 'str'},
        'priority': {'key': 'priority', 'type': 'int'},
        'direction': {'key': 'direction', 'type': 'str'},
    }

    def __init__(self, name=None, protocol=None, source_port_range=None, destination_port_range=None, source_address_prefix=None, destination_address_prefix=None, expanded_source_address_prefix=None, expanded_destination_address_prefix=None, access=None, priority=None, direction=None):
        self.name = name
        self.protocol = protocol
        self.source_port_range = source_port_range
        self.destination_port_range = destination_port_range
        self.source_address_prefix = source_address_prefix
        self.destination_address_prefix = destination_address_prefix
        self.expanded_source_address_prefix = expanded_source_address_prefix
        self.expanded_destination_address_prefix = expanded_destination_address_prefix
        self.access = access
        self.priority = priority
        self.direction = direction
