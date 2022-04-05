from django.db import models
from django.contrib.auth.models import User


class Shipmentmethod(models.Model):
    """ Способ доставки """
    normal = models.IntegerField(verbose_name='Normal shipping method ')
    express = models.IntegerField(verbose_name='Express shipping method')


class Shipmentrules(models.Model):
    """ Правила доставки """
    freenormal = models.FloatField(verbose_name='Free shipping ')
    paidnormal = models.FloatField(verbose_name='Standard shipping ')
    paidexpress = models.FloatField(verbose_name='Express shipping ')


class Paymentmethod(models.Model):
    """ Способ оплаты """
    card = models.IntegerField(verbose_name='Card number')
    foreignaccount = models.IntegerField(verbose_name='Foreign account')


class Orders(models.Model):
    """ Заказы """
    useridx = models.ForeignKey(User, on_delete=models.CASCADE)
    order = models.TextField(verbose_name='Order list', null=False)
    orderdate = models.DateTimeField(auto_now=True, verbose_name='Order date', null=False)
    total = models.DecimalField(verbose_name='Order total price', decimal_places=2)
    paid = models.ForeignKey(Paymentmethod, on_delete=models.SET_NULL, verbose_name='Payment method')
    shipment = models.ForeignKey(Shipmentmethod, on_delete=models.SET_NULL, verbose_name='Shipment method')
    address = models.CharField(verbose_name='Order delivery address', max_length=50, null=False)

    def __str__(self):
        return self.order


class Discounttype(models.Model):
    """ Типы скидок """
    title = models.CharField(verbose_name='Discount type', max_length=50)

    def __str__(self):
        return self.title


class Discountrule(models.Model):
    """ Правила применения скидки """
    title = models.CharField(verbose_name='Discount rule name ', max_length=50)
    discountvalue = models.FloatField(verbose_name='Discount value', null=False)
    goodset = models.TextField(verbose_name='Goods list for discount', null=False)

    def __str__(self):
        return self.title


class Discount(models.Model):
    """ Скидки """
    discounttypeidx = models.ForeignKey(Discounttype, on_delete=models.CASCADE)
    discountruleidx = models.ForeignKey(Discountrule, on_delete=models.CASCADE)
    description = models.TextField(verbose_name='Discount description', null=False)
    startdate = models.DateField(verbose_name='Discount start date', null=False)
    enddate = models.DateField(verbose_name='Discount end date', null=False)
    isactive = models.BooleanField(verbose_name='Discount activity ', default=False)
    priority = models.IntegerField(verbose_name='Discount priority ', default=0, null=False)

    def __str__(self):
        return self.description
