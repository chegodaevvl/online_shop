from random import sample
from app_categories.models import Subcategories
from app_goods.models import Goods
from django.db.models import Min


def get_subcategories() -> list:
    favorite_subcategories = list(Subcategories.objects.all())
    # for i in range(3):
    #     min_price = Goods.objects.filter(categoryidx=favorite_subcategories[i].id).aggregate(Min('price'))
    #     favorite_subcategories[i]['price'] = min_price
    return sample(favorite_subcategories, 3)
