from __future__ import unicode_literals

from wagtail.contrib.modeladmin.options import ModelAdmin, modeladmin_register

from .models import TestModel


class TestModelAdmin(ModelAdmin):
    model = TestModel
    inspect_view_enabled = True

modeladmin_register(TestModelAdmin)
