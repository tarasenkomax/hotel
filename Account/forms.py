from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _
from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'name', 'surname', 'date_of_birth')  # TODO настроить инпут даты


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('name',
                  'surname',
                  'date_of_birth',
                  'phone',
                  'photo')


class AuthenticationUserForm(AuthenticationForm):
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))

    error_messages = {
        'invalid_login': _(
            "Не нашлось совпадений логина и пароля"
        ),
        'inactive': _(
            "Этот аккаунт не активен."
        ),
    }
