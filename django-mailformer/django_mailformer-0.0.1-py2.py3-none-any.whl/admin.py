from django.contrib import admin

from .admin_pseudo_fields import recipient_form_link, recipient_form_url
from .models import Message, Recipient, Sender


class RecipientAdmin(admin.ModelAdmin):
    readonly_fields = (recipient_form_url, recipient_form_link, 'identifier',)


class MessageAdmin(admin.ModelAdmin):
    readonly_fields = ('returned', 'processor', 'process_after', 'created_at', 'updated_at',)


admin.site.register(Recipient, RecipientAdmin)
admin.site.register(Message, MessageAdmin)
admin.site.register(Sender)
