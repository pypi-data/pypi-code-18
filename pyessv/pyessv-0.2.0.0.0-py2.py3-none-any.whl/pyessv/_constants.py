# -*- coding: utf-8 -*-

"""
.. module:: pyessv._constants.py
   :copyright: Copyright "December 01, 2016", IPSL
   :license: GPL/CeCIL
   :platform: Unix, Windows
   :synopsis: Package constants.

.. moduleauthor:: Mark Conway-Greenslade <momipsl@ipsl.jussieu.fr>


"""
import os
import re



# Directory containing vocabulary archive.
DIR_ARCHIVE = os.path.expanduser('~/.esdoc/pyessv-archive')

# Dictionary encoding.
ENCODING_DICT = 'dict'

# JSON encoding.
ENCODING_JSON = 'json'

# Set of supported encodings.
ENCODING_SET = {
    ENCODING_DICT,
    ENCODING_JSON
}

# Entity type - an authority governing vocabularies.
ENTITY_TYPE_AUTHORITY = 'authority'

# Entity type - a scope constraining collection of vocabularies.
ENTITY_TYPE_SCOPE = 'scope'

# Entity type - a collection constraining collection of term.
ENTITY_TYPE_COLLECTION = 'collection'

# Entity type - a term.
ENTITY_TYPE_TERM = 'term'

# Set of allowed name types.
ENTITY_TYPE_SET = (
  ENTITY_TYPE_AUTHORITY,
  ENTITY_TYPE_COLLECTION,
  ENTITY_TYPE_SCOPE,
  ENTITY_TYPE_TERM
  )

# Governance state - the term is accepted.
GOVERNANCE_STATUS_ACCEPTED = 'accepted'

# Governance state - the term is obsolete.
GOVERNANCE_STATUS_DEPRECATED = 'obsolete'

# Governance state - the term is pending review.
GOVERNANCE_STATUS_PENDING = 'pending'

# Governance state - the term is rejected.
GOVERNANCE_STATUS_REJECTED = 'rejected'

# Set of allowed governance states.
GOVERNANCE_STATUS_SET = (
    GOVERNANCE_STATUS_PENDING,
    GOVERNANCE_STATUS_ACCEPTED,
    GOVERNANCE_STATUS_REJECTED,
    GOVERNANCE_STATUS_DEPRECATED
)

# Regular expression for validating a canonical name.
REGEX_CANONICAL_NAME = r'^[A-z0-9\_\-\ \.]*$'
