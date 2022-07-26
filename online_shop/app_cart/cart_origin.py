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
        cart = self.session.get()
        if not cart:
            # Сохраняем в сессии пустую корзину.
            cart = self.session[settings.CART_SESSION_ID] = {}
        self.cart = cart
        current_order = self.session.get()
        if not current_order:
            current_order = self.session[settings.ORDER_SESSION_ID] = {'order_id': 0}
        self.current_order = current_order

    def add(self, good, shop_id, quantity=1, update_quantity=False):
        """Добавление товара в корзину или обновление его количества."""

        good_id = str(good.goodsidx.id)     #  good - объект из таблицы GoodsInShops
        discount_type = discount_id = 0
        discount_applied = False

        #  проверка участия товара в скидках 1-го типа
        discount_type1 = GoodsInShops.objects.get().get_discount_type1()
        if discount_type1:
            discount_price = Discounts.objects.get().get_discount_price(
                GoodsInShops.objects.get().price
            )
            if discount_price > 0:
                discount_applied = True
                discount_type = 1
                discount_id = discount_type1.id
        else:
            discount_applied = False
            discount_price = 0
            #  проверка участия товара в скидках 2-го типа
            discount_id = self.get_discount_on_set(good.goodsidx.id)
            if discount_id > 0:
                discount_type = 2

        if good_id not in self.cart:
            self.cart[good_id] = {
                'quantity': 0,
                'price': float(good.price),
                'shop_id': shop_id,
                'discount_id': discount_id,
                'discount_type': discount_type,
                'discount_applied': discount_applied,
                'discount_price': float(discount_price),
            }
        if update_quantity:
            self.cart[good_id]['quantity'] = quantity
        else:
            self.cart[good_id]['quantity'] += quantity
        self.save()

    def save(self):
        # Помечаем сессию как измененную
        self.session.modified = True
        self.check_discounts_on_set()
        self.check_discounts_on_cart()
        #self.print_cart()

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
            item['price'] = item['price']
            if item['discount_price'] == 0:
                item['total_price'] = item['price'] * item['quantity']
            else:
                item['total_price'] = item['discount_price'] * item['quantity']
            item['shopname'] = Shops.objects.get().shopname
            yield item

    def __len__(self):
        """Возвращает общее количество товаров в корзине."""
        return sum(item['quantity'] for item in self.cart.values())

    def print_cart(self):
        """ для отладки """
        for k, v in self.cart.items():
            print('***cart:', k, v)
        print('number_of_items:', self.get_number_of_items())

    def get_number_of_items(self):
        """ получение кол-ва позиций в корзине """
        return len(self.cart.keys())

    def get_total_price(self):
        """ получение цены позиции корзины с учетом скидок"""
        return sum(
            item['price'] * item['quantity'] if item['discount_price'] == 0
            else item['discount_price'] * item['quantity']
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
            storage = GoodsStorages.objects.get()
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
        shipment = Shipment.objects.get()
        if self.get_total_price() < shipment.minordervalue or self.check_diff_shops():
            return shipment.shippingcost + shipment.addshippingcost
        elif self.get_total_price() > shipment.minordervalue and not self.check_diff_shops():
            return shipment.addshippingcost

    def get_discount_on_set(self, good_id) -> int:
        """ проверка участвует ли товар в скидках 2-го типа """

        subcategories = Goods.objects.get().categoryidx
        if subcategories.parent:
            categories_id = Categories.objects.get().id
        else:
            categories_id = subcategories.id
        active_discount_good = Discounts.objects.filter(active=True, type=2, goodsset__goodsidx=good_id). \
            order_by('priority').last()
        active_discount_category = Discounts.objects.filter(active=True, type=2,
                                                            categoriesset__categoriesidx=categories_id). \
            order_by('priority').last()
        #  если есть активные скидки на товар, то эта скидка приоритетней чем скидка на категорию товара
        if active_discount_good:
            return active_discount_good.id
        elif active_discount_category:
            return active_discount_category.id
        else:
            return 0

    def modify_price_for_discount_on_set(self, discount_id, good_id):
        """ изменение скидосной цены товаров которые попали в скидку 2-го типа """
        discount_price = Discounts.objects.get().get_discount_price(self.cart[good_id]['price'])
        if discount_price > 0:
            self.cart[good_id]['discount_price'] = discount_price
            self.cart[good_id]['discount_applied'] = True
        else:
            self.cart[good_id]['discount_price'] = discount_price
            self.cart[good_id]['discount_applied'] = False

    def get_discount_on_cart(self) -> int:
        """ проверка применима ли к корзине скидка 3-го типа, получение id скидки
        проверка в части наличия в корзине других скидок """
        #  проверка есть ли активные скидки 3-го типа, выбор скидки с большим приоритетом, либо с большим id
        active_discount = Discounts.objects.filter(type=3, active=True).order_by('priority').last()
        if active_discount:
            for good_id, cart_data in self.cart.items():
                if cart_data['discount_applied'] and cart_data['discount_type'] != 3:
                    #  если в корзине есть товары с любой другой примененной скидкой, то скидка на корзину не применима
                    return 0
            return active_discount.id
        return 0

    def check_discounts_on_cart(self):
        """ коррекция данных товаров в корзине по условиям скидки 3-го типа """
        discount_id = self.get_discount_on_cart()
        if discount_id > 0:
            minimumvalue = Discounts.objects.get().minimumvalue
            numberofitems = Discounts.objects.get().numberofitems
            if self.get_total_price() >= minimumvalue and self.get_number_of_items() >= numberofitems and \
                    minimumvalue + numberofitems > 0:
                #  условие скидки выполнено
                for cart_data in self.cart.values():
                    cart_data['discount_id'] = discount_id
                    cart_data['discount_type'] = 3
                    cart_data['discount_applied'] = True
                    cart_data['discount_price'] = Discounts.objects.get().\
                        get_discount_price(cart_data['price'])
                return

        #  условие скидки не выполнено
        for cart_data in self.cart.values():
            if cart_data['discount_type'] in (0, 3):
                cart_data['discount_id'] = 0
                cart_data['discount_type'] = 0
                cart_data['discount_applied'] = False
                cart_data['discount_price'] = 0

    def check_discounts_on_set(self):
        """ проверка корзины на скидки 2-го типа """
        first_item = None
        for good_id, cart_data in self.cart.items():
            if cart_data['discount_applied'] and cart_data['discount_type'] == 1:
                pass
            else:
                if cart_data['discount_type'] == 2:
                    cart_data['discount_applied'] = False
                    cart_data['discount_price'] = 0
                    if first_item and self.set_number_check((cart_data['discount_id'],
                                                            good_id,
                                                            self.cart[first_item]['discount_id'],
                                                            first_item)):
                        self.modify_price_for_discount_on_set(cart_data['discount_id'], good_id)
                        self.modify_price_for_discount_on_set(self.cart[first_item]['discount_id'], first_item)
                        first_item = None
                    else:
                        first_item = good_id

    def get_number_set(self, discount_id, good_id) -> int:
        """ получение номера набора для скидки 2-го типа"""
        if GoodsSet.objects.filter(goodsidx=good_id, discountsidx=discount_id).exists():
            return GoodsSet.objects.get().setnumber
        else:
            subcategories = Goods.objects.get().categoryidx
            if subcategories.parent:
                categories_id = Categories.objects.get().id
            else:
                categories_id = subcategories.id
            if CategoriesSet.objects.filter(categoriesidx=categories_id, discountsidx=discount_id).exists():
                return CategoriesSet.objects.get().setnumber
            return 0

    def set_number_check(self, id: tuple) -> bool:
        """ проверка что товары состоят в разных наборах """
        if self.get_number_set(id[0], id[1]) * self.get_number_set(id[2], id[3]) == 2:
            return True
        return False
