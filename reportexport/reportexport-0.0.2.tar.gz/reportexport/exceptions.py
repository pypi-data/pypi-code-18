# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals


class InvalidTemplate(Exception):
    """There is no template for given extension."""


class AlreadyRegisteredError(Exception):
    """A template for given extension is already been registered."""
