"""online_shop URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import MainView

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', main_view, name='main'),
    path('', MainView.as_view(), name='main'),
    path('users/', include('app_users.urls')),
    path('goods/', include('app_goods.urls')),
    path('banners/', include('app_banners.urls')),
    path('categories/', include('app_categories.urls')),
    path('cart/', include('app_cart.urls', namespace='app_cart')),
    path('orders/', include('app_orders.urls', namespace='app_orders')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
