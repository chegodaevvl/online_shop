from .models import Shipment, PaymentMethod, Orders


def get_shipment_methods():
    return Shipment.objects.all()


def get_payment_methods():
    return PaymentMethod.objects.all()


def get_last_order(user_id: int):
    return Orders.objects.filter(useridx=user_id).order_by('-dt')[0]
