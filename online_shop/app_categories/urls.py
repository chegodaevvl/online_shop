from django.urls import path
from .views import CategoriesList, FeaturedCategoriesListView


urlpatterns = [
    path('', CategoriesList.as_view(), name='categories'),
    path('featured_categories', FeaturedCategoriesListView.as_view(), name='featured_categories')
]
