from django.db import models
from django.utils.translation import gettext_lazy as _


class Categories(models.Model):
    """Категории"""
    categoryname = models.CharField(max_length=50, verbose_name=_('category name'))
    parent = models.ForeignKey('Categories', on_delete=models.DO_NOTHING, null=True,
                               blank=True, verbose_name=_('parent'))
    categoryimg = models.ImageField(upload_to='img/', null=True, blank=True,
                                    default=None, verbose_name=_('category image'))
    is_active = models.BooleanField(default=False, verbose_name=_('active'))
    goodscharacteristics = models.TextField(default=None, null=True,
                                            blank=True, verbose_name=_('list of characteristics'))

    class Meta:
        verbose_name = _('category')
        verbose_name_plural = _('categories')

    def __str__(self):
        return self.categoryname


class Subcategories(models.Model):
    """Подкатегории"""
    categoryidx = models.ForeignKey('Categories', on_delete=models.CASCADE, verbose_name=_('parent category'))
    subcategoryname = models.CharField(max_length=50, verbose_name=_('subcategory name'))
    goodscharacteristics = models.TextField(verbose_name=_('list of characteristics'))

    class Meta:
        verbose_name = _('subcategory')
        verbose_name_plural = _('subcategories')

    def __str__(self):
        return self.subcategoryname


class CharacteristicTypes(models.Model):
    """Типы характеристик"""
    characteristictype = models.CharField(max_length=25, verbose_name=_('characteristic type'))

    class Meta:
        verbose_name = _('characteristic type')
        verbose_name_plural = _('characteristic types')

    def __str__(self):
        return self.characteristictype


class Characteristics(models.Model):
    """Характеристики"""
    characteristictype = models.ForeignKey('CharacteristicTypes',
                                           on_delete=models.CASCADE, verbose_name=_('characteristic type'))
    goodsidx = models.ForeignKey('app_goods.Goods', on_delete=models.CASCADE, verbose_name=_('goods'))
    value = models.CharField(max_length=5, verbose_name=_('characteristic value'))

    class Meta:
        verbose_name = _('characteristic')
        verbose_name_plural = _('characteristics')
