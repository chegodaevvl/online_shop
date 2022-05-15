from django.shortcuts import render
from .models import OrderItem, Orders
from .forms import OrderCreateForm
from app_cart.cart import Cart
import json
from app_goods.models import GoodsStorages


def order_create(request):
    """Создание заказа"""
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            total_price = 0.00
            item_dict = {
                "order": order.id,
                "items": []
            }

            if cart.item_in_storage_check():
                # вывод списка товаров отсутствующих на складе
                return render(request, 'app_orders/no_items_in_storage.html',
                              {'items': cart.item_in_storage_check()})

            for item in cart:
                storage = GoodsStorages.objects.get(goodsidx=item['good'].goodsidx)

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
    else:
        form = OrderCreateForm()
        return render(request, 'app_orders/create.html', {'cart': cart, 'form': form})
