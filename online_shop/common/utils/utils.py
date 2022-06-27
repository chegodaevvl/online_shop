from random import sample
from typing import Set
from django.db.models import Avg

from app_categories.models import Categories
from app_banners.models import Banners
from app_goods.models import Goods, GoodsInShops


def get_banners() -> list:
    banners = list(Banners.objects.filter(isactive=True))
    return sample(banners, 3)


def get_favorite_categories() -> list:
    categories = Categories.objects.annotate(min_price=Avg('goods__goodsinshops__price'))
    result = list()
    for item in categories:
        if not item.categories_set.all():
            result.append(item)
    return sample(result, 3)


def get_categories() -> Set:
    result = Categories.objects.filter(is_active=True)
    for item in result:
        item.child = item.categories_set.all()
    return result
