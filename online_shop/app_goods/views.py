from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .utils import get_hot_offers, get_limited_goods, get_top_goods, get_offer_of_the_day
from .models import Goods, GoodsInShops, GoodsStorages
from app_cart.forms import CartAddGoodForm


class HotOffersListView(ListView):
    queryset = get_hot_offers(quantity=9)
    context_object_name = 'hot_offers'
    template_name = 'app_goods/hot_offers.html'


class LimitedGoodsListView(ListView):
    queryset = get_limited_goods(quantity=16)
    context_object_name = 'limited_goods'
    template_name = 'app_goods/limited_goods.html'


class TopGoodsListView(ListView):
    queryset = get_top_goods(quantity=8)
    context_object_name = 'top_goods'
    template_name = 'app_goods/top_goods.html'


def days_offer_view(request):
    context = {'test_context': get_offer_of_the_day()}
    return render(request, 'test_page.html', context)


class _GoodsList(ListView):
    queryset = GoodsInShops.objects.all()
    context_object_name = 'goods_list'
    template_name = 'app_goods/goods_list.html'


class _GoodsDetail(DetailView):
    model = GoodsInShops
    template_name = 'app_goods/goods_detail.html'
    cart_product_form = CartAddGoodForm()
    extra_context = {'cart_product_form': cart_product_form}
