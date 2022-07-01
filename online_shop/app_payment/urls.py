from django.urls import path
from .views import order_payment, payment_details, PaymentProcessing


app_name = 'app_payment'

urlpatterns = [
    path('<int:order_id>', order_payment, name='payment_data_request'),
    path('processing', PaymentProcessing.as_view(), name='payment_processing'),
    path('payment_details/<int:payment_id>', payment_details, name='payment_details'),
    ]
