from django.contrib import admin
from django.utils.translation import ugettext_lazy as _

from .models import Rating


@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'votes', 'average',
        'update_time', 'content_type', 'target'
    )
    list_display_links = ('id',)
    list_per_page = 20
    filter_horizontal = ('user',)
    date_hierarchy = 'created_at'
    readonly_fields = ('content_type', 'object_id')

    def target(self, obj):
        if obj.content_object:
            return '<a href="{0}">{1}</a>'.format(
                obj.content_object.get_absolute_url(),
                obj.content_object.title
            )
    target.short_description = _('Target object')
    target.allow_tags = True

    def update_time(self, obj):
        return obj.created_at.strftime("%d.%m.%Y")
    update_time.short_description = _('Updated at')
