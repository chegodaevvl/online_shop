from math import ceil, floor
from django.db.models import Sum
from .models import Categories


def get_featured_categories(quantity: int):
    categories = Categories.objects.annotate(total_bought=Sum('goods__statistics__quantity'))\
                     .order_by('-total_bought')[:quantity]
    return categories


def get_min_price(query_set):
    return floor(min(item.price() for item in query_set))


def get_max_price(query_set):
    return ceil(max(item.price() for item in query_set))
