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


class LoginView(views.LoginView):
    template_name = 'app_users/login.html'


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
            profile.useridx = User.objects.get(id=user.id)
            profile.save()
            username = user_form.cleaned_data.get('username')
            password = user_form.cleaned_data.get('password1')
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


class OrderHistoryListView(LoginRequiredMixin, ListView):
    template_name = 'app_users/order_history.html'
    context_object_name = 'order_history'

    def get_queryset(self):
        queryset = Orders.objects.filter(useridx=self.request.user)
        return queryset


class OrderHistoryDetailView(UserPassesTestMixin, DetailView):
    model = Orders
    template_name = 'app_users/order_history_item.html'
    context_object_name = 'order'

    def test_func(self):
        return self.get_object().useridx == self.request.user


class LastViewedGoodsListView(LoginRequiredMixin, ListView):
    template_name = 'app_users/last_viewed_goods.html'
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
    template_name = 'app_users/personal_account.html'
