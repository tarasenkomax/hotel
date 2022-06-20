import re

from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _
from django import forms

from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser


class CleanNameUser:
    """ Миксин для валидации имени и фамилии пользователя """

    def clean_name(self):
        name = self.cleaned_data['name']
        if re.search(r'[.,:;!_*+()/#¤%&]', name):
            raise forms.ValidationError("Имя не должно содержать символы")
        if re.search(r'[0123456789]', name):
            raise forms.ValidationError("Имя не должно содержать цифры")
        if re.search(r'\s', name):
            raise forms.ValidationError("Имя не должно содержать пробелы")
        return name

    def clean_surname(self):
        surname = self.cleaned_data['surname']
        if re.search(r'[.,:;!_*+()/#¤%&]', surname):
            raise forms.ValidationError("Фамилия не должна содержать символы")
        if re.search(r'[0123456789]', surname):
            raise forms.ValidationError("Фамилия не должна содержать цифры")
        if re.search(r'\s', surname):
            raise forms.ValidationError("Фамилия не должна содержать пробелы")
        return surname


class CustomUserCreationForm(UserCreationForm, CleanNameUser):
    """ Форма создания пользователя """

    class Meta:
        model = CustomUser
        fields = ('email', 'surname', 'name', 'date_of_birth')
        error_messages = {'password_mismatch': _('Пароли не совпадают'), }

    password1 = forms.CharField(
        label=_("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
    )
    password2 = forms.CharField(
        label=_("Password confirmation"),
        widget=forms.PasswordInput(attrs={'autocomplete': 'new-password'}),
        strip=False,
    )


class UserSettingsForm(forms.ModelForm, CleanNameUser):
    """ Форма изменения личных данных пользователя """

    class Meta:
        model = CustomUser
        fields = ('surname',
                  'name',
                  'date_of_birth',
                  'phone',
                  'photo')


class AuthenticationUserForm(AuthenticationForm):
    """ Форма авторизации пользователя """
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))

    error_messages = {
        'invalid_login': _(
            "Не нашлось совпадений логина и пароля"
        ),
        'inactive': _(
            "Этот аккаунт не активен."
        ),
    }
