"""Staxing test files - Page Load."""

# import logging
# import pytest
import unittest

# from selenium.webdriver.remote.remote_connection import LOGGER
from staxing.page_load import SeleniumWait
# from time import sleep

__version__ = '0.0.0'


class TestStaxingSeleniumWait(unittest.TestCase):
    """Staxing case tests for the page loading wait."""

    def setUp(self):
        """Pretest settings."""
        self.wait = SeleniumWait()

    def tearDown(self):
        """Test destructor."""
        try:
            self.wait.__del__()
        except:
            pass
