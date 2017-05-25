from django import template

register = template.Library()


@register.simple_tag()
def asana_url(instance, project=None):
    return instance.asana_url(project)
