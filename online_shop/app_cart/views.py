from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.http import HttpResponseRedirect
from app_goods.models import GoodsInShops, GoodsStorages, Goods
from .cart import Cart
from .forms import CartAddGoodForm


# @require_POST
# def cart_add(request, good_id):
#     """Обработчик для добавления товара в корзину"""
#     cart = Cart(request)
#     good = get_object_or_404(GoodsInShops, id=good_id)
#
#     form = CartAddGoodForm(request.POST)
#     if form.is_valid():
#         cd = form.cleaned_data
#         cart.add(good=good, shop_id=good.shopidx.id, quantity=cd['quantity'], update_quantity=cd['update'])
#         return redirect('app_cart:cart_detail')
#
#     if form.data['update'] == 'False':
#         return redirect('app_goods:goods-detail', good.goodsidx.id)
#
#     return redirect('app_cart:cart_detail')


def cart_add(request, good_id):
    """Обработчик для добавления товара в корзину"""
    cart = Cart(request)
    cart.add(good_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def cart_remove(request, good_id):
    """Обработчик для удаления товара из корзины"""
    cart = Cart(request)
    cart.remove(good_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


# def cart_detail(request):
#     """Отображение корзины"""
#     cart = Cart(request)
#     for item in cart:
#         good_storage_quantity = GoodsStorages.objects.get(goodsidx=item['good'].goodsidx).quantity
#         item['update_quantity_form'] = CartAddGoodForm(
#             initial={'quantity': item['quantity'],
#                      'update': True,
#                      'max_quantity': good_storage_quantity})
#     return render(request, 'app_cart/cart_detail.html', {'cart': cart})


def cart_detail(request):
    """Отображение корзины"""
    cart = Cart(request)
    # for item in cart:
    #     good_storage_quantity = GoodsStorages.objects.get(goodsidx=item['good'].goodsidx).quantity
    #     item['update_quantity_form'] = CartAddGoodForm(
    #         initial={'quantity': item['quantity'],
    #                  'update': True,
    #                  'max_quantity': good_storage_quantity})
    return render(request, 'app_cart/cart_detail.html', {'cart': cart})
