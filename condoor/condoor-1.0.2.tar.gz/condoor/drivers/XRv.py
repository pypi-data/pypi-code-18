"""This is IOS XRv driver implementation."""

import logging
from condoor.drivers.XR import Driver as eXR
from condoor import pattern_manager

logger = logging.getLogger(__name__)


class Driver(eXR):
    """This is a Driver class implementation for IOS XRv."""

    platform = 'XRv'
    inventory_cmd = 'admin show inventory chassis'
    users_cmd = 'show users'
    target_prompt_components = ['prompt_dynamic', 'prompt_default', 'rommon', 'xml']
    prepare_terminal_session = ['terminal exec prompt no-timestamp', 'terminal len 0', 'terminal width 0']
    reload_cmd = 'admin reload location all'
    families = {
        "IOS XRv 9000": "IOSXRv-9K",
        "IOS XRv x64": "IOSXRv-X64",
    }

    def update_driver(self, prompt):
        """Return driver name based on prompt analysis."""
        return pattern_manager.platform(prompt, ['XRv', 'Calvados', 'Windriver'])
