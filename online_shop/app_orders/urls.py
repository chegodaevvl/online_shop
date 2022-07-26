from django.urls import path
from .views import OrderCreate, order_created, OrdersList, OrderDetail


app_name = 'app_orders'

urlpatterns = [
    path('create/', OrderCreate.as_view(), name='order_create'),
    path('created/', order_created, name='payment_successful'),
    path('', OrdersList.as_view(), name='orders_history'),
    path('<int:pk>/', OrderDetail.as_view(), name='order_detail'),
    ]
