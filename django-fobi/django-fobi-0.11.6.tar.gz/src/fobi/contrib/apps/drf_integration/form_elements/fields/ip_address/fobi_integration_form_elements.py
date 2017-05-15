from .......base import integration_form_element_plugin_registry
from .base import IPAddressInputPlugin

__title__ = 'fobi.contrib.apps.drf_integration.form_elements.fields.' \
            'ip_address.fobi_integration_form_elements'
__author__ = 'Artur Barseghyan <artur.barseghyan@gmail.com>'
__copyright__ = '2014-2017 Artur Barseghyan'
__license__ = 'GPL 2.0/LGPL 2.1'
__all__ = ('IPAddressInputPlugin',)


integration_form_element_plugin_registry.register(IPAddressInputPlugin)
