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


class LinuxConfiguration(Model):
    """Describes Windows configuration of the OS Profile.

    :param disable_password_authentication: Specifies whether password
     authentication should be disabled.
    :type disable_password_authentication: bool
    :param ssh: The SSH configuration for linux VMs.
    :type ssh: :class:`SshConfiguration
     <azure.mgmt.compute.compute.v2016_04_30_preview.models.SshConfiguration>`
    """

    _attribute_map = {
        'disable_password_authentication': {'key': 'disablePasswordAuthentication', 'type': 'bool'},
        'ssh': {'key': 'ssh', 'type': 'SshConfiguration'},
    }

    def __init__(self, disable_password_authentication=None, ssh=None):
        self.disable_password_authentication = disable_password_authentication
        self.ssh = ssh
