from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class UserProfiles(models.Model):
    useridx = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    fullname = models.CharField(max_length=50, verbose_name='ФИО')
    avatar = models.ImageField(upload_to='avatars/', verbose_name='Аватар')
    phone = models.PositiveIntegerField(max_length=20, verbose_name='Телефон')
    email = models.EmailField(verbose_name='Электронная почта')

    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


class Comments(models.Model):
    useridx = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    text = models.TextField(verbose_name='Текст')
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name='Оценка')

    class Meta:
        verbose_name = 'Отзыв'
        verbose_name_plural = 'Отзывы'
