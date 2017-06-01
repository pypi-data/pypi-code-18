import sys
try:
    from urllib import quote_plus
    from urllib import urlencode as urllib_encode
except ImportError:
    from urllib.parse import urlencode as urllib_encode
    from urllib.parse import quote_plus


def url_with_query(base, params):
    """
    Takes in a base url and a group of parameters/query, and returns a
    formatted url. Will be consistent between python 2 and 3.
    """
    return base + "?%s" % urlencode(params)


def urlencode(query, doseq=True, safe='', encoding=None, errors=None,
              quote_via=quote_plus):
    """
    This is a utility method used to ensure that the query params are sorted
    consistently between python2 and python3 by urlencode.
    """
    if type(query) is dict:
        query = [(key, query[key]) for key in sorted(query.keys())]
    elif type(query) is list:
        query = sorted(query, key=lambda tup: tup[0])

    if (sys.version_info > (3, 5)):
        return urllib_encode(query, doseq, safe, encoding, errors, quote_via)
    elif (sys.version_info == (3, 4)):
        return urllib_encode(query, doseq, safe, encoding, errors)
    else:
        return urllib_encode(query, doseq)
