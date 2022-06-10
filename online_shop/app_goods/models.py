from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex


class Goods(models.Model):
    """Товары"""
    goodsname = models.CharField(max_length=100, verbose_name=_('goods name'))
    description = models.TextField(verbose_name=_('description'))
    categoryidx = models.ForeignKey('app_categories.Categories', related_name='goods',
                                    on_delete=models.CASCADE, verbose_name=_('category'))
    image = models.ImageField(upload_to='goods/', verbose_name=_('image'))
    search_vector = SearchVectorField(null=True)

    class Meta:
        verbose_name = _('goods')
        verbose_name_plural = _('goods')

        indexes = [
            GinIndex(fields=['search_vector']),
        ]

    def __str__(self):
        return self.goodsname


class Shops(models.Model):
    """Магазины"""
    shopname = models.CharField(max_length=50, verbose_name=_('shop name'))
    address = models.CharField(max_length=100, verbose_name=_('address'))
    phone = models.PositiveIntegerField(verbose_name=_('phone'))
    email = models.EmailField(verbose_name=_('email'))
    description = models.TextField(verbose_name=_('description'))
    image = models.ImageField(upload_to='shops/', verbose_name=_('image'))

    class Meta:
        verbose_name = _('shop')
        verbose_name_plural = _('shops')

    def __str__(self):
        return self.shopname


class GoodsStorages(models.Model):
    """Склады товаров"""
    goodsidx = models.ForeignKey('Goods', on_delete=models.CASCADE, related_name='storage', verbose_name=_('goods'))
    quantity = models.PositiveIntegerField(verbose_name=_('quantity'))
    limited = models.BooleanField(default=False, verbose_name=_('limited edition'))

    class Meta:
        verbose_name = _('goods storage')
        verbose_name_plural = _('goods storages')


class GoodsInShops(models.Model):
    """Товары в магазинах"""
    goodsidx = models.ForeignKey('Goods', on_delete=models.CASCADE, verbose_name=_('goods'))
    shopidx = models.ForeignKey('Shops', on_delete=models.CASCADE, verbose_name=_('shop'))
    price = models.FloatField(verbose_name=_('price'))

    class Meta:
        verbose_name = _('goods in shop')
        verbose_name_plural = _('goods in shops')


class Offer(models.Model):
    """таблица для хранения предложения дня"""
    goodsidx = models.ForeignKey('Goods', on_delete=models.CASCADE, related_name='offer', verbose_name=_('goods'))
    startofferdate = models.DateTimeField(verbose_name=_('date offer start'))

    def __str__(self):
        return self.goodsidx.goodsname
