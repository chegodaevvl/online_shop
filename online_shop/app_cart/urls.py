from django.urls import path
from .views import cart_add, cart_remove, CartDetail


app_name = 'app_cart'

urlpatterns = [
    path('', CartDetail.as_view(), name='cart_detail'),
    path('add/<int:good_id>/', cart_add, name='cart_add'),
    path('remove/<int:good_id>/', cart_remove, name='cart_remove'),
    ]
