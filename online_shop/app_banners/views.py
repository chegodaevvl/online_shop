from django.shortcuts import render
from .utils import get_random_banners


def banners_view(request):
    context = get_random_banners(5)
    return render(request, 'app_banners/banners.html', {'context': context})
