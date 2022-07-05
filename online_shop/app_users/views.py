from django.shortcuts import redirect, reverse, render
from django.contrib.auth import views, authenticate, login
from django.contrib.auth.models import User
from django.views import View
from django.views.generic import ListView, DetailView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth import update_session_auth_hash
from .forms import ProfileForm
from .utils import get_browsing_history
from app_orders.models import Orders
from app_orders.utils import get_last_order
from app_goods.utils import LastViewed
from common.utils.utils import get_favorite_categories, get_banners, get_categories
from app_compare.compare import Comparation
from app_cart.cart import Cart


class LoginView(views.LoginView):
    template_name = 'app_users/login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context.update({'compare_count': len(Comparation(self.request))})
        context.update({'cart_count': len(cart)})
        context.update({'cart_cost': cart.total_cost()})
        context.update({'categories': get_categories()})
        return context


class LogoutView(views.LogoutView):
    next_page = '/users/login'


class RegisterView(View):
    def get(self, request):
        user_form = UserCreationForm()
        profile_form = ProfileForm()
        return render(request, 'app_users/register.html', {'user_form': user_form, 'profile_form': profile_form})

    def post(self, request):
        user_form = UserCreationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            profile = profile_form.save(commit=False)
            profile.useridx = User.objects.get()
            profile.save()
            username = user_form.cleaned_data.get()
            password = user_form.cleaned_data.get()
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect(reverse('personal_account'))
        return render(request, 'app_users/register.html', {'user_form': user_form, 'profile_form': profile_form})


class ProfileUpdateView(LoginRequiredMixin, View):
    def get(self, request):
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, 'app_users/profile_update.html', {'form': profile_form})

    def post(self, request):
        profile_form = ProfileForm(request.POST, request.FILES, instance=request.user.profile)
        if profile_form.is_valid():
            profile_form.save()
            return redirect(reverse('personal_account'))
        return render(request, 'app_users/profile_update.html', {'form': profile_form})


class PasswordUpdateForm(LoginRequiredMixin, View):
    def get(self, request):
        password_form = PasswordChangeForm(request.user)
        return render(request, 'app_users/password_update.html', {'form': password_form})

    def post(self, request):
        password_form = PasswordChangeForm(request.user, request.POST)
        if password_form.is_valid():
            user = password_form.save()
            update_session_auth_hash(request, user)
            return redirect(reverse('profile_update'))
        return render(request, 'app_users/password_update.html', {'form': password_form})


class LastOrderView(LoginRequiredMixin, TemplateView):
    template_name = 'app_users/last_order.html'

    def get_context_data(self, **kwargs):
        context = super(LastOrderView, self).get_context_data(**kwargs)
        last_order = Orders.objects.filter(useridx=self.request.user).order_by('-dt')[0]
        context.update({'last_order': last_order})
        return context


# class OrderHistoryListView(LoginRequiredMixin, ListView):
#     template_name = 'app_users/order_history.html'
#     context_object_name = 'order_history'
#
#     def get_queryset(self):
#         queryset = Orders.objects.filter(useridx=self.request.user)
#         return queryset
#
#
# class OrderHistoryDetailView(UserPassesTestMixin, DetailView):
#     model = Orders
#     template_name = 'app_users/order_history_item.html'
#     context_object_name = 'order'
#
#     def test_func(self):
#         return self.get_object().useridx == self.request.user


class LastViewedGoodsListView(LoginRequiredMixin, ListView):
    template_name = 'app_users/orders_list.html'
    context_object_name = 'last_viewed_goods'

    def get_queryset(self):
        queryset = get_browsing_history(self.request.COOKIES, 3)
        return queryset


class BrowsingHistoryListView(ListView):
    template_name = 'app_users/browsing_history.html'
    context_object_name = 'browsing_history'

    def get_queryset(self):
        queryset = get_browsing_history(self.request.COOKIES, 20)
        return queryset


class PersonalAccountView(LoginRequiredMixin, TemplateView):
    template_name = 'app_users/account.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        last_viewed = LastViewed(self.request)
        short_last_viewed = list()
        stop_value = 0
        for item in last_viewed:
            if stop_value == 3:
                break
            short_last_viewed.append(item)
            stop_value += 1
        context['short_last_viewed'] = short_last_viewed
        cart = Cart(self.request)
        context.update({'compare_count': len(Comparation(self.request))})
        context.update({'cart_count': len(cart)})
        context.update({'cart_cost': cart.total_cost()})
        context.update({'categories': get_categories()})
        context.update({'last_order': get_last_order(self.request.user.id)})
        return context


class ProfileView(TemplateView):
    template_name = 'app_users/profile.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cart = Cart(self.request)
        context.update({'user': self.request.user.profile})
        context.update({'compare_count': len(Comparation(self.request))})
        context.update({'cart_count': len(cart)})
        context.update({'cart_cost': cart.total_cost()})
        context.update({'categories': get_categories()})
        context.update({'last_order': get_last_order(self.request.user.id)})
        return context
