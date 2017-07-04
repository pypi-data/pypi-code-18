"""A pickle wrapper module with protocol=-1 by default."""

import json


def loads(s):
    return json.loads(s)


def dumps(obj):
    return json.dumps(obj)
