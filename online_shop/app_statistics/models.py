from django.db import models


class Statisitcs(models.Model):
    goodidx = models.ForeignKey('app_goods.Goods', on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.IntegerField(verbose_name='Количество')
    dt = models.ForeignKey('app_orders.Orders', on_delete=models.CASCADE, verbose_name='Дата продажи')
