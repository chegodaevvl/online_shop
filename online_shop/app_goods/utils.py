from django.db.models import Q
from .models import Goods, Offer
from random import choices, sample
from typing import List
from datetime import datetime


def get_hot_offers(quantity: int) -> List[Goods]:
    hot_offers = list(Goods.objects.filter(Q(discounts__isnull=False) | Q(sets__isnull=False)))
    if len(hot_offers) > quantity:
        hot_offers = choices(hot_offers, k=quantity)
    return hot_offers
    pass


def get_limited_goods(quantity: int) -> List[Goods]:
    limited_goods = list(Goods.objects.filter(storage__limited=True))
    if len(limited_goods) > quantity:
        limited_goods = choices(limited_goods, k=quantity)
    return limited_goods
    pass


def get_sample_limited_goods():
    limited_goods_in_storage = Goods.objects.filter(storage__limited=True)
    if len(limited_goods_in_storage) > 0:
        return sample(list(limited_goods_in_storage), 1)[0]
    return None


def get_offer_of_the_day():
    limited_goods = get_sample_limited_goods()
    if limited_goods:
        Offer.objects.get_or_create(pk=1, defaults={
                'goodsidx': limited_goods,
                'startofferdate': datetime.fromisoformat('1999-01-01')
            })
        offer = Offer.objects.get(pk=1)
        if Offer.objects.get(pk=1).startofferdate.date() != datetime.today().date():
            offer.goodsidx = limited_goods
            offer.startofferdate = datetime.today().date()
            offer.save()
        return offer
    else:
        return None
