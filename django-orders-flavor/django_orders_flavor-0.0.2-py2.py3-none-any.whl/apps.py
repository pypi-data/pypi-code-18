from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class OrdersAppConfig(AppConfig):
    name = 'orders_flavor'
    verbose_name = _('Orders')
