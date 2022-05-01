from django.views.generic import ListView
from .models import Categories


class CategoriesList(ListView):
    model = Categories
