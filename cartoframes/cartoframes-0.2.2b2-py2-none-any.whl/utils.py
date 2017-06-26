import sys
import re

def dict_items(d):
    """Description

    Args:
        d (dict): dictionary

    Returns:
        list?
    """
    if sys.version_info >= (3,0):
        return d.items()
    else:
        return d.iteritems()

def cssify(css_dict):
    css = ''
    for key, value in dict_items(css_dict):
        css += '{key} {{ '.format(key=key)
        for field, field_value in dict_items(value):
            css += ' {field}: {field_value};'.format(field=field,
                                                     field_value=field_value)
        css += '} '
    return css

def norm_column(colname):
    """Convert a valid pandas DataFrame column name into a CARTO-supported
    PostgreSQL name"""
    normed = re.sub('[^a-z_0-9]', '_', colname.lower())
    if re.match('^[0-9]', normed):
        return '_' + normed
    return normed
