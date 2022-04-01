from django.db import models


class Banners(models.Model):
    advertisementname = models.CharField(max_length=50, verbose_name='Рекламодатель')
    bannerimg = models.ImageField(upload_to='img/', null=True, default=None, verbose_name='Рисунок баннера')
    isactive = models.BooleanField(default=False, verbose_name='Активный')
    bannerlink = models.TextField(verbose_name='Ссылка баннера')

    class Meta:
        verbose_name = 'Баннер'
        verbose_name_plural = "Баннеры"
