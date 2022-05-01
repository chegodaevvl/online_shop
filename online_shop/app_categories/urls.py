from django.urls import path
from .views import CategoriesList


urlpatterns = [
    path('', CategoriesList.as_view(), name='categories')
]
