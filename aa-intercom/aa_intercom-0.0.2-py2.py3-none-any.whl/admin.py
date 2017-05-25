# -*- coding: utf-8 -*-
from aa_intercom.models import IntercomEvent
from django.contrib import admin


class IntercomEventAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "type", "is_sent", "created")
    list_filter = ("id", "user", "type", "is_sent")


admin.site.register(IntercomEvent, IntercomEventAdmin)
