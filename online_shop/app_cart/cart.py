from decimal import Decimal
from django.conf import settings
from app_goods.models import GoodsInShops, Goods
from app_goods.models import GoodsStorages
from app_goods.models import Shops
from app_orders.models import Shipment, Discounts, GoodsSet, CategoriesSet

from app_categories.models import Subcategories, Categories


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

        good_id = str(good.goodsidx.id)     #  id из таблицы GoodsInShops

        #  проверка участия товара в скидках 1-го типа
        discount_price = GoodsInShops.objects.get(id=good_id).discountprice()
        if discount_price < float(str(good.price)):
            discount_applied = True
        else:
            discount_applied = False

        #  проверка участия товара в скидках 2-го типа
        discount2_id = self.get_discount_on_set(good)

        if good_id not in self.cart:
            self.cart[good_id] = {
                'quantity': 0,
                'price': str(good.price),
                'shop_id': shop_id,
                'discount2_id': discount2_id,
                'discount_applied': discount_applied,
                'discount_price': discount_price,
            }
        if update_quantity:
            self.cart[good_id]['quantity'] = quantity
        else:
            self.cart[good_id]['quantity'] += quantity
        self.save()

        #  коррекция цен по условию скидки 2-го типа, если добавленный товар участвует в такой скидке
        if len(self.cart.keys()) > 1 and discount2_id > 0:
            self.modify_price_for_discount_on_set(discount2_id)

        self.print_cart()

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

    def print_cart(self):
        for k, v in self.cart.items():
            print('***cart:', k, v)

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

    def get_discount_on_set(self, good: Goods) -> int:
        """ проверка участвует ли товар в скидках 2-го типа """

        subcategories = Subcategories.objects.get(id=good.goodsidx.categoryidx.id)
        categories_id = Categories.objects.get(id=subcategories.categoryidx.id).id
        active_discount_good = Discounts.objects.filter(active=True, type=2, goodsset__goodsidx=good.goodsidx.id). \
            order_by('priority').last()
        active_discount_category = Discounts.objects.filter(active=True, type=2,
                                                            categoriesset__categoriesidx=categories_id). \
            order_by('priority').last()
        #  если есть активные скидки на товар, то эта скидка приоритетней чем скидка на категорию
        if active_discount_good:
            return active_discount_good.id
        elif active_discount_category:
            return active_discount_category.id
        else:
            return 0

    def modify_price_for_discount_on_set(self, discount_id):
        """ изменение цены товаров которые попали в скидку 2-го типа """
        discount = Discounts.objects.get(id=discount_id)
        for good_id, value in self.cart.items():
            if value['discount2_id'] == discount_id and not value['discount_applied']:
                if discount.discountpercentage > 0:
                    self.cart[good_id]['discount_price'] = float(value['price']) * \
                                                           (100 - discount.discountpercentage) / 100
                    self.cart[good_id]['discount_applied'] = True
                elif discount.discountamount > 0:
                    if discount.discountamount >= float(value['price']):
                        self.cart[good_id]['discount_price'] = 1
                        self.cart[good_id]['discount_applied'] = True
                    else:
                        self.cart[good_id]['discount_price'] = float(value['price']) - discount.discountamount
                        self.cart[good_id]['discount_applied'] = True
                elif discount.fixedcost > 0:
                    self.cart[good_id]['discount_price'] = discount.fixedcost
                    self.cart[good_id]['discount_applied'] = True

    def check_discount_on_cart(self) -> int:
        """ проверка применима ли к корзине скидка 3-го типа """
        pass
        #  проверка есть ли активные скидки 3-го типа, выбор скидки с большим приоритетом, либо с большим id
        active_discount = Discounts.objects.filter(type=3, active=True).order_by('priority').last()
        if active_discount:

            for good_id, cart_data in self.cart.items():
                if cart_data['discount_applied']:
                    #  если в корзине есть товары с примененной скидкой, то скидка на корзину не применима
                    return 0
            return active_discount.id



        # subcategories = Subcategories.objects.get(id=good.goodsidx.categoryidx.id)
        # categories_id = Categories.objects.get(id=subcategories.categoryidx.id).id
        # active_discount_good = Discounts.objects.filter(active=True, type=2, goodsset__goodsidx=good.goodsidx.id). \
        #     order_by('priority').last()
        # active_discount_category = Discounts.objects.filter(active=True, type=2,
        #                                                     categoriesset__categoriesidx=categories_id). \
        #     order_by('priority').last()
        # #  если есть активные скидки на товар, то эта скидка приоритетней чем скидка на категорию
        # if active_discount_good:
        #     return active_discount_good.id
        # elif active_discount_category:
        #     return active_discount_category.id
        # else:
        #     return 0