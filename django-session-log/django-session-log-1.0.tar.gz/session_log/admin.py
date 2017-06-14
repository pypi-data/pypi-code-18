from __future__ import absolute_import
from django.contrib import admin
from .models import SessionActivity


class SessionActivityAdmin(admin.ModelAdmin):
    readonly_fields = (
        "user", "ip_address", "user_agent", "created_at",
        "time_logout", 'session_key'
    )

    list_display = (
        "user", "ip_address", "user_agent", "created_at",
        "time_logout"
    )

    list_select_related = True

    # list_display_links = None
    search_fields = [
        'user__username',
        "ip_address",
        "user_agent",
        "created_at",
        "time_logout"
    ]

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        """
        Nobody has permission to change any logs, but superuser can view them
        """
        return request.user.is_superuser

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

admin.site.register(SessionActivity, SessionActivityAdmin)
