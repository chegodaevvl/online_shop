import json
import os

from django.db.models.functions import Concat
from django.db.models import F, Value
from django.http import HttpResponseRedirect
from django.views.generic import ListView, TemplateView, DetailView
from .models import GoodsInShops, Goods, GoodsStorages, Shops
from .utils import get_hot_offers, get_limited_goods, get_top_goods, get_offer_of_the_day, LastViewed, \
    get_top_goods_by_store, get_goods_comments, get_goods_characteristics
from app_compare.compare import Comparation
from common.utils.utils import get_categories

from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from .forms import ImportForm
from .tasks import import_task

from .utils import get_hot_offers, get_limited_goods, get_top_goods, get_offer_of_the_day

from .models import GoodsInShops, Goods, GoodsStorages
from app_cart.forms import CartAddGoodForm
from app_cart.cart import Cart
from common.utils.fts import SearchResultsList
from app_users.models import Comments


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
    template_name = 'app_goods/day_offer.html'

    def get_context_data(self, **kwargs):
        context = super(DaysOfferView, self).get_context_data(**kwargs)
        context.update({'days_offer': get_offer_of_the_day()})
        return context


class GoodsDetail(DetailView):
    model = Goods
    context_object_name = 'goods'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        last_viewed = LastViewed(self.request)
        last_viewed.add(context['goods'].id)
        in_store = GoodsInShops.objects.filter(goodsidx=context['goods'])
        for line in in_store:
            if line.goodsidx.discount():
                line.price = float(line.price) * (1 - line.goodsidx.discount() / 100)
        context['in_store'] = in_store
        cart = Cart(self.request)
        context.update({'compare_count': len(Comparation(self.request))})
        context.update({'cart_count': len(cart)})
        context.update({'cart_cost': cart.total_cost()})
        context.update({'categories': get_categories()})
        context.update({'reviews': get_goods_comments(context['goods'])})
        context.update({'characteristics': get_goods_characteristics(context['goods'])})
        if 'error' in self.request.session.keys():
            context.update({'cart_error': self.request.session['error']})
            del self.request.session['error']
        #
        # good_storage_quantity = GoodsStorages.objects.get().quantity
        # cart_product_form = CartAddGoodForm(
        #     initial={'quantity': 0,
        #              'update': False,
        #              'max_quantity': good_storage_quantity, })
        # context['cart_product_form'] = cart_product_form
        #
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

    def post(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            new_comment = Comments()
            new_comment.useridx = self.request.user
            new_comment.goods = Goods.objects.get(id=kwargs['pk'])
            new_comment.text = self.request.POST['review']
            new_comment.rating = 5
            new_comment.save()
        return HttpResponseRedirect(self.request.META.get('HTTP_REFERER'))


class FindGood(SearchResultsList):
    model = Goods
    context_object_name = "goods"
    vector = ["goodsname", "description"]
    headline_expression = Concat(F("id"), F("goodsname"), F("image"),
                                  F("categoryidx_id"))
    annotate_expression = Concat('categoryidx_id__categoryname', Value(''))


class LastViewedView(TemplateView):
    template_name = 'app_goods/last_viewed_goods.html'

    def get_context_data(self, **kwargs):
        context = dict()
        context['last_viewed'] = LastViewed(self.request)
        cart = Cart(self.request)
        context.update({'compare_count': len(Comparation(self.request))})
        context.update({'cart_count': len(cart)})
        context.update({'cart_cost': cart.total_cost()})
        context.update({'categories': get_categories()})
        return context


class StoreDetail(DetailView):
    model = Shops
    context_object_name = 'store'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context.update({'compare_count': len(Comparation(self.request))})
        context.update({'cart_count': len(cart)})
        context.update({'cart_cost': cart.total_cost()})
        context.update({'categories': get_categories()})
        context.update({'solded_goods': get_top_goods_by_store(context['store'])})
        return context


class ImportView(UserPassesTestMixin, View):
    def get(self, request):
        form = ImportForm(choices=self.get_choices())
        return render(request, 'app_goods/import.html', {'form': form})

    def post(self, request):
        form = ImportForm(request.POST, choices=self.get_choices())
        if form.is_valid():
            email = form.cleaned_data['email']
            files = form.cleaned_data['files']
            import_task.delay(files=files, email=email)
            return redirect('/admin/')
        return render(request, 'app_goods/import.html', {'form': form})

    @staticmethod
    def get_choices():
        os.makedirs('import/to_import', exist_ok=True)
        choices = ((file, file) for file in os.listdir('import/to_import'))
        return choices

    def test_func(self):
        return self.request.user.is_staff
