from django.views.generic import ListView
from .utils import get_hot_offers, get_limited_goods


class HotOffersListView(ListView):
    queryset = get_hot_offers(quantity=9)
    context_object_name = 'hot_offers'
    template_name = 'app_goods/hot_offers.html'


class LimitedGoodsListView(ListView):
    queryset = get_limited_goods(quantity=16)
    context_object_name = 'limited_goods'
    template_name = 'app_goods/limited_goods.html'
