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

from .instance_view_status import InstanceViewStatus
from .sub_resource import SubResource
from .sku import Sku
from .availability_set import AvailabilitySet
from .virtual_machine_size import VirtualMachineSize
from .virtual_machine_extension_image import VirtualMachineExtensionImage
from .virtual_machine_image_resource import VirtualMachineImageResource
from .virtual_machine_extension_instance_view import VirtualMachineExtensionInstanceView
from .virtual_machine_extension import VirtualMachineExtension
from .purchase_plan import PurchasePlan
from .os_disk_image import OSDiskImage
from .data_disk_image import DataDiskImage
from .virtual_machine_image import VirtualMachineImage
from .usage_name import UsageName
from .usage import Usage
from .virtual_machine_capture_parameters import VirtualMachineCaptureParameters
from .virtual_machine_capture_result import VirtualMachineCaptureResult
from .plan import Plan
from .hardware_profile import HardwareProfile
from .image_reference import ImageReference
from .key_vault_secret_reference import KeyVaultSecretReference
from .key_vault_key_reference import KeyVaultKeyReference
from .disk_encryption_settings import DiskEncryptionSettings
from .virtual_hard_disk import VirtualHardDisk
from .managed_disk_parameters import ManagedDiskParameters
from .os_disk import OSDisk
from .data_disk import DataDisk
from .storage_profile import StorageProfile
from .additional_unattend_content import AdditionalUnattendContent
from .win_rm_listener import WinRMListener
from .win_rm_configuration import WinRMConfiguration
from .windows_configuration import WindowsConfiguration
from .ssh_public_key import SshPublicKey
from .ssh_configuration import SshConfiguration
from .linux_configuration import LinuxConfiguration
from .vault_certificate import VaultCertificate
from .vault_secret_group import VaultSecretGroup
from .os_profile import OSProfile
from .network_interface_reference import NetworkInterfaceReference
from .network_profile import NetworkProfile
from .boot_diagnostics import BootDiagnostics
from .diagnostics_profile import DiagnosticsProfile
from .virtual_machine_extension_handler_instance_view import VirtualMachineExtensionHandlerInstanceView
from .virtual_machine_agent_instance_view import VirtualMachineAgentInstanceView
from .disk_instance_view import DiskInstanceView
from .boot_diagnostics_instance_view import BootDiagnosticsInstanceView
from .virtual_machine_identity import VirtualMachineIdentity
from .virtual_machine_instance_view import VirtualMachineInstanceView
from .virtual_machine import VirtualMachine
from .upgrade_policy import UpgradePolicy
from .image_os_disk import ImageOSDisk
from .image_data_disk import ImageDataDisk
from .image_storage_profile import ImageStorageProfile
from .image import Image
from .virtual_machine_scale_set_identity import VirtualMachineScaleSetIdentity
from .virtual_machine_scale_set_os_profile import VirtualMachineScaleSetOSProfile
from .virtual_machine_scale_set_managed_disk_parameters import VirtualMachineScaleSetManagedDiskParameters
from .virtual_machine_scale_set_os_disk import VirtualMachineScaleSetOSDisk
from .virtual_machine_scale_set_data_disk import VirtualMachineScaleSetDataDisk
from .virtual_machine_scale_set_storage_profile import VirtualMachineScaleSetStorageProfile
from .api_entity_reference import ApiEntityReference
from .virtual_machine_scale_set_ip_configuration import VirtualMachineScaleSetIPConfiguration
from .virtual_machine_scale_set_network_configuration import VirtualMachineScaleSetNetworkConfiguration
from .virtual_machine_scale_set_network_profile import VirtualMachineScaleSetNetworkProfile
from .virtual_machine_scale_set_extension import VirtualMachineScaleSetExtension
from .virtual_machine_scale_set_extension_profile import VirtualMachineScaleSetExtensionProfile
from .virtual_machine_scale_set_vm_profile import VirtualMachineScaleSetVMProfile
from .virtual_machine_scale_set import VirtualMachineScaleSet
from .virtual_machine_scale_set_vm_instance_ids import VirtualMachineScaleSetVMInstanceIDs
from .virtual_machine_scale_set_vm_instance_required_ids import VirtualMachineScaleSetVMInstanceRequiredIDs
from .virtual_machine_status_code_count import VirtualMachineStatusCodeCount
from .virtual_machine_scale_set_instance_view_statuses_summary import VirtualMachineScaleSetInstanceViewStatusesSummary
from .virtual_machine_scale_set_vm_extensions_summary import VirtualMachineScaleSetVMExtensionsSummary
from .virtual_machine_scale_set_instance_view import VirtualMachineScaleSetInstanceView
from .virtual_machine_scale_set_sku_capacity import VirtualMachineScaleSetSkuCapacity
from .virtual_machine_scale_set_sku import VirtualMachineScaleSetSku
from .virtual_machine_scale_set_vm import VirtualMachineScaleSetVM
from .virtual_machine_scale_set_vm_instance_view import VirtualMachineScaleSetVMInstanceView
from .api_error_base import ApiErrorBase
from .inner_error import InnerError
from .api_error import ApiError
from .compute_long_running_operation_properties import ComputeLongRunningOperationProperties
from .resource import Resource
from .sub_resource_read_only import SubResourceReadOnly
from .operation_status_response import OperationStatusResponse
from .resource_update import ResourceUpdate
from .image_disk_reference import ImageDiskReference
from .creation_data import CreationData
from .source_vault import SourceVault
from .key_vault_and_secret_reference import KeyVaultAndSecretReference
from .key_vault_and_key_reference import KeyVaultAndKeyReference
from .encryption_settings import EncryptionSettings
from .disk import Disk
from .disk_update import DiskUpdate
from .grant_access_data import GrantAccessData
from .access_uri import AccessUri
from .snapshot import Snapshot
from .snapshot_update import SnapshotUpdate
from .availability_set_paged import AvailabilitySetPaged
from .virtual_machine_size_paged import VirtualMachineSizePaged
from .usage_paged import UsagePaged
from .image_paged import ImagePaged
from .virtual_machine_paged import VirtualMachinePaged
from .virtual_machine_scale_set_paged import VirtualMachineScaleSetPaged
from .virtual_machine_scale_set_sku_paged import VirtualMachineScaleSetSkuPaged
from .virtual_machine_scale_set_vm_paged import VirtualMachineScaleSetVMPaged
from .disk_paged import DiskPaged
from .snapshot_paged import SnapshotPaged
from .compute_management_client_enums import (
    StatusLevelTypes,
    OperatingSystemTypes,
    VirtualMachineSizeTypes,
    CachingTypes,
    DiskCreateOptionTypes,
    StorageAccountTypes,
    PassNames,
    ComponentNames,
    SettingNames,
    ProtocolTypes,
    ResourceIdentityType,
    UpgradeMode,
    OperatingSystemStateTypes,
    VirtualMachineScaleSetSkuScaleType,
    DiskCreateOption,
    AccessLevel,
    InstanceViewTypes,
)

__all__ = [
    'InstanceViewStatus',
    'SubResource',
    'Sku',
    'AvailabilitySet',
    'VirtualMachineSize',
    'VirtualMachineExtensionImage',
    'VirtualMachineImageResource',
    'VirtualMachineExtensionInstanceView',
    'VirtualMachineExtension',
    'PurchasePlan',
    'OSDiskImage',
    'DataDiskImage',
    'VirtualMachineImage',
    'UsageName',
    'Usage',
    'VirtualMachineCaptureParameters',
    'VirtualMachineCaptureResult',
    'Plan',
    'HardwareProfile',
    'ImageReference',
    'KeyVaultSecretReference',
    'KeyVaultKeyReference',
    'DiskEncryptionSettings',
    'VirtualHardDisk',
    'ManagedDiskParameters',
    'OSDisk',
    'DataDisk',
    'StorageProfile',
    'AdditionalUnattendContent',
    'WinRMListener',
    'WinRMConfiguration',
    'WindowsConfiguration',
    'SshPublicKey',
    'SshConfiguration',
    'LinuxConfiguration',
    'VaultCertificate',
    'VaultSecretGroup',
    'OSProfile',
    'NetworkInterfaceReference',
    'NetworkProfile',
    'BootDiagnostics',
    'DiagnosticsProfile',
    'VirtualMachineExtensionHandlerInstanceView',
    'VirtualMachineAgentInstanceView',
    'DiskInstanceView',
    'BootDiagnosticsInstanceView',
    'VirtualMachineIdentity',
    'VirtualMachineInstanceView',
    'VirtualMachine',
    'UpgradePolicy',
    'ImageOSDisk',
    'ImageDataDisk',
    'ImageStorageProfile',
    'Image',
    'VirtualMachineScaleSetIdentity',
    'VirtualMachineScaleSetOSProfile',
    'VirtualMachineScaleSetManagedDiskParameters',
    'VirtualMachineScaleSetOSDisk',
    'VirtualMachineScaleSetDataDisk',
    'VirtualMachineScaleSetStorageProfile',
    'ApiEntityReference',
    'VirtualMachineScaleSetIPConfiguration',
    'VirtualMachineScaleSetNetworkConfiguration',
    'VirtualMachineScaleSetNetworkProfile',
    'VirtualMachineScaleSetExtension',
    'VirtualMachineScaleSetExtensionProfile',
    'VirtualMachineScaleSetVMProfile',
    'VirtualMachineScaleSet',
    'VirtualMachineScaleSetVMInstanceIDs',
    'VirtualMachineScaleSetVMInstanceRequiredIDs',
    'VirtualMachineStatusCodeCount',
    'VirtualMachineScaleSetInstanceViewStatusesSummary',
    'VirtualMachineScaleSetVMExtensionsSummary',
    'VirtualMachineScaleSetInstanceView',
    'VirtualMachineScaleSetSkuCapacity',
    'VirtualMachineScaleSetSku',
    'VirtualMachineScaleSetVM',
    'VirtualMachineScaleSetVMInstanceView',
    'ApiErrorBase',
    'InnerError',
    'ApiError',
    'ComputeLongRunningOperationProperties',
    'Resource',
    'SubResourceReadOnly',
    'OperationStatusResponse',
    'ResourceUpdate',
    'ImageDiskReference',
    'CreationData',
    'SourceVault',
    'KeyVaultAndSecretReference',
    'KeyVaultAndKeyReference',
    'EncryptionSettings',
    'Disk',
    'DiskUpdate',
    'GrantAccessData',
    'AccessUri',
    'Snapshot',
    'SnapshotUpdate',
    'AvailabilitySetPaged',
    'VirtualMachineSizePaged',
    'UsagePaged',
    'ImagePaged',
    'VirtualMachinePaged',
    'VirtualMachineScaleSetPaged',
    'VirtualMachineScaleSetSkuPaged',
    'VirtualMachineScaleSetVMPaged',
    'DiskPaged',
    'SnapshotPaged',
    'StatusLevelTypes',
    'OperatingSystemTypes',
    'VirtualMachineSizeTypes',
    'CachingTypes',
    'DiskCreateOptionTypes',
    'StorageAccountTypes',
    'PassNames',
    'ComponentNames',
    'SettingNames',
    'ProtocolTypes',
    'ResourceIdentityType',
    'UpgradeMode',
    'OperatingSystemStateTypes',
    'VirtualMachineScaleSetSkuScaleType',
    'DiskCreateOption',
    'AccessLevel',
    'InstanceViewTypes',
]
