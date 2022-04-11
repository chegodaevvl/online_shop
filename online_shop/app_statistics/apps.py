from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class AppStatisticsConfig(AppConfig):
    name = 'app_statistics'
    verbose_name = _('statistics')
