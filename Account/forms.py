import re

from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext_lazy as _
from django import forms

from django_registration.forms import RegistrationForm

from .models import CustomUser


class CleanNameUserMixin:
    """ Миксин для валидации имени и фамилии пользователя """

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if re.search(r'[.,:;!_*+()/#¤%&]', first_name):
            raise forms.ValidationError("Имя не должно содержать символы")
        if re.search(r'[0123456789]', first_name):
            raise forms.ValidationError("Имя не должно содержать цифры")
        if re.search(r'\s', first_name):
            raise forms.ValidationError("Имя не должно содержать пробелы")
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if re.search(r'[.,:;!_*+()/#¤%&]', last_name):
            raise forms.ValidationError("Фамилия не должна содержать символы")
        if re.search(r'[0123456789]', last_name):
            raise forms.ValidationError("Фамилия не должна содержать цифры")
        if re.search(r'\s', last_name):
            raise forms.ValidationError("Фамилия не должна содержать пробелы")
        return last_name


class CustomUserCreationForm(RegistrationForm, CleanNameUserMixin):
    """ Форма создания пользователя """

    class Meta(RegistrationForm.Meta):
        model = CustomUser
        fields = ('email', 'last_name', 'first_name', 'date_of_birth')
        error_messages = {'password_mismatch': _('Введенные пароли не совпадают.'), }

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


class UserSettingsForm(forms.ModelForm, CleanNameUserMixin):
    """ Форма изменения личных данных пользователя """

    class Meta:
        model = CustomUser
        fields = ('last_name', 'first_name', 'date_of_birth', 'phone', 'photo')

    def clean_phone(self):
        phone = self.cleaned_data['phone']
        if re.search(r'[a-zA-Zа-яА-ЯёЁ]', phone):
            raise forms.ValidationError("Телефон не должен содержать букв")
        return phone


class AuthenticationUserForm(AuthenticationForm):
    """ Форма авторизации пользователя """
    username = UsernameField(widget=forms.TextInput(attrs={'autofocus': True}))

    error_messages = {'invalid_login': _("Не нашлось совпадений почты и пароля"),
                      'inactive': _("Этот аккаунт не активен.")}
