from django import template
from django.contrib.staticfiles import finders

register = template.Library()


@register.simple_tag
def include_static(path: str):
    """ Inserts the contents of a static file verbatim into a Django template. """
    actual_path = finders.find(path)
    with open(actual_path, 'r', encoding='UTF-8') as f:
        content = f.read()
        return content

