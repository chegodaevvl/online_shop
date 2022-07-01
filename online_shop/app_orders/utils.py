from .models import Shipment, PaymentMethod


def get_shipment_methods():
    return Shipment.objects.all()


def get_payment_methods():
    return PaymentMethod.objects.all()
