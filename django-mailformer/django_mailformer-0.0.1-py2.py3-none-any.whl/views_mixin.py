"""
Mixins used for views
"""

from django.core.exceptions import ImproperlyConfigured
from django.template import Template
from django.template.base import TemplateDoesNotExist
from django.template.response import TemplateResponse

from .constants import TEMPLATES


def class_factory_response(url_name_key, template_text):
    warning_text = "TEMPLATE '%s' NOT FOUND, USING FALLBACK !!!</br></br>"

    class ResponseClass(TemplateResponse):

        def resolve_template(self, template):
            if template:
                return super().resolve_template(template)
            else:
                name = TEMPLATES[url_name_key]
                try:
                    return super().resolve_template(name)
                except TemplateDoesNotExist:
                    text = warning_text % name + template_text
                    return Template("<html><body>{}</body></html>".format(text))

    return ResponseClass


class ResponseClassFallbackMixin(object):
    template_fallback = ""
    template_url_key_name = ""

    def render_to_response(self, context, **response_kwargs):
        self.response_class = class_factory_response(
            self.template_url_key_name, self.template_fallback
        )
        return super().render_to_response(context, **response_kwargs)

    def get_template_names(self):
        try:
            returns = super().get_template_names()
        except ImproperlyConfigured:
            returns = None

        return returns
