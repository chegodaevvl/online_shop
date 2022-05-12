from django.views.generic import ListView, TemplateView, DetailView
from .utils import get_hot_offers, get_limited_goods, get_top_goods, get_offer_of_the_day
from .models import GoodsInShops, Goods, GoodsStorages
from app_cart.forms import CartAddGoodForm
import json


class HotOffersListView(ListView):
    queryset = get_hot_offers(quantity=9)
    context_object_name = 'hot_offers'
    template_name = 'app_goods/hot_offers.html'


class LimitedGoodsListView(ListView):
    queryset = get_limited_goods(quantity=16)
    context_object_name = 'limited_goods'
    template_name = 'app_goods/limited_goods.html'


class TopGoodsListView(ListView):
    queryset = get_top_goods(quantity=8)
    context_object_name = 'top_goods'
    template_name = 'app_goods/top_goods.html'


class DaysOfferView(TemplateView):
    template_name = 'app_goods/days_offer.html'

    def get_context_data(self, **kwargs):
        context = super(DaysOfferView, self).get_context_data(**kwargs)
        context.update({'days_offer': get_offer_of_the_day()})
        return context


class GoodsDetail(DetailView):
    model = Goods
    context_object_name = 'goods'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        in_store = GoodsInShops.objects.filter(goodsidx=context['goods'])
        context['in_store'] = in_store

        good_storage_quantity = GoodsStorages.objects.get(goodsidx=context['goods']).quantity
        cart_product_form = CartAddGoodForm(
            initial={'quantity': 0,
                     'update': False,
                     'max_quantity': good_storage_quantity, })
        context['cart_product_form'] = cart_product_form

        return context

    def render_to_response(self, context, **response_kwargs):
        response = super(GoodsDetail, self).render_to_response(context, **response_kwargs)
        goods_id = self.get_object().id
        if 'browsing_history' not in self.request.COOKIES:
            cookies = [goods_id]
        else:
            cookies = json.loads(self.request.COOKIES['browsing_history'])
            if goods_id in cookies:
                cookies.remove(goods_id)
            cookies.insert(0, goods_id)
            cookies = cookies[:20]
        cookies = json.dumps(cookies, default=str)

        response.set_cookie(key='browsing_history', value=cookies)
        return response
