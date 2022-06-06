from random import sample
from typing import Set

from app_categories.models import Categories, Subcategories
from app_goods.models import Goods
from django.db.models import Min


def get_subcategories() -> list:
    favorite_subcategories = list(Subcategories.objects.all())
    # for i in range(3):
    #     min_price = Goods.objects.filter(categoryidx=favorite_subcategories[i].id).aggregate(Min('price'))
    #     favorite_subcategories[i]['price'] = min_price
    return sample(favorite_subcategories, 3)


def get_categories() -> Set:
    return Categories.objects.all()
