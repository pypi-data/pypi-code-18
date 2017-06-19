# -*- coding: utf-8 -*-
"""
Created on Mon Oct 31 14:27:37 2016

@author: Pedro
"""
VERSION = '1.0.1'
DESCRIPTION = 'settings_parser: Load, parse and validate user settings'

from settings_parser.settings import Settings
from settings_parser.value import Value, DictValue, Kind

__all__ = ["Settings", "Value", "DictValue", 'Kind']