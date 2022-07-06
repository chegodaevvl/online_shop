from random import sample
from datetime import datetime
from django.db.models import Q, Sum, Avg
from django.conf import settings
from .models import Goods, Offer, GoodsInShops
from app_users.models import Comments

class LastViewed(object):

    def __init__(self, request):
        self.session = request.session
        last_viewed = self.session.get(settings.LAST_VIEWED)
        if not last_viewed:
            last_viewed = self.session[settings.LAST_VIEWED] = list()
        self.last_viewed = last_viewed

    def add(self, goods_id):
        if goods_id in self.last_viewed:
            self.last_viewed.remove(goods_id)
        elif len(self.last_viewed) == 20:
            self.last_viewed.pop(0)
        self.last_viewed.append(goods_id)
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        for goods_id in self.last_viewed[::-1]:
            yield Goods.objects.get(id=goods_id)

    def __len__(self):
        return len(self.last_viewed)


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


def get_top_goods_by_store(store):
    top_goods = Goods.objects.filter(id__in=GoodsInShops.objects.filter(shopidx=store).values('goodsidx')).annotate(
        total_bought=Sum('statistics__quantity')).order_by('-total_bought')[:8]
    return top_goods


def get_goods_comments(goods_id):
    return Comments.objects.filter(goods=goods_id)
