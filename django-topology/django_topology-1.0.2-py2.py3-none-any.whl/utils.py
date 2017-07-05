# coding: utf-8
from django.conf import settings


def build_contains_filter(geometry, geom_field):

    return {
        '%s__contains' % geom_field: geometry
    }


def build_iintersects_filter(geometry, geom_field):
    return {
        '%s__relate' % geom_field: (geometry, 'T********')
    }


def validation_error_class(django=False):
    """gets the validationError class"""

    if 'djangorestframework' in settings.INSTALLED_APPS and not django:
        from djangorestframework.serializers import ValidationError
    else:
        from django.core.exceptions import ValidationError

    return ValidationError
