from django.contrib import admin

from cache.models import Invalidation


class InvalidationAdmin(admin.ModelAdmin):
    list_display = ('key', 'object_id', 'count', 'created_at')
    search_fields = ('key',)


admin.site.register(Invalidation, InvalidationAdmin)
