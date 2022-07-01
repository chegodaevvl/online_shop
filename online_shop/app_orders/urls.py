from django.urls import path
from .views import OrderCreate, order_created


app_name = 'app_orders'

urlpatterns = [
    path('create/', OrderCreate.as_view(), name='order_create'),
    path('created/', order_created, name='payment_successful'),
    ]
