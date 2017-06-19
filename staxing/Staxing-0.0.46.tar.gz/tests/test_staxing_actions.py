"""Staxing test files - Actions."""

# import logging
# import pytest
import unittest

# from selenium.webdriver.remote.remote_connection import LOGGER
from staxing.actions import Actions
# from time import sleep

__version__ = '0.0.0'


class TestStaxingActions(unittest.TestCase):
    """Staxing case tests for the ActionChain sleep."""

    def setUp(self):
        """Pretest settings."""
        self.action_chain = Actions()

    def tearDown(self):
        """Test destructor."""
        try:
            self.action_chain.__del__()
        except:
            pass
