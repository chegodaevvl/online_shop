from django.views.generic import ListView
from django.views import View
from django.shortcuts import render
from .models import Categories
from .utils import get_featured_categories
from app_goods.models import Goods


class CategoriesList(ListView):
    model = Categories
    context_object_name = 'categories'


class FeaturedCategoriesListView(ListView):
    queryset = get_featured_categories(quantity=3)
    context_object_name = 'featured_categories'
    template_name = 'app_categories/featured_categories.html'


class GoodsList(View):

    def get(self, request, cat_id):
        goods = Goods.objects.filter(categoryidx=cat_id)
        return render(request, 'app_goods/goods_list.html', context={'goods': goods})
