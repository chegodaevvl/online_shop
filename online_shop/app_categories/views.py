from django.views.generic import ListView, DetailView
from django.views import View
from django.shortcuts import render
from .models import Categories, Subcategories
from .utils import get_featured_categories
from app_goods.models import Goods


class CategoriesList(ListView):
    model = Categories


class FeaturedCategoriesListView(ListView):
    queryset = get_featured_categories(quantity=3)
    context_object_name = 'featured_categories'
    template_name = 'app_categories/featured_categories.html'


class SubcategoriesView(View):

    def get(self, request, cat_id):
        linked_subcategories = Subcategories.objects.filter(categoryidx=cat_id)
        return render(request, 'app_categories/subcategories_list.html', context={'subcategories': linked_subcategories})


class GoodsList(View):

    def get(self, request, sub_id):
        goods = Goods.objects.filter(categoryidx=sub_id)
        return render(request, 'app_goods/goods_list.html', context={'goods': goods})
