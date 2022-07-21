import datetime

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View

from django.views.generic import DetailView, UpdateView, CreateView
from django_registration.backends.activation.views import RegistrationView

from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings

from Account.forms import CustomUserCreationForm, UserSettingsForm
from Account.models import CustomUser
from Room.utils import check_dates_of_user


class Account(LoginRequiredMixin, DetailView):
    """ ЛК пользователя """
    model = CustomUser
    template_name = "profile/account.html"
    context_object_name = "user"

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, email=self.request.user.email)


class SignUpOneStepActivation(CreateView):
    """ Регистрация без подтверждения аккаунта по электронной почте"""
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('home')
    template_name = 'registration/signup.html'

    def form_valid(self, form):
        """ Автоматический вход в систему после регистрации """
        view = super(SignUpOneStepActivation, self).form_valid(form)
        email, password = form.cleaned_data.get('email'), form.cleaned_data.get('password1')
        user = authenticate(username=email, password=password)
        login(self.request, user)
        return view


class SignUpTwoStepActivation(RegistrationView):
    """ Регистрация с подтверждением аккаунта по электронной почте"""
    email_body_template = "django_registration/activation_email_body.html"
    form_class = CustomUserCreationForm
    template_name = 'registration/signup.html'

    def send_activation_email(self, user):
        activation_key = self.get_activation_key(user)
        context = self.get_email_context(activation_key)
        context["user"] = user
        subject = render_to_string(template_name=self.email_subject_template, context=context, request=self.request)
        subject = "".join(subject.splitlines())
        message = render_to_string(template_name=self.email_body_template, context=context, request=self.request)

        msg = EmailMultiAlternatives(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
        msg.attach_alternative(message, "text/html")
        msg.send()


class AccountSetting(LoginRequiredMixin, UpdateView):
    """ Настройки ЛК пользователя """
    form_class = UserSettingsForm
    template_name = 'profile/account_settings.html'
    success_url = reverse_lazy('account')

    def get_object(self, queryset=None):
        return get_object_or_404(CustomUser, email=self.request.user.email)


class Home(LoginRequiredMixin, View):
    """ Домашняя страница """

    def __init__(self):
        super().__init__()
        self.error = ''

    def get(self, request, *args, **kwargs):
        return render(self.request, 'home.html', {'error': self.error})

    def post(self, request, *args, **kwargs):
        if self.request.POST['day_in'] and self.request.POST['day_out'] and self.request.POST['number_of_guests']:
            day_in = datetime.datetime.strptime(self.request.POST['day_in'], '%d.%m.%Y').date()
            day_out = datetime.datetime.strptime(self.request.POST['day_out'], '%d.%m.%Y').date()
            number_of_guests = int(self.request.POST['number_of_guests'][0])
            if check_dates_of_user(self.request.user, day_in, day_out):
                return redirect(
                    f'/list_free_rooms?day_in={day_in}&day_out={day_out}&number_of_guests={number_of_guests}')
            else:
                self.error = 'У вас есть бронь пересекающаяся с выбранными датами'
        else:
            self.error = 'Пожалуйста заполните все поля формы'
        return self.get(self, request, *args, **kwargs)
