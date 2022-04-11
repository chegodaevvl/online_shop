from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.translation import gettext_lazy as _


class UserProfiles(models.Model):
    """Профили пользователей"""
    useridx = models.OneToOneField('auth.User', on_delete=models.CASCADE, verbose_name=_('user'))
    fullname = models.CharField(max_length=50, verbose_name=_('fullname'))
    avatar = models.ImageField(upload_to='avatars/', verbose_name=_('avatar'))
    phone = models.PositiveIntegerField(verbose_name=_('phone'))
    email = models.EmailField(verbose_name=_('email'))

    class Meta:
        verbose_name = _('user profile')
        verbose_name_plural = _('user profiles')

    def __str__(self):
        return self.fullname


class Comments(models.Model):
    """Отзывы"""
    useridx = models.ForeignKey('auth.User', on_delete=models.CASCADE, verbose_name=_('user'))
    goods = models.ForeignKey('app_goods.Goods', on_delete=models.CASCADE, verbose_name=_('goods'))
    text = models.TextField(verbose_name=_('text'))
    rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name=_('rating'))

    class Meta:
        verbose_name = _('comment')
        verbose_name_plural = _('comments')
        
    def __str__(self):
        return f'{self.text[:50]}...'
