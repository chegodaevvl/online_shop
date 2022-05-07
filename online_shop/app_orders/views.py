from django.shortcuts import render
from .models import OrderItem
from .forms import OrderCreateForm
from app_cart.cart import Cart


def order_create(request):
    """Создание заказа"""
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            order = form.save()
            print('***_order: ', order.id, type(order))
            for item in cart:
                print('***_item_order: ', order)
                print('***_good: ', item['good'])

                OrderItem.objects.create(orderidx=order,
                                         good=item['good'].goodsidx,
                                         price=item['price'],
                                         quantity=item['quantity'])
            # Очищаем корзину.
            cart.clear()
            # Вывод сообщения об успешном оформлении заказа
            return render(request, 'app_orders/created.html', {'order': order})
    else:
        form = OrderCreateForm()
        return render(request, 'app_orders/create.html', {'cart': cart, 'form': form})
