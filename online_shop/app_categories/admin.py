from django.contrib import admin
from .models import Categories, Characteristics, CharacteristicTypes, Subcategories


class CategoriesAdmin(admin.ModelAdmin):
    list_display = ['categoryname']


class CharacteristicsAdmin(admin.ModelAdmin):
    list_display = ['characteristictype', 'goodsidx', 'value']


class CharacteristicTypesAdmin(admin.ModelAdmin):
    list_display = ['characteristictype']


class SubcategoriesAdmin(admin.ModelAdmin):
    list_display = ['categoryidx', 'subcategoryname', 'goodscharacteristics']


admin.site.register(Categories, CategoriesAdmin)
admin.site.register(Characteristics, CharacteristicsAdmin)
admin.site.register(CharacteristicTypes, CharacteristicTypesAdmin)
admin.site.register(Subcategories, SubcategoriesAdmin)
