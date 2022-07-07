from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from common.utils.utils import get_categories
from .compare import Comparation
from app_cart.cart import Cart
from .utils import get_comparations_rows


def add_goods_to_comparation(request, goods_id):
    comparation = Comparation(request)
    if goods_id not in comparation:
        comparation.add(goods_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_goods(request, goods_id):
    comparation = Comparation(request)
    comparation.remove(goods_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def clear_list(request):
    comparation = Comparation(request)
    comparation.clear()
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class GoodsCompare(TemplateView):
    template_name = 'app_compare/compare.html'

    def get_context_data(self, **kwargs):
        context = dict()
        comparation_set = Comparation(self.request)
        cart = Cart(self.request)
        context.update({'compare_count': len(comparation_set)})
        context.update({'cart_count': len(cart)})
        context.update({'cart_cost': cart.total_cost()})
        context.update({'categories': get_categories()})
        context['comparation_rows'] = get_comparations_rows(comparation_set)
        return context
