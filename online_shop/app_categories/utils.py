from django.db.models import Sum
from .models import Categories


def get_featured_categories(quantity: int):
    categories = Categories.objects.annotate(total_bought=Sum('goods__statistics__quantity'))\
                     .order_by('-total_bought')[:quantity]
    return categories
