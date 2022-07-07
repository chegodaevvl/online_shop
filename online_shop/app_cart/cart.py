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
        goods_in_shops = GoodsInShops.objects.filter(goodsidx=goods_id)
        if shop_id:
            random_shop = goods_in_shops.get(shopidx=shop_id)
        else:
            random_shop = choice(goods_in_shops)
        if goods_id not in self.cart.keys():
            self.cart[goods_id] = {'quantity': quantity,
                                   'shop_id': random_shop.shopidx.id,
                                   'price': float(random_shop.price)}
            if random_shop.goodsidx.discount():
                self.cart[goods_id]['price'] *= (1 - random_shop.goodsidx.discount() / 100)
        else:
            if quantity != 1:
                self.cart[goods_id]['quantity'] = quantity
            if shop_id and self.cart[goods_id]['shop_id'] != random_shop.shopidx.id:
                self.cart[goods_id]['shop_id'] = float(random_shop.price)
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
