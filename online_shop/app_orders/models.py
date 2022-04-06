from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _


class ShipmentMethod(models.Model):
    """ Способ доставки """
    normal = models.IntegerField(verbose_name=_('normal shipping method '))
    express = models.IntegerField(verbose_name=_('express shipping method'))

    class Meta:
        verbose_name = _('shipment method')
        verbose_name_plural = _('shipment methods')


class ShipmentRules(models.Model):
    """ Правила доставки """
    freenormal = models.FloatField(verbose_name=_('free shipping '))
    paidnormal = models.FloatField(verbose_name=_('standard shipping '))
    paidexpress = models.FloatField(verbose_name=_('express shipping '))

    class Meta:
        verbose_name = _('shipment rule')
        verbose_name_plural = _('shipment rules')


class PaymentMethod(models.Model):
    """ Способ оплаты """
    card = models.IntegerField(verbose_name=_('card number'))
    foreignaccount = models.IntegerField(verbose_name=_('foreign account'))

    class Meta:
        verbose_name = _('payment rule')
        verbose_name_plural = _('payment methods')


class Orders(models.Model):
    """ Заказы """
    useridx = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name=_('user'))
    order = models.TextField(null=False, verbose_name=_('order list'))
    orderdate = models.DateTimeField(auto_now=True, null=False, verbose_name=_('order date'))
    total = models.DecimalField(decimal_places=2, verbose_name=_('order total price'))
    paid = models.ForeignKey(PaymentMethod, on_delete=models.SET_NULL, verbose_name=_('payment method'))
    shipment = models.ForeignKey(ShipmentMethod, on_delete=models.SET_NULL, verbose_name=_('shipment method'))
    address = models.CharField(max_length=50, null=False, verbose_name=_('order delivery address'))

    class Meta:
        verbose_name = _('order')
        verbose_name_plural = _('orders')

    def __str__(self):
        return self.order


class DiscountType(models.Model):
    """ Типы скидок """
    title = models.CharField(max_length=50, verbose_name=_('discount type'))

    class Meta:
        verbose_name = _('discount type')
        verbose_name_plural = _('discount types')

    def __str__(self):
        return self.title


class DiscountRule(models.Model):
    """ Правила применения скидки """
    title = models.CharField(max_length=50, verbose_name=_('discount rule name'))
    discountvalue = models.FloatField(null=False, verbose_name=_('discount value'))
    goodsset = models.TextField(null=False, verbose_name=_('goods list for discount'))

    class Meta:
        verbose_name = _('discount rule')
        verbose_name_plural = _('discount_rules')

    def __str__(self):
        return self.title


class Discount(models.Model):
    """ Скидки """
    discounttypeidx = models.ForeignKey(DiscountType, on_delete=models.CASCADE)
    discountruleidx = models.ForeignKey(DiscountRule, on_delete=models.CASCADE)
    description = models.TextField(null=False, verbose_name=_('discount description'))
    startdate = models.DateField(null=False, verbose_name=_('discount start date'))
    enddate = models.DateField(null=False, verbose_name=_('discount end date'))
    isactive = models.BooleanField(default=False, verbose_name=_('discount activity'))
    priority = models.IntegerField(default=0, null=False, verbose_name=_('discount priority'))

    class Meta:
        verbose_name = _('discount')
        verbose_name_plural = _('discounts')

    def __str__(self):
        return self.description
