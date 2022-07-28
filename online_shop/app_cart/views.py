from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from common.utils.utils import get_categories
from .cart import Cart
from app_compare.compare import Comparation


def cart_add(request, good_id, shop_id=None, quantity=1):
    """Обработчик для добавления товара в корзину"""
    cart = Cart(request)
    cart.add(good_id, shop_id, quantity)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_update(request, good_id, shop_id=None, quantity=None):
    """Обработчик для добавления товара в корзину"""
    cart = Cart(request)
    cart.update(good_id, shop_id, quantity)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_remove(request, good_id):
    """Обработчик для удаления товара из корзины"""
    cart = Cart(request)
    cart.remove(good_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class CartDetail(TemplateView):
    """Отображение корзины"""
    template_name = 'app_cart/cart_detail.html'

    def get_context_data(self, **kwargs):
        cart = Cart(self.request)
        context = super().get_context_data(**kwargs)
        context.update({'compare_count': len(Comparation(self.request))})
        context.update({'cart_count': len(cart)})
        context.update({'cart_cost': cart.total_cost()})
        context.update({'categories': get_categories()})
        context.update({'cart': cart})
        return context
