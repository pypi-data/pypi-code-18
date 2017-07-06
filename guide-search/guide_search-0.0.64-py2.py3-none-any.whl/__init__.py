'''
    guide-api
    -----------
    This module provides the interface to elasticsearch
    :copyright: (c) 2017 John Pickerill.
    :license: MIT/X11, see LICENSE for more details.
'''

# -*- coding: utf-8 -*-

from guide_search.esearch import Esearch
from guide_search.dsl import Dsl
from .__about__ import __version__, __title__
__service_name__ = __title__

from guide_search.exceptions import (    # noqa: F401
    BadRequestError,            # 400
    ResourceNotFoundError,      # 404
    ConflictError,              # 409
    PreconditionError,          # 412
    ServerError,                # 500
    ServiceUnreachableError,    # 503
    UnknownError,               # unexpected htstp response
    ResultParseError,           # es result not in expected form
    CommitError,
    JSONDecodeError,
    ValidationError)

__all__ = ['Esearch', 'Dsl',  'ResourceNotFoundError', '__version__']
