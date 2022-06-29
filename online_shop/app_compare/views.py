from django.views.generic import TemplateView
from django.http import HttpResponseRedirect
from .compare import Comparation


def add_goods_to_comparation(request, goods_id):
    comparation = Comparation(request)
    if goods_id not in comparation:
        comparation.add(goods_id)
    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


class GoodsCompare(TemplateView):
    template_name = 'app_compare/compare.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        row_number = 0
        comparation_set = Comparation(self.request)
        if len(comparation_set) == 0:
            return None
        context.update({row_number: ['', '', 'Цена']})
        for goods in comparation_set:
            row_number += 1
            context.update({row_number: [goods.goodsname, goods.image, goods.price]})
        print(context)
        return context
