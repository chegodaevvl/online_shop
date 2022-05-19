from django.views.generic import ListView
from .models import Categories
from .utils import get_featured_categories


class CategoriesList(ListView):
    model = Categories


class FeaturedCategoriesListView(ListView):
    queryset = get_featured_categories(quantity=3)
    context_object_name = 'featured_categories'
    template_name = 'app_categories/featured_categories.html'
