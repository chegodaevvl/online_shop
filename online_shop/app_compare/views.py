from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from common.utils.utils import get_categories
from .compare import Comparation
from app_cart.cart import Cart


def add_goods_to_comparation(request, goods_id):
    comparation = Comparation(request)
    if goods_id not in comparation:
        comparation.add(goods_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def remove_goods(request, goods_id):
    comparation = Comparation(request)
    comparation.remove(goods_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class GoodsCompare(TemplateView):
    template_name = 'app_compare/compare.html'

    def get_context_data(self, **kwargs):
        characteristics_list = ['header', 'goods_name', 'price']
        context = dict()
        comparation_set = Comparation(self.request)
        cart = Cart(self.request)
        context.update({'compare_count': len(comparation_set)})
        context.update({'cart_count': len(cart)})
        context.update({'cart_cost': cart.total_cost()})
        context.update({'categories': get_categories()})
        if len(comparation_set) < 2:
            return None
        comparation_rows = list()
        for characteristic in characteristics_list:
            comparation_row = dict()
            if characteristic == 'header':
                comparation_row['name'] = characteristic
                comparation_row['title'] = None
                comparation_row['values'] = list()
                for item in comparation_set:
                    comparation_row['values'].append({'goods_name': item.goodsname,
                                                      'goods_image': item.image})
            elif characteristic == 'goods_name':
                comparation_row['name'] = characteristic
                comparation_row['title'] = None
                comparation_row['values'] = list()
                for item in comparation_set:
                    comparation_row['values'].append({'goods_name': item.goodsname,
                                                      'goods_id': item.id})
            else:
                comparation_row['name'] = characteristic
                comparation_row['title'] = characteristic
                comparation_row['values'] = list()
                for item in comparation_set:
                    comparation_row['values'].append(getattr(item, characteristic))
            comparation_rows.append(comparation_row)
        context['comparation_rows'] = comparation_rows
        return context
