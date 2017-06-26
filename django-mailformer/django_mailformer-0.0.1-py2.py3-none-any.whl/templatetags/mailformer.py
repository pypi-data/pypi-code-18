from django import template

from ..tools import get_email_form_url

register = template.Library()


@register.simple_tag()
def get_url_by_email(email_address, **kwargs):
    return get_email_form_url(email_address, **kwargs)
