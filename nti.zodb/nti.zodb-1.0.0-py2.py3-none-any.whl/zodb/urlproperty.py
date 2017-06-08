#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Classes and utilities for working with URLs stored on persistent objects.

Deprecated, do not use.

"""

from __future__ import print_function, absolute_import, division
__docformat__ = "restructuredtext en"

logger = __import__('logging').getLogger(__name__)

import zope.deprecation
zope.deprecation.moved('nti.property.urlproperty')
