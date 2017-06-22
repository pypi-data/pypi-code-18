from django.contrib import admin
from rxncon_system.models import Rxncon_system


class RxnconSystemAdmin(admin.ModelAdmin):
    list_display = ["__str__", "project_name", "project_id"]
    list_display_links = ["__str__"]
    list_filter = ["updated", "timestamp"]
    search_fields = ["__str__"]

    class Meta:
        model = Rxncon_system


admin.site.register(Rxncon_system, RxnconSystemAdmin)
