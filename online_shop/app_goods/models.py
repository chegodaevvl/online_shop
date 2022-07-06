from django.db import models
from django.utils.translation import gettext_lazy as _
from django.db.models import Avg

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

    def discount(self):
        active_discount_good = Discounts.objects.filter(active=True, type=1, goodsset__goodsidx=self.id).\
            order_by('priority').last()
        if not active_discount_good:
            return None
        return int(active_discount_good.discountpercentage)

    def price(self):
        return float(GoodsInShops.objects.filter(goodsidx=self.id).aggregate(Avg('price'))['price__avg'])

    def discount_price(self):
        return float(self.price() * (1 - self.discount() / 100))

    def available_quantity(self):
        return GoodsStorages.objects.get(goodsidx=self.id).values('quantity')


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
    price = models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name=_('price'))

    class Meta:
        verbose_name = _('goods in shop')
        verbose_name_plural = _('goods in shops')

    def get_discount_type1(self):
        """ проверка на выполнения условия скидки по 1-му типу - Скидка на товар """
        good_id = self.goodsidx.id
        subcategories = Categories.objects.get()
        categories_id = Categories.objects.get().id
        active_discount_good = Discounts.objects.filter(active=True, type=1, goodsset__goodsidx=good_id).\
            order_by('priority').last()
        active_discount_category = Discounts.objects.filter(active=True, type=1,
                                                            categoriesset__categoriesidx=categories_id).\
            order_by('priority').last()
        # если есть активные скидки на товар, то эта скидка приоритетней чем скидка на категорию товара
        if active_discount_good:
            active_discount = active_discount_good
        elif active_discount_category:
            active_discount = active_discount_category
        else:
            active_discount = None

        return active_discount

    def get_price_for_discount_type1(self):
        discount_type1 = self.get_discount_type1()
        if discount_type1:
            return Discounts.objects.get().get_discount_price(
                GoodsInShops.objects.get().price
            )
        return None


class Offer(models.Model):
    """таблица для хранения предложения дня"""
    goodsidx = models.ForeignKey('Goods', on_delete=models.CASCADE, related_name='offer', verbose_name=_('goods'))
    startofferdate = models.DateTimeField(verbose_name=_('date offer start'))

    def __str__(self):
        return self.goodsidx.goodsname
