from math import ceil, floor
from django.db.models import Sum
from .models import Categories
from app_goods.models import GoodsInShops, Shops


def get_featured_categories(quantity: int):
    categories = Categories.objects.annotate(total_bought=Sum('goods__statistics__quantity'))\
                     .order_by('-total_bought')[:quantity]
    return categories


def get_min_price(query_set):
    return floor(min(item.price() for item in query_set))


def get_max_price(query_set):
    return ceil(max(item.price() for item in query_set))


def get_sellers_list(query_set):
    stores_in_view = GoodsInShops.objects.filter(goodsidx__in=query_set).values('shopidx').distinct('shopidx')
    sellers = Shops.objects.filter(id__in=stores_in_view).values('id', 'shopname')
    return sellers


def get_sellers_goods(seller_id):
    return GoodsInShops.objects.filter(shopidx=seller_id).values('goodsidx').distinct('goodsidx')
