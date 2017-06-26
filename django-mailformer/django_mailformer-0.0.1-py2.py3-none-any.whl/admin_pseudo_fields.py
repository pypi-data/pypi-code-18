'''
Pseudo Fields
'''
from django.utils.html import mark_safe

from .tools import get_email_form_url


def recipient_form_url(instance):
    if instance.email != '':
        value = get_email_form_url(instance.email)
    else:
        value = ''
    return value


recipient_form_url.short_description = 'Form URL text'


def recipient_form_link(instance):
    url = recipient_form_url(instance)
    if url == '':
        return url
    a_text = '<a href="{}">form</a>'
    return mark_safe(a_text.format(url))


recipient_form_link.short_description = 'Form URL link'
