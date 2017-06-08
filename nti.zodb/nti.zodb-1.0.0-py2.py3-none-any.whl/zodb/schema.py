#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Deprecated, do not use.
"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import zope.deferredimport
zope.deferredimport.initialize()
zope.deferredimport.deprecatedFrom(
    "Moved to nti.schema.field",
    "nti.schema.field",
    "FieldValidationMixin",
    "Number")
