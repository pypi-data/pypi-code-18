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

from enum import Enum


class Reason(Enum):

    account_name_invalid = "AccountNameInvalid"
    already_exists = "AlreadyExists"


class SkuName(Enum):

    standard_lrs = "Standard_LRS"
    standard_grs = "Standard_GRS"
    standard_ragrs = "Standard_RAGRS"
    standard_zrs = "Standard_ZRS"
    premium_lrs = "Premium_LRS"


class SkuTier(Enum):

    standard = "Standard"
    premium = "Premium"


class AccessTier(Enum):

    hot = "Hot"
    cool = "Cool"


class Kind(Enum):

    storage = "Storage"
    blob_storage = "BlobStorage"


class ProvisioningState(Enum):

    creating = "Creating"
    resolving_dns = "ResolvingDNS"
    succeeded = "Succeeded"


class AccountStatus(Enum):

    available = "available"
    unavailable = "unavailable"


class KeyPermission(Enum):

    read = "Read"
    full = "Full"


class UsageUnit(Enum):

    count = "Count"
    bytes = "Bytes"
    seconds = "Seconds"
    percent = "Percent"
    counts_per_second = "CountsPerSecond"
    bytes_per_second = "BytesPerSecond"


class HttpProtocol(Enum):

    httpshttp = "https,http"
    https = "https"
