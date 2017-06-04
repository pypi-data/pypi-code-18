from django import template
from django.contrib.staticfiles import finders
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def include_static(path: str):
    """ Inserts the contents of a static file verbatim into a Django template. """
    actual_path = finders.find(path)
    with open(actual_path, 'r', encoding='UTF-8') as f:
        content = f.read()
        return mark_safe(content)

