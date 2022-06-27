from django.views.generic import TemplateView
from common.utils.utils import get_favorite_categories, get_banners, get_categories
from app_goods.utils import get_limited_goods, get_top_goods, get_hot_offers, get_offer_of_the_day


class MainView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'banners': get_banners()})
        context.update({'favorite_categories': get_favorite_categories()})
        print(context['favorite_categories'])
        context.update({'categories': get_categories()})
        context.update({'day_offer': get_offer_of_the_day()})
        context.update({'top_goods': get_top_goods(8)})
        context.update({'hot_goods': get_hot_offers(9)})
        # context.update({'hot_goods': get_top_goods(9)})
        context.update({'limited_goods': get_limited_goods(16)})
        return context
