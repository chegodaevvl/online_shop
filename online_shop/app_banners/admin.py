from django.contrib import admin
from .models import Banners


class BannerAdmin(admin.ModelAdmin):
    list_display = ['advertisementname', 'bannerimg', 'isactive', 'bannerlink']


admin.site.register(Banners, BannerAdmin)
