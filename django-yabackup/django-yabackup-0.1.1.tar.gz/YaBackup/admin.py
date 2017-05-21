from django.contrib import admin
from YaBackup.models import Backup, Path
from YaBackup.backup import YaBackup
from django.utils.translation import ugettext_lazy as _


def run_backups_admin(self, request, queryset):
    backup = YaBackup()
    backup.run_backups(queryset, manual=True)
    self.message_user(request, _('Successfully made %s backups!' % queryset.count()))
run_backups_admin.short_description = _('Run backups')


class PathInline(admin.TabularInline):
    model = Path
    extra = 0


@admin.register(Backup)
class BackupAdmin(admin.ModelAdmin):

    list_display = ('title', 'output_directory', 'file_name', 'upload', 'delete_after_upload', 'mysqldump', 'pub_date', )

    fieldsets = (
        (None, {
            'fields': ('title', ('output_directory', 'file_name'), ('upload', 'delete_after_upload'), 'mysqldump')
        }),
        (_('Notes'), {
            'classes': ('collapse',),
            'fields': ('description',),
        }),
    )
    inlines = [
        PathInline,
    ]
    empty_value_display = _('Untitled backup')
    list_filter = ('upload', 'delete_after_upload', 'mysqldump', 'pub_date')
    search_fields = ['title', 'file_name']
    actions = [run_backups_admin]
