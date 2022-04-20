from django.urls import path
from .views import HotOffersListView, LimitedGoodsListView


urlpatterns = [
    path('hot-offers', HotOffersListView.as_view(), name='hot_offers'),
    path('limited-goods', LimitedGoodsListView.as_view(), name='limited_goods')
]
