from django.urls import path
from .views import banners_view


urlpatterns = [
    path('', banners_view, name='banners')
]
