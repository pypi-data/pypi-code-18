from django.contrib import admin

from polymorphic import admin as polymorphic_admin
from sorl.thumbnail.admin import AdminImageMixin

from . import models


@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user', 'amount', 'currency', 'payment_method', 'status',
        'status_changed', 'created')

    list_filter = (
        'user', 'content_type', 'status', 'status_changed', 'created')


@admin.register(models.Item)
class ItemAdmin(AdminImageMixin,
                polymorphic_admin.PolymorphicParentModelAdmin):

    base_model = models.Item
    list_display = ('name', 'sku', 'price', 'tax_rate', 'created')
    list_filter = ('created',)
