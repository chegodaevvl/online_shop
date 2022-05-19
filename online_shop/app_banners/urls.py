from django.urls import path
from .views import BannersList


urlpatterns = [
    path('', BannersList.as_view(), name='banners')
]
