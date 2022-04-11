from django.contrib import admin
from .models import Statistics


class StatisticsAdmin(admin.ModelAdmin):
    list_display = ['goodsidx', 'quantity', 'dt']


admin.site.register(Statistics, StatisticsAdmin)
