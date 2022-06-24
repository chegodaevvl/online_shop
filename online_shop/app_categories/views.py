from django.views.generic import TemplateView, ListView
from django.views import View
from django.shortcuts import render
from django.core.paginator import Paginator
from .models import Categories
from .utils import get_featured_categories
from app_goods.models import Goods
from common.utils.utils import get_categories


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
