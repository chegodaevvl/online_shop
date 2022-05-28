from django.urls import path
from . import views


app_name = 'app_payment'

urlpatterns = [
    path('payment/', views.payment, name='payment_data_request'),
    path('payment_details/<int:payment_id>', views.payment_details, name='payment_details'),
    ]
