from random import choice
from django.conf import settings
from app_goods.models import GoodsInShops, Goods


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = dict()
        self.cart = cart

    def add(self, goods_id, shop_id=None, quantity=1):
        goods_id = str(goods_id)
        if shop_id:
            goods_in_shop = GoodsInShops.objects.get(goodsidx=goods_id, shopidx=shop_id)
        else:
            goods_in_shop = choice(GoodsInShops.objects.prefetch_related('shopidx').filter(goodsidx=goods_id))
        random_shop_id = goods_in_shop.shopidx_id
        exact_price = float(goods_in_shop.price)
        if goods_in_shop.goodsidx.discount():
            exact_price *= (1 - goods_in_shop.goodsidx.discount() / 100)
        if goods_id not in self.cart.keys():
            self.cart[goods_id] = {'quantity': 0,
                                   'shop_id': random_shop_id,
                                   'price': exact_price}
        self.cart[goods_id]['quantity'] += quantity
        if shop_id and self.cart[goods_id]['shop_id'] != shop_id:
            self.cart[goods_id]['shop_id'] = shop_id
            self.cart[goods_id]['price'] = exact_price
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, goods_id):
        goods_id = str(goods_id)
        if goods_id in self.cart:
            del self.cart[goods_id]
        self.save()

    def clear(self):
        del self.session[settings.CART_SESSION_ID]
        self.save()

    def __iter__(self):
        for goods_id in self.cart:
            item = dict()
            item['goods'] = Goods.objects.get(id=goods_id)
            item['quantity'] = self.cart[goods_id]['quantity']
            item['price'] = self.cart[goods_id]['price']
            item['shop_id'] = self.cart[goods_id]['shop_id']
            item['stores'] = GoodsInShops.objects.filter(goodsidx=goods_id)
            yield item

    def __len__(self):
        return len(self.cart.keys())

    def total_cost(self):
        if len(self.cart) == 0:
            return 0
        return round(sum(item['quantity'] * item['price'] for item in self.cart.values()), 2)
