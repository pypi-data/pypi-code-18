"""Admin configuration for the application affiliations."""

from django.contrib import admin

from .models import (
    Partner,
    Subscription,
    Visitor,
)

admin.site.register(Partner)
admin.site.register(Subscription)
admin.site.register(Visitor)
