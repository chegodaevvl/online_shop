from django.db import models


class Categories(models.Model):
        categoryname = models.CharField(max_length=50, verbose_name='Название категории')

        class Meta:
                verbose_name = 'Категория'
                verbose_name_plural = 'Категории'

        def __str__(self):
                return self.categoryname


class Subcategories(models.Model):
        categoryidx = models.ForeignKey('Categories', on_delete=models.CASCADE, verbose_name='Родительская категория')
        subcategoryname = models.CharField(max_length=50, verbose_name='Название подкатегории')
        goodcharacteristics = models.TextField(verbose_name='Перечень характеристик')

        class Meta:
                verbose_name = 'Подкатегория'
                verbose_name_plural = 'Подкатегории'

        def __str__(self):
                return self.subcategoryname



class Characteristictypes(models.Model):
        characteristictype = models.CharField(max_length=25, verbose_name='Тип характеристики')

        class Meta:
                verbose_name = 'Тип характеристик'
                verbose_name_plural = 'Типы характеристик'


class Characterisitcs(models.Model):
        characterisitctype = models.ForeignKey('Characteristictypes', on_delete=models.CASCADE, verbose_name='Тип характеристики')
        goodidx = models.ForeignKey('app_goods.Goods', on_delete=models.CASCADE, verbose_name='Товар')
        value = models.CharField(max_length=5, verbose_name='Значение характеристики')

        class Meta:
                verbose_name = 'Характеристика'
                verbose_name_plural = 'Характеристики'
