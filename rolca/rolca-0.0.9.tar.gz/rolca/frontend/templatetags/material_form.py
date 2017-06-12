""".. Ignore pydocstyle D400.

=====================
Frontend templatetags
=====================

.. autofunction:: rolca.frontend.templatetags.material_form.render

"""
import os

from django import template
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe

from rolca.frontend import settings as rolca_settings

register = template.Library()  # pylint: disable=invalid-name


@register.filter
def render(bound_field):
    """Render form field in material design."""
    input_type = bound_field.field.widget.input_type

    if input_type in ['text', 'password', 'email']:
        template_name = 'text_field.html'
    elif input_type == 'file':
        template_name = 'file_field.html'
    else:
        return bound_field

    context = {
        'bound_field': bound_field,
        'field': bound_field.field,
        'color': rolca_settings.frontend_color,
    }

    template_path = os.path.join('frontend', 'fields', template_name)
    rendered = render_to_string(template_path, context)

    return mark_safe(rendered)
