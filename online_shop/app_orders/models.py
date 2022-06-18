from django.db import models
from django.utils.translation import gettext_lazy as _


# class ShipmentMethod(models.Model): # todo первый вариант доставки - удалить модель
#     """ Способ доставки """
#     normal = models.IntegerField(default=0, verbose_name=_('normal shipping method '))
#     express = models.IntegerField(default=1, verbose_name=_('express shipping method'))
#
#     class Meta:
#         verbose_name = _('shipment method')
#         verbose_name_plural = _('shipment methods')
#
#
# class ShipmentRules(models.Model):
#     """ Правила доставки """
#     freenormal = models.FloatField(default=2000, verbose_name=_('free shipping'))
#     paidnormal = models.FloatField(default=200, verbose_name=_('standard shipping'))
#     paidexpress = models.FloatField(default=500, verbose_name=_('express shipping'))
#
#     class Meta:
#         verbose_name = _('shipment rule')
#         verbose_name_plural = _('shipment rules')


class Shipment(models.Model):
    """ Правила доставки вариант 2 """
    deliverymethod = models.CharField(max_length=100, null=False, verbose_name=_('delivery method'))
    minordervalue = models.DecimalField(default=0, max_digits=8, decimal_places=2,
                                        verbose_name=_('minimum order value'))
    shippingcost = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name=_('shipping cost'))
    addshippingcost = models.DecimalField(default=0, max_digits=8, decimal_places=2,
                                          verbose_name=_('additional shipping cost'))

    class Meta:
        verbose_name = _('shipment rule')
        verbose_name_plural = _('shipment rules')

    def __str__(self):
        return self.deliverymethod


class PaymentMethod(models.Model):
    """ Способ оплаты """
    paymentmethodcode = models.IntegerField(null=False, verbose_name=_('payment method code'))
    paymentmethodtext = models.TextField(null=False, verbose_name=_('payment method'))

    class Meta:
        verbose_name = _('payment rule')
        verbose_name_plural = _('payment methods')

    def __str__(self):
        return self.paymentmethodtext


class Orders(models.Model):
    """ Заказы """
    useridx = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name=_('user'))
    order = models.TextField(null=False, verbose_name=_('order list'))
    dt = models.DateTimeField(auto_now=True, null=False, verbose_name=_('order date'))
    total = models.DecimalField(default=0, max_digits=8, decimal_places=2, verbose_name=_('order total price'))
    paid = models.ForeignKey('PaymentMethod', on_delete=models.CASCADE, verbose_name=_('payment method'))
    shipment = models.ForeignKey('Shipment', on_delete=models.CASCADE, verbose_name=_('shipment method'))
    address = models.CharField(max_length=50, null=False, verbose_name=_('order delivery address'))
    paymentidx = models.OneToOneField('app_payment.Payment', on_delete=models.CASCADE, verbose_name=_('payment id'), null=True)

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):
        return self.order


# class DiscountsRules(models.Model):
#     """Правила скидок"""
#     percentdiscount = models.IntegerField(default=0, verbose_name=_('percent discount'))
#     normaldiscount = models.IntegerField(default=1, verbose_name=_('normal discount'))
#     fixedprice = models.IntegerField(default=2, verbose_name=_('fixed price'))
#
#     class Meta:
#         verbose_name = _('discount rule')
#         verbose_name_plural = _('discounts rules')


# class GoodsDiscounts(models.Model):
#     """Скидочные товары"""
#     goodsidx = models.OneToOneField('app_goods.Goods', on_delete=models.CASCADE,
#                                     related_name='discounts', verbose_name=_('goods'))
#     discountruleidx = models.ForeignKey('DiscountsRules', on_delete=models.CASCADE, verbose_name=_('discount rule'))
#     goodsdiscount = models.FloatField(verbose_name=_('goods discount'))
#
#     class Meta:
#         verbose_name = _('goods discount')
#         verbose_name_plural = _('goods discounts')


# class GoodsDiscountsCalendar(models.Model):
#     """Календарь скидок на товары"""
#     goodsidx = models.ForeignKey('app_goods.Goods', on_delete=models.CASCADE, verbose_name=_('goods'))
#     startdt = models.DateTimeField(verbose_name=_('start date'))
#     enddt = models.DateTimeField(verbose_name=_('end date'))
#     isactive = models.BooleanField(verbose_name=_('is active'))
#
#     class Meta:
#         verbose_name = _('goods discount calendar')
#         verbose_name_plural = _('goods discounts calendar')


# class GoodsSets(models.Model):
#     """Наборы товаров"""
#     goodsidx = models.ForeignKey('app_goods.Goods', on_delete=models.CASCADE,
#                                  related_name='sets', verbose_name=_('goods'))
#     discountruleidx = models.ForeignKey('DiscountsRules', on_delete=models.CASCADE, verbose_name=_('discount rule'))
#     goodsset = models.TextField(verbose_name=_('goods set'))
#     setdiscount = models.FloatField(verbose_name=_('set discount'))
#
#     class Meta:
#         verbose_name = _('goods set')
#         verbose_name_plural = _('goods sets')


# class SetsDiscountsCalendar(models.Model):
#     """Календарь скидок на наборы"""
#     setidx = models.ForeignKey('GoodsSets', on_delete=models.CASCADE, verbose_name=_('goods'))
#     startdt = models.DateTimeField(verbose_name=_('start date'))
#     enddt = models.DateTimeField(verbose_name=_('end date'))
#     isactive = models.BooleanField(verbose_name=_('active'))
#
#     class Meta:
#         verbose_name = _('set discount calendar')
#         verbose_name_plural = _('sets discounts calendar')


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


# модели для системы скидок

DISCOUNT_TYPE = [
    (1, 'Good discount'),
    (2, 'Set discount'),
    (3, 'Discount on the number/total value of items in the cart'),
]


class Discounts(models.Model):
    """ список скидок """
    name = models.CharField(max_length=100, null=False, verbose_name=_('discount name'))
    priority = models.PositiveSmallIntegerField(default=1, verbose_name=_('discount priority'))
    description = models.TextField(default='', verbose_name=_('discount description'))
    active = models.BooleanField(default=False, verbose_name=_('discount is active'))
    type = models.IntegerField(choices=DISCOUNT_TYPE, verbose_name=_('discount type'))
    startdate = models.DateTimeField(verbose_name=_('discount start date'))
    stopdate = models.DateTimeField(verbose_name=_('discount stop date'))
    discountpercentage = models.PositiveSmallIntegerField(default=0, verbose_name=_('discount value in percent'))
    discountamount = models.DecimalField(decimal_places=2, max_digits=10, default=0,
                                         verbose_name=_('fixed amount of discount'))
    fixedcost = models.DecimalField(decimal_places=2, max_digits=10, default=0, verbose_name=_('fixed cost'))
    minimumvalue = models.DecimalField(default=0, max_digits=10, decimal_places=2,
                                       verbose_name=_('minimum value of items in the cart'))
    numberofitems = models.IntegerField(default=0, verbose_name=_('number of items in the cart'))

    class Meta:
        verbose_name = _('discounts list')
        verbose_name_plural = _('discounts list')

    def __str__(self):
        return self.name

    def get_discount_price(self, price):
        """ расчет скидочной стоимости """
        discount_price = 0
        if self.discountpercentage > 0:
            discount_price = round(price * (100 - self.discountpercentage) / 100, 2)
        elif self.discountamount > 0:
            if self.discountamount >= price:
                discount_price = 1
            else:
                discount_price = price - self.discountamount
        elif self.fixedcost > 0:
            discount_price = self.fixedcost
        return discount_price


SET_NUMBER = [
    (1, 'First set'),
    (2, 'Second set'),
]


class GoodsSet(models.Model):
    """ список товаров для скидок """
    discountsidx = models.ForeignKey(Discounts, on_delete=models.CASCADE, verbose_name=_('discounts'))
    setnumber = models.IntegerField(choices=SET_NUMBER, verbose_name=_('set number'))
    goodsidx = models.ForeignKey('app_goods.Goods', on_delete=models.CASCADE,
                                 related_name='set', verbose_name=_('goods'))

    def __str__(self):
        return f'{self.discountsidx.name} Set number: {self.setnumber} Goods: {self.goodsidx.goodsname}'


class CategoriesSet(models.Model):
    """ список категорий для скидок """
    discountsidx = models.ForeignKey(Discounts, on_delete=models.CASCADE, verbose_name=_('discounts'))
    setnumber = models.IntegerField(choices=SET_NUMBER, verbose_name=_('set number'))
    categoriesidx = models.ForeignKey('app_categories.Categories', on_delete=models.CASCADE,
                                 related_name='set', verbose_name=_('categories'))

    def __str__(self):
        return f'{self.discountsidx.name} Set number: {self.setnumber} Category: {self.categoriesidx.categoryname}'
