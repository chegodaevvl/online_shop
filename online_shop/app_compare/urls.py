from django.urls import path
from .views import add_goods_to_comparation, GoodsCompare, remove_goods


app_name = 'app_compare'

urlpatterns = [
    path('', GoodsCompare.as_view(), name='comparation'),
    path('add/<int:goods_id>/', add_goods_to_comparation, name='add_compare'),
    path('remove/<int:goods_id>/', remove_goods, name='remove_compare'),
    ]
