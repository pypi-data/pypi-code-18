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


class DnsNameAvailabilityResult(Model):
    """Response for the CheckDnsNameAvailability API service call.

    :param available: Domain availability (True/False).
    :type available: bool
    """

    _attribute_map = {
        'available': {'key': 'available', 'type': 'bool'},
    }

    def __init__(self, available=None):
        self.available = available
