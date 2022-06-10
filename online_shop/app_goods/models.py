from django.db import models
from django.utils.translation import gettext_lazy as _

from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex

from app_orders.models import Discounts
from app_categories.models import Categories, Subcategories


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

    def discountprice(self):
        """ вычисление стоимости товара со скидкой по 1-му типу - Скидки на товар """
        #  тип скидки - скидка на товар type=1
        good_id = self.goodsidx.id
        subcategories = Subcategories.objects.get(id=self.goodsidx.categoryidx.id)
        categories_id = Categories.objects.get(id=subcategories.categoryidx.id).id
        active_discount_good = Discounts.objects.filter(active=True, type=1, goodsset__goodsidx=good_id).\
            order_by('priority').last()
        active_discount_category = Discounts.objects.filter(active=True, type=1,
                                                            categoriesset__categoriesidx=categories_id).\
            order_by('priority').last()
        # если есть активные скидки на товар, то эта скидка приоритетней чем скидка на категорию
        if active_discount_good:
            active_discount = active_discount_good
        elif active_discount_category:
            active_discount = active_discount_category
        else:
            active_discount = None

        if active_discount:
            if active_discount.discountpercentage > 0:
                return self.price * (100 - active_discount.discountpercentage) / 100
            elif active_discount.discountamount > 0:
                if active_discount.discountamount >= self.price:
                    return 1
                return self.price - active_discount.discountamount
            elif active_discount.fixedcost > 0:
                return active_discount.fixedcost
        return self.price


class Offer(models.Model):
    """таблица для хранения предложения дня"""
    goodsidx = models.ForeignKey('Goods', on_delete=models.CASCADE, related_name='offer', verbose_name=_('goods'))
    startofferdate = models.DateTimeField(verbose_name=_('date offer start'))

    def __str__(self):
        return self.goodsidx.goodsname
