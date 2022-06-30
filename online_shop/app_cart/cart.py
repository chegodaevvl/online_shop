from django.conf import settings
from app_goods.models import Goods, GoodsInShops


class Cart(object):

    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            cart = self.session[settings.CART_SESSION_ID] = dict()
        self.cart = cart

    def add(self, goods_id, shop_id=None, quantity=1):
        goods = Goods.objects.get(id=goods_id)
        if goods_id not in self.cart.keys():
            self.cart['goods_id'] = {'quantity': 0,
                                     'shop_id': None,
                                     'price': float(goods.price())}
        self.cart['goods_id']['quantity'] += quantity
        if shop_id:
            self.cart['goods_id']['shop_id'] = shop_id
        if goods.discount():
            self.cart['goods_id']['price'] = goods.discount_price()
        self.save()

    def save(self):
        self.session.modified = True

    def remove(self, goods_id):
        if goods_id in self.cart.keys():
            del self.cart['goods_id']
        self.save()

    def __iter__(self):
        goods = GoodsInShops.objects.filter(godsidx__in=self.cart)
        for item in goods:
            yield item

    def __len__(self):
        return len(self.cart.keys())

    def total_cost(self):
        if len(self.cart) == 0:
            return 0
        return round(sum(item['quantity'] * item['price'] for item in self.cart.values()), 2)
