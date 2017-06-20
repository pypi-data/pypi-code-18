"""
requests_tracker.filtering.columns
==================================
"""

IDENTITY = 0
METHOD = 10
SCHEME = 100
NETLOC = 101
PATH = 102
QUERY = 103
FRAGMENT = 104

ALL_COLUMNS = [IDENTITY, METHOD,
               SCHEME, NETLOC, PATH, QUERY, FRAGMENT]

COLUMN_CHOICES = (
    (IDENTITY, 'identity'),
    (METHOD, 'method'),
    (SCHEME, 'url:scheme'),
    (NETLOC, 'url:netloc'),
    (PATH, 'url:path'),
    (QUERY, 'url:query'),
    (FRAGMENT, 'url:fragment'),
)


def get_column_name(column):
    return dict(COLUMN_CHOICES)[column]
