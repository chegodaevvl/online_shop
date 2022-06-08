from random import sample
from typing import Set

from app_categories.models import Categories, Subcategories
from app_goods.models import Goods
from app_cart.cart import Cart


def get_cart_info():
    cart = Cart()
    cart_info = {'quantity': len(cart),
                 'total': cart.get_total_price(),
                 }
    return cart_info


def get_subcategories() -> list:
    favorite_subcategories = list(Subcategories.objects.all())
    return sample(favorite_subcategories, 3)


def get_categories() -> Set:
    return Categories.objects.all()
