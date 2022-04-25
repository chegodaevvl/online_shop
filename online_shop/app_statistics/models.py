from django.db import models
from django.utils.translation import gettext_lazy as _


class Statistics(models.Model):
    """Статистика"""
    goodsidx = models.ForeignKey('app_goods.Goods', on_delete=models.CASCADE,
                                 related_name='statistics', verbose_name=_('goods'))
    quantity = models.IntegerField(verbose_name=_('quantity'))
    dt = models.ForeignKey('app_orders.Orders', on_delete=models.CASCADE, verbose_name=_('date of sale'))

    class Meta:
        verbose_name = _('statistic')
        verbose_name_plural = _('statistics')
