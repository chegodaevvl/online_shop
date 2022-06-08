from django.views.generic import TemplateView
from common.utils.views import get_subcategories, get_categories, get_cart_info
from app_goods.utils import get_limited_goods, get_top_goods


class MainView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({'subcats': get_subcategories()})
        context.update({'top_goods': get_top_goods(8)})
        context.update({'limited_goods': get_limited_goods(16)})
        context.update({'categories': get_categories()})
        return context
