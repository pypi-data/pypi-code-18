# coding: utf-8
from django.utils.translation import ugettext_lazy as _


LEVEL_CHOICES_WARNING = 'WARNING'
LEVEL_CHOICES_ERROR = 'ERROR'

LEVEL_CHOICES = (
    (LEVEL_CHOICES_WARNING, _('Warning')),
    (LEVEL_CHOICES_ERROR, _('Error')),
)
