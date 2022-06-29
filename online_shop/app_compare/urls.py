from django.urls import path
from .views import add_goods_to_comparation, GoodsCompare


app_name = 'app_compare'

urlpatterns = [
    path('', GoodsCompare.as_view(), name='cart_add'),
    path('add/<int:goods_id>/', add_goods_to_comparation, name='cart_add'),
    ]
