from django.urls import path
from .views import HotOffersListView, LimitedGoodsListView, TopGoodsListView, \
    DaysOfferView, GoodsDetail, FindGood, LastViewedView, StoreDetail


app_name = 'app_goods'
urlpatterns = [
    path('find-goods', FindGood.as_view(), name='find_goods'),
    path('top-goods', TopGoodsListView.as_view(), name='top_goods'),
    path('hot-offers', HotOffersListView.as_view(), name='hot_offers'),
    path('limited-goods', LimitedGoodsListView.as_view(), name='limited_goods'),
    path('offer-of-the-day', DaysOfferView.as_view(), name='offer-of-the-day'),
    path('<int:pk>', GoodsDetail.as_view(), name='goods-detail'),
    path('last-viewed', LastViewedView.as_view(), name='last-viewed'),
    path('shop/<int:pk>', StoreDetail.as_view(), name='last-viewed'),
]
