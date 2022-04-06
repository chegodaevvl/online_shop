from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppOrdersConfig(AppConfig):
    name = 'app_orders'
    verbose_name = _('orders')
