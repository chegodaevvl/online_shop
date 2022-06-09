from random import sample
from typing import Set

from app_categories.models import Categories, Subcategories
from app_banners.models import Banners


def get_banners() -> list:
    banners = list(Banners.objects.filter(isactive=True))
    return sample(banners, 3)


def get_subcategories() -> list:
    favorite_subcategories = list(Subcategories.objects.all())
    return sample(favorite_subcategories, 3)


def get_categories() -> Set:
    result = Categories.objects.all()
    for item in result:
        item.child = item.categories_set.all()
    return result
