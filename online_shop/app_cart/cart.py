from decimal import Decimal
from django.conf import settings
from app_goods.models import GoodsInShops
from app_goods.models import GoodsStorages
from app_goods.models import Shops
from app_orders.models import Shipment


class Cart(object):

    def __init__(self, request):
        """Инициализация объекта корзины."""
        self.session = request.session
        cart = self.session.get(settings.CART_SESSION_ID)
        if not cart:
            # Сохраняем в сессии пустую корзину.
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        current_order = self.session.get(settings.ORDER_SESSION_ID)
        if not current_order:
            current_order = self.session[settings.ORDER_SESSION_ID] = {'order_id': 0}
        self.current_order = current_order

    def add(self, good, shop_id, quantity=1, update_quantity=False):
        """Добавление товара в корзину или обновление его количества."""

        good_id = str(good.goodsidx.id)
        if good_id not in self.cart:
            self.cart[good_id] = {'quantity': 0, 'price': str(good.price), 'shop_id': shop_id}
        if update_quantity:
            self.cart[good_id]['quantity'] = quantity
        else:
            self.cart[good_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Помечаем сессию как измененную
        self.session.modified = True

    def remove(self, good):
        """Удаление товара из корзины."""
        good_id = str(good.goodsidx.id)
        if good_id in self.cart:
            del self.cart[good_id]
        self.save()

    def __iter__(self):
        """Проходим по товарам корзины и получаем соответствующие объекты Goods."""
        good_ids = self.cart.keys()
        # good_ids = []
        # for i in self.cart.keys():
        #     if i.isdigit():
        #         good_ids.append(i)

        # Получаем объекты модели Goods и передаем их в корзину.
        goods = GoodsInShops.objects.filter(goodsidx__in=good_ids)
        cart = self.cart.copy()
        for good in goods:
            cart[str(good.goodsidx.id)]['good'] = good
        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            item['shopname'] = Shops.objects.get(id=item['shop_id']).shopname
            yield item

    def __len__(self):
        """Возвращает общее количество товаров в корзине."""
        return sum(item['quantity'] for item in self.cart.values())

    def get_total_price(self):
        return sum(
            Decimal(item['price']) * item['quantity']
            for item in self.cart.values()
            )

    def clear(self):
        # Очистка корзины.
        del self.session[settings.CART_SESSION_ID]
        # Сброс номера текущего заказа
        self.current_order['order_id'] = 0
        self.save()

    def item_in_storage_check(self) -> list:
        # проверка доступного количества товара на складе
        missing_items = []
        for good_id in self.cart.keys():
            storage = GoodsStorages.objects.get(goodsidx=int(good_id))
            if storage.quantity < self.cart[good_id]['quantity']:
                missing_items.append(storage.goodsidx)
        return missing_items

    def set_order_id(self, order_id: int):
        """ Сохранение id заказа """
        self.current_order['order_id'] = order_id
        self.save()

    def get_order_id(self):
        return self.current_order['order_id']

    def check_diff_shops(self):
        """ проверка, если в корзине товары из разных магазинов, то возвращает - True """
        shops = set()
        for item in self.cart.values():
            shops.add(item['shop_id'])
        if len(shops) > 1:
            return True
        return False

    def get_delivery_cost(self, shipment_id):
        """ Расчет стоимости доставки """
        shipment = Shipment.objects.get(id=shipment_id)
        if self.get_total_price() < shipment.minordervalue or self.check_diff_shops():
            return shipment.shippingcost + shipment.addshippingcost
        elif self.get_total_price() > shipment.minordervalue and not self.check_diff_shops():
            return shipment.addshippingcost
