__title__ = 'fobi.contrib.plugins.form_elements.fields.input.constants'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2014-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = (
    'FORM_FIELD_TYPE_CHOICES', 'FIELD_TYPE_TO_DJANGO_FORM_FIELD_MAPPING',
    'FIELD_TYPE_TO_DJANGO_FORM_WIDGET_MAPPING',
)

FORM_FIELD_TYPE_CHOICES = (
    # ('button', 'button'),
    ('checkbox', 'checkbox'),
    ('color', 'color'),
    ('date', 'date'),
    ('datetime', 'datetime'),
    ('datetime-local', 'datetime-local'),
    ('email', 'email'),
    ('file', 'file'),
    ('hidden', 'hidden'),
    ('image', 'image'),
    ('month', 'month'),
    ('number', 'number'),
    ('password', 'password'),
    ('radio', 'radio'),
    ('range', 'range'),
    ('reset', 'reset'),
    ('search', 'search'),
    # ('submit', 'submit'),
    ('tel', 'tel'),
    ('text', 'text'),
    ('time', 'time'),
    ('url', 'url'),
    ('week', 'week'),
)

FIELD_TYPE_TO_DJANGO_FORM_FIELD_MAPPING = {
    'button': '',
    'checkbox': '',
    'color': '',
    'date': '',
    'datetime': '',
    'datetime-local': '',
    'email': '',
    'file': '',
    'hidden': '',
    'image': '',
    'month': '',
    'number': '',
    'password': '',
    'radio': '',
    'range': '',
    'reset': '',
    'search': '',
    'submit': '',
    'tel': '',
    'text': '',
    'time': '',
    'url': '',
    'week': '',
}

FIELD_TYPE_TO_DJANGO_FORM_WIDGET_MAPPING = {
    'button': '',
    'checkbox': '',
    'color': '',
    'date': '',
    'datetime': '',
    'datetime-local': '',
    'email': '',
    'file': '',
    'hidden': '',
    'image': '',
    'month': '',
    'number': '',
    'password': '',
    'radio': '',
    'range': '',
    'reset': '',
    'search': '',
    'submit': '',
    'tel': '',
    'text': '',
    'time': '',
    'url': '',
    'week': '',
}
