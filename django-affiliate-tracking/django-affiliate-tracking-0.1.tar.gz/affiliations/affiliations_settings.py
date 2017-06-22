"""
Default settings for affiliations.

This module will include all the default settings that the affiliations
application will use.
"""
from django.conf import settings


AFFILIATE_QUERY_STRING_KEY = getattr(
    settings,
    'AFFILIATE_QUERY_STRING_KEY',
    'affiliate_id'
)

AFFILIATE_SESSION_KEY = getattr(
    settings,
    'AFFILIATE_SESSION_KEY',
    'affiliate_visitor_id'
)
