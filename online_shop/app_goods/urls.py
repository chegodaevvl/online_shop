from django.urls import path

from .views import HotOffersListView, LimitedGoodsListView, TopGoodsListView, days_offer_view
from .views import _GoodsList, _GoodsDetail

urlpatterns = [
    path('top-goods', TopGoodsListView.as_view(), name='top_goods'),
    path('hot-offers', HotOffersListView.as_view(), name='hot_offers'),
    path('limited-goods', LimitedGoodsListView.as_view(), name='limited_goods'),
    path('offer-of-the-day', days_offer_view, name='offer-of-the-day'),
    path('goods-list', _GoodsList.as_view(), name='goods_list'),
    path('goods-list/<int:pk>', _GoodsDetail.as_view()),
]
