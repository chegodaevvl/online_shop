from django.urls import path
from . import views


app_name = 'app_cart'

urlpatterns = [
    path('', views.cart_detail, name='cart_detail'),
    path('add/<int:good_id>/', views.cart_add, name='cart_add'),
    path('remove/<int:good_id>/', views.cart_remove, name='cart_remove'),
    ]
