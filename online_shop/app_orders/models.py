from django.db import models
from django.utils.translation import gettext_lazy as _


class ShipmentMethod(models.Model):
    """ Способ доставки """
    normal = models.IntegerField(default=0, verbose_name=_('normal shipping method '))
    express = models.IntegerField(default=1, verbose_name=_('express shipping method'))

    class Meta:
        verbose_name = _('shipment method')
        verbose_name_plural = _('shipment methods')


class ShipmentRules(models.Model):
    """ Правила доставки """
    freenormal = models.FloatField(default=2000, verbose_name=_('free shipping'))
    paidnormal = models.FloatField(default=200, verbose_name=_('standard shipping'))
    paidexpress = models.FloatField(default=500, verbose_name=_('express shipping'))

    class Meta:
        verbose_name = _('shipment rule')
        verbose_name_plural = _('shipment rules')


class PaymentMethod(models.Model):
    """ Способ оплаты """
    card = models.IntegerField(default=0, verbose_name=_('card number'))
    foreignaccount = models.IntegerField(default=1, verbose_name=_('foreign account'))

    class Meta:
        verbose_name = _('payment rule')
        verbose_name_plural = _('payment methods')


class Orders(models.Model):
    """ Заказы """
    useridx = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name=_('user'))
    order = models.TextField(null=False, verbose_name=_('order list'))
    dt = models.DateTimeField(auto_now=True, null=False, verbose_name=_('order date'))
    total = models.DecimalField(max_digits=8, decimal_places=2, verbose_name=_('order total price'))
    paid = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE, verbose_name=_('payment method'))
    shipment = models.ForeignKey('ShipmentMethod', on_delete=models.CASCADE, verbose_name=_('shipment method'))
    address = models.CharField(max_length=50, null=False, verbose_name=_('order delivery address'))

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):
        return self.order


class DiscountsRules(models.Model):
    """Правила скидок"""
    percentdiscount = models.IntegerField(default=0, verbose_name=_('percent discount'))
    normaldiscount = models.IntegerField(default=1, verbose_name=_('normal discount'))
    fixedprice = models.IntegerField(default=2, verbose_name=_('fixed price'))

    class Meta:
        verbose_name = _('discount rule')
        verbose_name_plural = _('discounts rules')


class GoodsDiscounts(models.Model):
    """Скидочные товары"""
    goodsidx = models.OneToOneField('app_goods.Goods', on_delete=models.CASCADE,
                                    related_name='discounts', verbose_name=_('goods'))
    discountruleidx = models.ForeignKey('DiscountsRules', on_delete=models.CASCADE, verbose_name=_('discount rule'))
    goodsdiscount = models.FloatField(verbose_name=_('goods discount'))

    class Meta:
        verbose_name = _('goods discount')
        verbose_name_plural = _('goods discounts')


class GoodsDiscountsCalendar(models.Model):
    """Календарь скидок на товары"""
    goodsidx = models.ForeignKey('app_goods.Goods', on_delete=models.CASCADE, verbose_name=_('goods'))
    startdt = models.DateTimeField(verbose_name=_('start date'))
    enddt = models.DateTimeField(verbose_name=_('end date'))
    isactive = models.BooleanField(verbose_name=_('is active'))

    class Meta:
        verbose_name = _('goods discount calendar')
        verbose_name_plural = _('goods discounts calendar')


class GoodsSets(models.Model):
    """Наборы товаров"""
    goodsidx = models.ForeignKey('app_goods.Goods', on_delete=models.CASCADE,
                                 related_name='sets', verbose_name=_('goods'))
    discountruleidx = models.ForeignKey('DiscountsRules', on_delete=models.CASCADE, verbose_name=_('discount rule'))
    goodsset = models.TextField(verbose_name=_('goods set'))
    setdiscount = models.FloatField(verbose_name=_('set discount'))

    class Meta:
        verbose_name = _('goods set')
        verbose_name_plural = _('goods sets')


class SetsDiscountsCalendar(models.Model):
    """Календарь скидок на наборы"""
    setidx = models.ForeignKey('GoodsSets', on_delete=models.CASCADE, verbose_name=_('goods'))
    startdt = models.DateTimeField(verbose_name=_('start date'))
    enddt = models.DateTimeField(verbose_name=_('end date'))
    isactive = models.BooleanField(verbose_name=_('active'))

    class Meta:
        verbose_name = _('set discount calendar')
        verbose_name_plural = _('sets discounts calendar')


class OrderItem(models.Model):
    """Состав товаров в заказах"""
    orderidx = models.ForeignKey(Orders, on_delete=models.CASCADE, verbose_name=_('order'))
    good = models.ForeignKey('app_goods.Goods', on_delete=models.CASCADE,
                                    related_name='orderitem', verbose_name=_('orderitem'))
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = _('order item')
        verbose_name_plural = _('order items')

    def __str__(self):
        return f'Item for order {self.orderidx}'

    def get_cost(self):
        return self.price * self.quantity
