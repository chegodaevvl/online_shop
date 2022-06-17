from django.urls import path
from .views import CategoriesList, FeaturedCategoriesListView, GoodsList


urlpatterns = [
    path('', CategoriesList.as_view(), name='categories'),
    path('featured_categories', FeaturedCategoriesListView.as_view(), name='featured_categories'),
    path('<int:cat_id>', GoodsList.as_view(), name='goods'),
]
