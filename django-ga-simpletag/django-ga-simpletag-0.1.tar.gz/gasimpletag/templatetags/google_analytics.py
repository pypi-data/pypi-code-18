from django import template
from django.conf import settings


register = template.Library()


@register.simple_tag
def ga_js(idtrack):
    if not settings.DEBUG:
        c = {
            'idtrack': idtrack
        }
        js = template.loader.get_template("ga.js")
        return js.render(c)
    else:
        return ""
