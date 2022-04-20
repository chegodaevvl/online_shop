from django.db.models import Q
from .models import Goods
from random import choices
from typing import List


def get_hot_offers(quantity: int) -> List[Goods]:
    hot_offers = list(Goods.objects.filter(Q(discounts__isnull=False) | Q(sets__isnull=False)))
    if len(hot_offers) > quantity:
        hot_offers = choices(hot_offers, k=quantity)
    return hot_offers


def get_limited_goods(quantity: int) -> List[Goods]:
    limited_goods = list(Goods.objects.filter(storage__limited=True))
    if len(limited_goods) > quantity:
        limited_goods = choices(limited_goods, k=quantity)
    return limited_goods
