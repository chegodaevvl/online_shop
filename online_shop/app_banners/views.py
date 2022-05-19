from random import sample
from django.views.generic import ListView
from .models import Banners


class BannersList(ListView):
    model = Banners

    def get_context_data(self, **kwargs):
        context = dict()
        active_banners = Banners.objects.filter(isactive=True)
        banners_count = len(active_banners)
        context['context'] = list()
        if banners_count > 5:
            result_idx = sample(range(banners_count), 5)
            for idx in result_idx:
                context['context'].append(active_banners[idx])
        else:
            context = active_banners
        return context
