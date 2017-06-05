import json

from django.core.serializers import serialize
from django.db.models.query import QuerySet
from django.template import Library
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.safestring import mark_safe

register = Library()


def jsonify(object):
    """ This template tag transforms a given input to json."""
    if isinstance(object, QuerySet):
        return mark_safe(serialize('json', object, cls=DjangoJSONEncoder))
    return mark_safe(json.dumps(object))
register.filter('jsonify', jsonify)
