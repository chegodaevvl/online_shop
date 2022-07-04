from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import TemplateView, ListView, DetailView
import json
from datetime import datetime
from .forms import OrderCreateForm
from app_cart.cart import Cart
from app_goods.models import GoodsStorages
from app_users.models import UserProfiles
from app_payment.models import Payment
from .models import OrderItem, Orders, PaymentMethod, Shipment
from .utils import get_shipment_methods, get_payment_methods
from common.utils.utils import get_categories
from app_compare.compare import Comparation
from app_cart.cart import Cart


# def order_create(request):
#     """Создание заказа"""
#     cart = Cart(request)
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#
#             # проверка что все товары в корзине есть на складе в нужном кол-ве
#             if cart.item_in_storage_check():
#                 # вывод списка товаров отсутствующих на складе
#                 return render(request, 'app_orders/no_items_in_storage.html',
#                               {'items': cart.item_in_storage_check()})
#
#             order = form.save(commit=False)
#             order.useridx = request.user
#             order.save()
#             cart.set_order_id(order.id)
#
#             # todo оплата заказа
#             return redirect('app_payment:payment_data_request')
#
#     else:
#         form = OrderCreateForm()
#         return render(request, 'app_orders/create.html', {'cart': cart, 'form': form})


class OrderCreate(TemplateView):
    template_name = 'app_orders/create.html'

    def get_context_data(self, **kwargs):
        context = dict()
        context['cart'] = Cart(self.request)
        context['user_info'] = None
        context['shipments'] = get_shipment_methods()
        context['payments'] = get_payment_methods()
        if self.request.user.is_authenticated:
            context['user_info'] = UserProfiles.objects.get(useridx=self.request.user.id)
        return context

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        shipment = Shipment.objects.get(id=request.POST['delivery'])
        payment = PaymentMethod.objects.get(id=request.POST['pay'])
        if request.user.is_authenticated:
            new_order = Orders()
            new_order.useridx = request.user
            new_order.dt = datetime.now()
            new_order.paid = payment
            new_order.paymentidx = Payment().save()
            new_order.shipment = shipment
            new_order.address = f"{request.POST['city']}, {request.POST['address']}"
            new_order.order = "Some order"
            new_order.total = cart.total_cost() + float(shipment.shippingcost) + float(shipment.addshippingcost)
            new_order.save()
            for item in cart:
                new_order_item = OrderItem()
                new_order_item.orderidx = new_order
                new_order_item.good = item['goods']
                new_order_item.price = item['price']
                new_order_item.quantity = item['quantity']
                new_order_item.save()
            # return redirect('app_payment:payment_data_request')
            return redirect(f'/payment/{new_order.id}')


def order_created(request):
    """ Завершие создания заказа - оплата и все проверки пройдены """
    cart = Cart(request)
    order = Orders.objects.get()
    total_price = 0.00
    item_dict = {
        "order": cart.get_order_id(),
        "items": []
    }
    for item in cart:
        storage = GoodsStorages.objects.get()

        # уменьшение кол-ва товара на складе
        storage.quantity -= item['quantity']
        storage.save()

        OrderItem.objects.create(orderidx=order,
                                 good=item['good'].goodsidx,
                                 price=item['price'],
                                 quantity=item['quantity'])
        total_price += float(item['price'] * item['quantity'])
        item_dict["items"].append({
            "good": item['good'].goodsidx.goodsname,
            "price": str(item['price']),
            "quantity": str(item['quantity'])
        })

    order.order = json.dumps(item_dict)
    order.total = total_price
    order.save()
    # Очищаем корзину.
    cart.clear()
    # Вывод сообщения об успешном оформлении заказа
    return render(request, 'app_orders/created.html', {'order': order})


class OrdersList(ListView):
    model = Orders
    context_object_name = 'orders'
    template_name = 'app_orders/orders_list.html'

    def get_queryset(self):
        return Orders.objects.filter(useridx=self.request.user.id)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context.update({'compare_count': len(Comparation(self.request))})
        context.update({'cart_count': len(cart)})
        context.update({'cart_cost': cart.total_cost()})
        context.update({'categories': get_categories()})
        return context


class OrderDetail(DetailView):
    model = Orders
    context_object_name = 'order'
    template_name = 'app_orders/order_detail.html'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context.update({'compare_count': len(Comparation(self.request))})
        context.update({'cart_count': len(cart)})
        context.update({'cart_cost': cart.total_cost()})
        context.update({'categories': get_categories()})
        user_profile = UserProfiles.objects.get(useridx=self.request.user.id)
        context.update({'user': user_profile})
        order_lines = OrderItem.objects.filter(orderidx=context['order'])
        context.update({'order_lines': order_lines})
        return context
