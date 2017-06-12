from django.contrib import admin

from aa_intercom.models import IntercomEvent


class IntercomEventAdmin(admin.ModelAdmin):
    readonly_fields = ("id", "user", "type", "text_content", "created", "modified", "content_type", "object_id",
                       "content_object", "is_sent")

    list_display = ("id", "user", "type", "is_sent", "created")
    list_filter = ("id", "user", "type", "is_sent")

    def has_add_permission(self, request):
        return False


admin.site.register(IntercomEvent, IntercomEventAdmin)
