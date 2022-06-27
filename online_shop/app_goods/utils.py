from django.db.models import Q, Sum, Avg
from .models import Goods, Offer, GoodsInShops
from random import sample
from datetime import datetime


def get_hot_offers(quantity: int):
    pass
    # hot_offers = list(Goods.objects.filter(Q(discounts__isnull=False) | Q(sets__isnull=False)).
    #                   annotate(price=Avg('goodsinshops__price')))
    # if len(hot_offers) > quantity:
    #     hot_offers = sample(hot_offers, k=quantity)
    # return hot_offers


def get_limited_goods(quantity: int):
    pass
    limited_goods = list(Goods.objects.filter(Q(storage__limited=True) & Q(offer__isnull=True)).
                         annotate(price=Avg('goodsinshops__price')))
    if len(limited_goods) > quantity:
        limited_goods = sample(limited_goods, k=quantity)
    return limited_goods


def get_top_goods(quantity: int):
    top_goods = Goods.objects.annotate(
        total_bought=Sum('statistics__quantity')).order_by('-total_bought')[:quantity]
    return top_goods


def get_offer_of_the_day():
    limited_goods = get_limited_goods(quantity=1)
    if limited_goods:
        offer = Offer.objects.get_or_create(pk=1, defaults={
                'goodsidx': limited_goods[0],
                'startofferdate': datetime.fromisoformat('1999-01-01')
            })[0]
        if offer.startofferdate.date() != datetime.today().date():
            offer.goodsidx = limited_goods[0]
            offer.startofferdate = datetime.today().date()
            offer.save()
        return offer.goodsidx
    else:
        return None
