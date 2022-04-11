from django.contrib import admin
from .models import Goods, GoodsStorages, GoodsInShops, Shops


class GoodsAdmin(admin.ModelAdmin):
    list_display = ['goodsname', 'description', 'image', 'categoryidx']


class GoodsStorageAdmin(admin.ModelAdmin):
    list_display = ['goodsidx', 'quantity', 'limited']


class GoodsInShopsAdmin(admin.ModelAdmin):
    list_display = ['goodsidx', 'shopidx', 'price']


class ShopsAdmin(admin.ModelAdmin):
    list_display = ['shopname', 'address', 'phone', 'email', 'description', 'image']


admin.site.register(Goods, GoodsAdmin)
admin.site.register(GoodsStorages, GoodsStorageAdmin)
admin.site.register(GoodsInShops, GoodsInShopsAdmin)
admin.site.register(Shops, ShopsAdmin)
