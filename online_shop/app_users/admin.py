from django.contrib import admin
from .models import UserProfiles, Comments


class UserProfilesAdmin(admin.ModelAdmin):
    list_display = ['useridx', 'fullname', 'avatar', 'phone', 'email']


class CommentsAdmin(admin.ModelAdmin):
    list_display = ['useridx', 'goods', 'text', 'rating']


admin.site.register(UserProfiles, UserProfilesAdmin)
admin.site.register(Comments, CommentsAdmin)
