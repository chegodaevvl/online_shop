from django.urls import path
from .views import *


urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('login', LoginView.as_view(), name='login'),
    path('logout', LogoutView.as_view(), name='logout'),
    path('personal_account', PersonalAccountView.as_view(), name='personal_account'),
    path('profile_update', ProfileUpdateView.as_view(), name='profile_update'),
    path('password_update', PasswordUpdateForm.as_view(), name='password_update'),
    path('last_order', LastOrderView.as_view(), name='last_order'),
    path('last_viewed_goods', LastViewedGoodsListView.as_view(), name='last_viewed_goods'),
    path('browsing_history', BrowsingHistoryListView.as_view(), name='browsing_history')
]
