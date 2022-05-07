from django.contrib import admin
from .models import *


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ['good']


class OrdersAdmin(admin.ModelAdmin):
    list_display = ['useridx', 'order', 'dt', 'total', 'paid', 'shipment', 'address']
    list_filter = ['paid', 'dt']
    inlines = [OrderItemInline]


class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['card', 'foreignaccount']


class ShipmentMethodAdmin(admin.ModelAdmin):
    list_display = ['normal', 'express']


class ShipmentRulesAdmin(admin.ModelAdmin):
    list_display = ['freenormal', 'paidnormal', 'paidexpress']


class DiscountsRulesAdmin(admin.ModelAdmin):
    list_display = ['percentdiscount', 'normaldiscount', 'fixedprice']


class GoodsDiscountsAdmin(admin.ModelAdmin):
    list_display = ['goodsidx', 'discountruleidx', 'goodsdiscount']


class GoodsDiscountsCalendarAdmin(admin.ModelAdmin):
    list_display = ['goodsidx', 'startdt', 'enddt', 'isactive']


class GoodsSetsAdmin(admin.ModelAdmin):
    list_display = ['goodsidx', 'discountruleidx', 'goodsset', 'setdiscount']


class SetsDiscountsCalendarAdmin(admin.ModelAdmin):
    list_display = ['setidx', 'startdt', 'enddt', 'isactive']




admin.site.register(Orders, OrdersAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(ShipmentMethod, ShipmentMethodAdmin)
admin.site.register(ShipmentRules, ShipmentRulesAdmin)
admin.site.register(DiscountsRules, DiscountsRulesAdmin)
admin.site.register(GoodsDiscounts, GoodsDiscountsAdmin)
admin.site.register(GoodsDiscountsCalendar, GoodsDiscountsCalendarAdmin)
admin.site.register(GoodsSets, GoodsSetsAdmin)
admin.site.register(SetsDiscountsCalendar, SetsDiscountsCalendarAdmin)
