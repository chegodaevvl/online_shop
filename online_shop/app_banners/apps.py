from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppBannersConfig(AppConfig):
    name = 'app_banners'
    verbose_name = _('banners')
