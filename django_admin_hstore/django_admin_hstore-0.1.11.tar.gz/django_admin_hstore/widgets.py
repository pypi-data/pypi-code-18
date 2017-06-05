from __future__ import absolute_import, unicode_literals

import json

import django
from django import forms
from django.conf import settings
from django.contrib.admin.templatetags.admin_static import static
from django.contrib.admin.widgets import AdminTextareaWidget
from django.template import Context
from django.template.loader import get_template
from django.utils.safestring import mark_safe

from collections import OrderedDict

__all__ = [
    'AdminHStoreWidget'
]


class AdminHStoreWidget(AdminTextareaWidget):
    """ Base admin widget class for default-admin and grappelli-admin widgets

        The schema shows the user how we represent the Hstore field. an example of a schema is:

        ::
            schema = {
                'field': {
                    'verbose_name': 'Field Name',
                    'type': 'IntegerField'
                },
                'field2': {
                    'verbose_name': 'Some name',
                    'type': 'CharField',
                };
            }

        The possible values that can be mapped are `IntegerField`, `CharField`, `BooleanField`. Note that in any cases
        the values are stored as chars/nulls because these are the only types supported by postgres hstore extension

        note:: This widget was a test to see if it would be more practical to set dynamic columns in a hstore field
            instead of creating a separate table for these dynamic columns. We conclude that design wise it may have
            been better to skip Hstore and use an intermediate table for these dynamic fields.
    """

    admin_style = 'default'
    schema = OrderedDict()

    def __init__(self, schema=None, *args, **kwargs):
        if schema is not None:
            self.schema = schema
        super(AdminHStoreWidget, self).__init__(*args, **kwargs)

    def render(self, name, value, attrs=None, schema=None):
        # Since the Hstore stores all its internal data as strings we need to transform the boolean back to boolean.
        # we decided that for this widget it was not necessary to transform the int and floats back from strings.
        value = json.loads(value)
        for key, item in value.items():
            if item == "True":
                value[key] = True
            elif item == "False":
                value[key] = False

        # prepare template context
        template_context = {
            'field_name': name,
            'schema': json.dumps(self.schema),
            'value': json.dumps(value),
        }

        # generate the html widget
        template = get_template('django_admin_hstore/hstore_widget.html')
        html = template.render(template_context)
        html = mark_safe(html)

        return html
