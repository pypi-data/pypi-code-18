# -*- coding: utf-8 -*-
"""
.. module:: pyessv.__init__.py

   :copyright: @2015 IPSL (http://ipsl.fr)
   :license: GPL / CeCILL
   :platform: Unix
   :synopsis: Python Earth Science Standard Vocabulary library intializer.

.. moduleauthor:: IPSL (ES-DOC) <dev@esdocumentation.org>

"""
__title__ = 'pyessv'
__version__ = '0.2.0.0.0'
__author__ = 'ES-DOC'
__license__ = 'GPL'
__copyright__ = 'Copyright 2016 ES-DOC'



from pyessv._archive import add
from pyessv._archive import load
from pyessv._archive import save

from pyessv._codecs import decode
from pyessv._codecs import encode

from pyessv._constants import DIR_ARCHIVE
from pyessv._constants import ENCODING_DICT
from pyessv._constants import ENCODING_JSON
from pyessv._constants import ENTITY_TYPE_AUTHORITY
from pyessv._constants import ENTITY_TYPE_COLLECTION
from pyessv._constants import ENTITY_TYPE_SCOPE
from pyessv._constants import ENTITY_TYPE_TERM
from pyessv._constants import GOVERNANCE_STATUS_ACCEPTED
from pyessv._constants import GOVERNANCE_STATUS_DEPRECATED
from pyessv._constants import GOVERNANCE_STATUS_PENDING
from pyessv._constants import GOVERNANCE_STATUS_REJECTED

from pyessv._exceptions import InvalidAssociationError
from pyessv._exceptions import TemplateParsingError
from pyessv._exceptions import ParsingError
from pyessv._exceptions import ValidationError

from pyessv._factory import create_authority
from pyessv._factory import create_collection
from pyessv._factory import create_template_parser
from pyessv._factory import create_scope
from pyessv._factory import create_term

from pyessv._initializer import init

from pyessv._model import Authority
from pyessv._model import Collection
from pyessv._model import Scope
from pyessv._model import Term

from pyessv._parser import parse
from pyessv._parser import parse_namespace

from pyessv._validation import get_errors
from pyessv._validation import is_valid
from pyessv._validation import validate_entity as validate


# Auto-initialize.
init()
