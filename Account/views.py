from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic
import datetime as DT

from django.views.generic import DetailView, UpdateView

from Account.forms import CustomUserCreationForm, UserSettingsForm
from Account.models import CustomUser
from Room.reserve_functions import dates_of_user


class Account(LoginRequiredMixin, DetailView):
    """ ЛК пользователя """
    model = CustomUser
    template_name = "profile/account.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, email=self.request.user.email)


class SignUp(generic.CreateView):
    """ Регистрация """
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        """ Автоматический вход в систему после регистрации """
        view = super(SignUp, self).form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        user = authenticate(username=email, password=password)
        login(self.request, user)
        return view


class AccountSetting(LoginRequiredMixin, UpdateView):
    """ Настройки ЛК пользователя """
    form_class = UserSettingsForm
    template_name = 'profile/account_settings.html'
    success_url = reverse_lazy('account')

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, email=self.request.user.email)


@login_required(login_url="login")
def home(request):
    """ Домашняя страница """
    error = ''
    if request.method == 'POST':
        if request.POST['day_in'] and request.POST['day_out'] and request.POST['number_of_guests']:
            day_in = DT.datetime.strptime(request.POST['day_in'], '%d.%m.%Y').date()
            day_out = DT.datetime.strptime(request.POST['day_out'], '%d.%m.%Y').date()
            number_of_guests = int(request.POST['number_of_guests'][0])
            if dates_of_user(request.user, day_in, day_out):
                return redirect(f'/list_free_rooms?day_in={day_in}&day_out={day_out}&number_of_guests={number_of_guests}')
            else:
                error = 'У вас есть бронь пересекающаяся с выбранными датами'
        else:
            error = 'Пожалуйста заполните все поля формы'
    return render(request, 'home.html', {'error': error})
