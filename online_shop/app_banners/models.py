from django.db import models
from django.utils.translation import gettext_lazy as _


class Banners(models.Model):
    """Баннеры"""
    advertisementname = models.CharField(max_length=50, verbose_name=_('advertiser'))
    bannerimg = models.ImageField(upload_to='img/', null=True, default=None, verbose_name=_('banner image'))
    isactive = models.BooleanField(default=False, verbose_name=_('active'))
    bannerlink = models.TextField(verbose_name=_('banner link'))

    class Meta:
        verbose_name = _('banner')
        verbose_name_plural = _('banners')
