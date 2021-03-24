import re

from django.contrib.auth.forms import AuthenticationForm, UsernameField
from django.utils.translation import gettext, gettext_lazy as _
from django import forms

from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('email', 'surname', 'name', 'patronymic', 'date_of_birth')

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

    def clean_patronymic(self):
        patronymic = self.cleaned_data['patronymic']
        if re.search(r'[.,:;!_*+()/#¤%&]', patronymic):
            raise forms.ValidationError("Отчество не должно содержать символы")
        if re.search(r'[0123456789]', patronymic):
            raise forms.ValidationError("Отчество не должно содержать цифры")
        if re.search(r'\s', patronymic):
            raise forms.ValidationError("Отчество не должно содержать пробелы")
        return patronymic


class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ('email',)


class UserSettingsForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('surname',
                  'name',
                  'patronymic',
                  'date_of_birth',
                  'phone',
                  'photo')

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

    def clean_patronymic(self):
        patronymic = self.cleaned_data['patronymic']
        if re.search(r'[.,:;!_*+()/#¤%&]', patronymic):
            raise forms.ValidationError("Отчество не должно содержать символы")
        if re.search(r'[0123456789]', patronymic):
            raise forms.ValidationError("Отчество не должно содержать цифры")
        if re.search(r'\s', patronymic):
            raise forms.ValidationError("Отчество не должно содержать пробелы")
        return patronymic


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
