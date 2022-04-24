from django.urls import path
from .views import HotOffersListView, LimitedGoodsListView, days_offer_view

urlpatterns = [
    path('hot-offers', HotOffersListView.as_view(), name='hot_offers'),
    path('limited-goods', LimitedGoodsListView.as_view(), name='limited_goods'),
    path('test', days_offer_view, name='test'),
]
