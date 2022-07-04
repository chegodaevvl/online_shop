from django.views.generic import TemplateView, ListView
from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Categories
from .utils import get_featured_categories, get_max_price, get_min_price, get_sellers_list
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
        return Goods.objects.filter(categoryidx=self.kwargs['cat_id'])

    def get_context_data(self, *, object_list=None, **kwargs):
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
