from unicodedata import decimal

from django.db.models import Avg
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView, ListView
from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Categories
from .utils import get_featured_categories, get_max_price, get_min_price, get_sellers_list, get_sellers_goods
from app_goods.models import Goods
from common.utils.utils import get_categories
from app_compare.compare import Comparation
from app_cart.cart import Cart


class CategoriesList(ListView):
    model = Categories
    context_object_name = 'categories'


class FeaturedCategoriesListView(ListView):
    queryset = get_featured_categories(quantity=3)
    context_object_name = 'featured_categories'
    template_name = 'app_categories/featured_categories.html'


class GoodsList(ListView):
    context_object_name = 'goods'
    template_name = 'app_goods/goods_list.html'
    paginate_by = 8

    def get_queryset(self):
        # TODO: Pagination for filtered queryset
        goods = Goods.objects.filter(categoryidx=self.kwargs['cat_id'])
        if 'title' in self.request.GET:
            goods = goods.filter(goodsname__contains=self.request.GET['title'])
        if 'seller' in self.request.GET:
            goods = goods.filter(id__in=get_sellers_goods(self.request.GET['seller']))
        if 'price' in self.request.GET:
            price_range = list(map(float, self.request.GET['price'].split(';')))
            goods = goods.filter(goodsinshops__price__range=(price_range[0], price_range[1]))
        if 'available' in self.request.GET:
            goods = goods.filter(storage__quantity__gte=1)
        return goods

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'min_price': get_min_price(context['goods'])})
        context.update({'max_price': get_max_price(context['goods'])})
        context.update({'sellers': get_sellers_list(context['goods'])})
        cart = Cart(self.request)
        context.update({'compare_count': len(Comparation(self.request))})
        context.update({'cart_count': len(cart)})
        context.update({'cart_cost': cart.total_cost()})
        context.update({'categories': get_categories()})
        return context

    # def post(self, request, *args, **kwargs):
    #     goods = self.get_queryset()
    #     # context.annotate(price=goodsinshops.aggregate(Avg('price')))
    #     # min_price, max_price = request.POST['price'].split(';')
    #     # min_price = float(min_price)
    #     # max_price = float(max_price)
    #     # context = context.filter(price__value=(min_price, max_price))
    #     goods_title = request.POST['title']
    #     goods = goods.filter(goodsname__contains=goods_title)
    #     # seller_id = request.POST['seller']
    #     print(goods)
    #     return goods
