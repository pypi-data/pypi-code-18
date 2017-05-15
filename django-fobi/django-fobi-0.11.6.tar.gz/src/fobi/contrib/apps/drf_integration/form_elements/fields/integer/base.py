from django.utils.translation import ugettext_lazy as _

from rest_framework.fields import IntegerField

from .......base import IntegrationFormFieldPlugin
from .... import UID as INTEGRATE_WITH_UID
from ....base import (
    DRFIntegrationFormElementPluginProcessor,
    DRFSubmitPluginFormDataMixin,
)
from . import UID

__title__ = 'fobi.contrib.apps.drf_integration.form_elements.fields.' \
            'integer.base'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2014-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('IntegerInputPlugin',)


class IntegerInputPlugin(IntegrationFormFieldPlugin,
                         DRFSubmitPluginFormDataMixin):
    """IntegerField plugin."""

    uid = UID
    integrate_with = INTEGRATE_WITH_UID
    name = _("Integer")
    group = _("Fields")

    def get_custom_field_instances(self,
                                   form_element_plugin,
                                   request=None,
                                   form_entry=None,
                                   form_element_entries=None,
                                   **kwargs):
        """Get form field instances."""
        field_kwargs = {
            'required': form_element_plugin.data.required,
            'label': form_element_plugin.data.label,
            'help_text': form_element_plugin.data.help_text,
        }
        if form_element_plugin.data.initial:
            field_kwargs.update(
                {'initial': int(form_element_plugin.data.initial)}
            )

        return [
            DRFIntegrationFormElementPluginProcessor(
                field_class=IntegerField,
                field_kwargs=field_kwargs
            )
        ]
