from django.urls import path
from .views import CategoriesList, FeaturedCategoriesListView, SubcategoriesView, GoodsList


urlpatterns = [
    path('', CategoriesList.as_view(), name='categories'),
    path('featured_categories', FeaturedCategoriesListView.as_view(), name='featured_categories'),
    path('cat-<int:cat_id>', SubcategoriesView.as_view(), name='subcategories'),
    path('sub-<int:sub_id>', GoodsList.as_view(), name='goods'),
]
