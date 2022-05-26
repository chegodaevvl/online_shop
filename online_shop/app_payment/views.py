from django.shortcuts import render, redirect
from app_cart.cart import Cart
from app_orders.models import Orders
from app_payment.forms import PaymentDataRequestForm


def payment(request):
    """ оплата заказа """

    cart = Cart(request)
    if request.method == 'POST':
        form = PaymentDataRequestForm(request.POST)
        if form.is_valid():
            # отправка данных в платежную систему
            print('***_request payment API')
            pass
            response_payment_api = True
            if response_payment_api:
                # платеж прошел
                # переход к продолжению оформления заказа
                return redirect('app_orders:payment_successful')
            else:
                # платеж не прошел
                pay_error = 777
                return render(request, 'app_payment/payment_fail.html', {'pay_error': pay_error})
    else:
        form = PaymentDataRequestForm()
        return render(request, 'app_payment/payment_data_request.html', {'cart': cart, 'form': form})


