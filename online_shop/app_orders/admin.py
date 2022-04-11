from django.contrib import admin
from .models import Orders, Discount, DiscountRule, DiscountType, PaymentMethod, ShipmentMethod, ShipmentRules


class OrdersAdmin(admin.ModelAdmin):
    list_display = ['useridx', 'order', 'dt', 'total', 'paid', 'shipment', 'address']


class DiscountAdmin(admin.ModelAdmin):
    list_display = ['discounttypeidx', 'discountruleidx', 'description', 'startdate', 'enddate', 'isactive', 'priority']


class DiscountRuleAdmin(admin.ModelAdmin):
    list_display = ['title', 'discountvalue', 'goodsset']


class DiscountTypeAdmin(admin.ModelAdmin):
    list_display = ['title']


class PaymentMethodAdmin(admin.ModelAdmin):
    list_display = ['card', 'foreignaccount']


class ShipmentMethodAdmin(admin.ModelAdmin):
    list_display = ['normal', 'express']


class ShipmentRulesAdmin(admin.ModelAdmin):
    list_display = ['freenormal', 'paidnormal', 'paidexpress']


admin.site.register(Orders, OrdersAdmin)
admin.site.register(Discount, DiscountAdmin)
admin.site.register(DiscountType, DiscountTypeAdmin)
admin.site.register(DiscountRule, DiscountRuleAdmin)
admin.site.register(PaymentMethod, PaymentMethodAdmin)
admin.site.register(ShipmentMethod, ShipmentMethodAdmin)
admin.site.register(ShipmentRules, ShipmentRulesAdmin)
