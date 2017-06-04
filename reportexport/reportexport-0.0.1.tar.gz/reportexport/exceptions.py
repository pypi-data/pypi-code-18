# -*- coding: utf-8 -*-
class InvalidTemplate(Exception):
    """There is no template for given extension."""


class AlreadyRegisteredError(Exception):
    """A template for given extension is already been registered."""
