from decimal import Decimal

from django.shortcuts import render, redirect
from app_cart.cart import Cart
from app_orders.models import Orders
from app_payment.forms import PaymentDataRequestForm

from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from payments import get_payment_model, RedirectNeeded


def payment_details(request, payment_id):
    payment = get_object_or_404(get_payment_model(), id=payment_id)
    try:
        form = payment.get_form(data=request.POST or None)
    except RedirectNeeded as redirect_to:
        return redirect(str(redirect_to))
    return TemplateResponse(request, 'app_payment/payment_detail.html',
                            {'form': form, 'payment': payment})


def payment(request):
    """ оплата заказа """

    cart = Cart(request)
    order = Orders.objects.get(id=cart.get_order_id())

    if request.method == 'POST':
        form = PaymentDataRequestForm(request.POST)
        if form.is_valid():
            # заполнение данных платежа

            Payment = get_payment_model()
            payment = Payment.objects.create(
                variant='default',  # this is the variant from PAYMENT_VARIANTS
                description='online_shop purchase',
                total=Decimal(cart.get_total_price()),
                currency='USD',
                billing_first_name=request.user.first_name,
                billing_last_name=request.user.last_name,
                billing_address_1=order.address,
                customer_ip_address='127.0.0.1',
                #    tax=Decimal(20),
                #     delivery=Decimal(10),
                #     billing_address_2='',
                #     billing_city='London',
                #     billing_postcode='NW1 6XE',
                #     billing_country_code='GB',
                #     billing_country_area='Greater London',
             )

            order.paymentidx = payment
            order.save()

            # проверка валидности номера карты, по ТЗ
            if form.cleaned_data.get('bankcard_number') % 2 == 0 and \
                    form.cleaned_data.get('bankcard_number') % 10 != 0:
                response_payment_api = True
                payment.status = 'preauth'
                payment.capture()
                payment.save()

            else:
                response_payment_api = False
                payment.status = 'error'
                payment.save()

            if response_payment_api:
                # платеж прошел
                # переход к продолжению оформления заказ
                return redirect('app_orders:payment_successful')
            else:
                # платеж не прошел
                pay_error = 777
                return render(request, 'app_payment/payment_fail.html', {'pay_error': pay_error})
    else:
        form = PaymentDataRequestForm()
        return render(request, 'app_payment/payment_data_request.html', {'cart': cart,
                                                                         'form': form,
                                                                         'payment_method': order.paid.paymentmethodcode})
