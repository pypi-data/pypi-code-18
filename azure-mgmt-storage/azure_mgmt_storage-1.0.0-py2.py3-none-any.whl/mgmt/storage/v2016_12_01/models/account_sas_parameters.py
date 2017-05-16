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


class AccountSasParameters(Model):
    """The parameters to list SAS credentials of a storage account.

    :param services: The signed services accessible with the account SAS.
     Possible values include: Blob (b), Queue (q), Table (t), File (f).
     Possible values include: 'b', 'q', 't', 'f'
    :type services: str or :class:`enum
     <azure.mgmt.storage.v2016_12_01.models.enum>`
    :param resource_types: The signed resource types that are accessible with
     the account SAS. Service (s): Access to service-level APIs; Container (c):
     Access to container-level APIs; Object (o): Access to object-level APIs
     for blobs, queue messages, table entities, and files. Possible values
     include: 's', 'c', 'o'
    :type resource_types: str or :class:`enum
     <azure.mgmt.storage.v2016_12_01.models.enum>`
    :param permissions: The signed permissions for the account SAS. Possible
     values include: Read (r), Write (w), Delete (d), List (l), Add (a), Create
     (c), Update (u) and Process (p). Possible values include: 'r', 'd', 'w',
     'l', 'a', 'c', 'u', 'p'
    :type permissions: str or :class:`enum
     <azure.mgmt.storage.v2016_12_01.models.enum>`
    :param ip_address_or_range: An IP address or a range of IP addresses from
     which to accept requests.
    :type ip_address_or_range: str
    :param protocols: The protocol permitted for a request made with the
     account SAS. Possible values include: 'https,http', 'https'
    :type protocols: str or :class:`HttpProtocol
     <azure.mgmt.storage.v2016_12_01.models.HttpProtocol>`
    :param shared_access_start_time: The time at which the SAS becomes valid.
    :type shared_access_start_time: datetime
    :param shared_access_expiry_time: The time at which the shared access
     signature becomes invalid.
    :type shared_access_expiry_time: datetime
    :param key_to_sign: The key to sign the account SAS token with.
    :type key_to_sign: str
    """

    _validation = {
        'services': {'required': True},
        'resource_types': {'required': True},
        'permissions': {'required': True},
        'shared_access_expiry_time': {'required': True},
    }

    _attribute_map = {
        'services': {'key': 'signedServices', 'type': 'str'},
        'resource_types': {'key': 'signedResourceTypes', 'type': 'str'},
        'permissions': {'key': 'signedPermission', 'type': 'str'},
        'ip_address_or_range': {'key': 'signedIp', 'type': 'str'},
        'protocols': {'key': 'signedProtocol', 'type': 'HttpProtocol'},
        'shared_access_start_time': {'key': 'signedStart', 'type': 'iso-8601'},
        'shared_access_expiry_time': {'key': 'signedExpiry', 'type': 'iso-8601'},
        'key_to_sign': {'key': 'keyToSign', 'type': 'str'},
    }

    def __init__(self, services, resource_types, permissions, shared_access_expiry_time, ip_address_or_range=None, protocols=None, shared_access_start_time=None, key_to_sign=None):
        self.services = services
        self.resource_types = resource_types
        self.permissions = permissions
        self.ip_address_or_range = ip_address_or_range
        self.protocols = protocols
        self.shared_access_start_time = shared_access_start_time
        self.shared_access_expiry_time = shared_access_expiry_time
        self.key_to_sign = key_to_sign
