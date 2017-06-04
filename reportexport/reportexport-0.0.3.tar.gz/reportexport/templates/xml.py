# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
import dicttoxml

from .base import Template


@Template.register
class XMLTemplate(Template):
    """XML generator template."""

    extension = 'xml'
    _MANDATORY_FIELDS = {'organization', 'reported_at', 'created_at', 'inventory'}

    @classmethod
    def render(cls, report):
        for mandatory_field in cls._MANDATORY_FIELDS:
            if mandatory_field not in report.type_dict:
                raise KeyError('Mandatory field missing.')

        return dicttoxml.dicttoxml(report.type_dict)
