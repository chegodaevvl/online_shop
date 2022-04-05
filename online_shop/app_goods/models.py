from django.db import models
from app_categories.models import Subcategories


class Goods(models.Model):
    goodsname = models.CharField(max_length=100, verbose_name='Название товара')
    description = models.TextField(verbose_name='Описание')
    categoryidx = models.ForeignKey(Subcategories, on_delete=models.CASCADE, verbose_name='Категория')
    image = models.ImageField(upload_to='goods/', verbose_name='Изображение товара')

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'


class Shops(models.Model):
    shopname = models.CharField(max_length=50, verbose_name='Название магазина')
    address = models.CharField(max_length=100, verbose_name='Адрес')
    phone = models.PositiveIntegerField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Электронная почта')
    description = models.TextField(verbose_name='Описание')
    image = models.ImageField(upload_to='shops/', verbose_name='Изображение магазина')

    class Meta:
        verbose_name = 'Магазин'
        verbose_name_plural = 'Магазины'


class GoodsStorages(models.Model):
    goodsidx = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='Товар')
    quantity = models.PositiveIntegerField(verbose_name='Количество')
    limited = models.BooleanField(default=False, verbose_name='Ограниченный тираж')

    class Meta:
        verbose_name = 'Товар на складе'
        verbose_name_plural = 'Товары на складе'


class GoodsInShops(models.Model):
    goodsidx = models.ForeignKey(Goods, on_delete=models.CASCADE, verbose_name='Товар')
    shopidx = models.ForeignKey(Shops, on_delete=models.CASCADE, verbose_name='Магазин')
    price = models.FloatField(verbose_name='Цена')

    class Meta:
        verbose_name = 'Товар в магазине'
        verbose_name_plural = 'Товары в магазинах'
