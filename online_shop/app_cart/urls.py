from django.urls import path
from .views import cart_add, cart_update, cart_remove, CartDetail


app_name = 'app_cart'

urlpatterns = [
    path('', CartDetail.as_view(), name='cart_detail'),
    path('add/<int:good_id>/', cart_add, name='cart_add'),
    path('add/<int:good_id>/<int:shop_id>', cart_add, name='cart_add'),
    path('add/<int:good_id>=<int:quantity>', cart_add, name='cart_add'),
    path('update/<int:good_id>/<int:shop_id>', cart_update, name='cart_update'),
    path('update/<int:good_id>=<int:quantity>', cart_update, name='cart_update'),
    path('remove/<int:good_id>/', cart_remove, name='cart_remove'),
    ]
