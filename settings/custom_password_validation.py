import re

from django.core.exceptions import ValidationError

from django.utils.translation import gettext as _, ngettext


class MinimumLengthValidator:
    """ Проверка минимальной длины пароля """

    def __init__(self, min_length=8):
        self.min_length = min_length

    def validate(self, password, user=None):
        if len(password) < self.min_length:
            raise ValidationError(ngettext(
                f"Этот пароль слишком короткий. Он должен содержать не менее {self.min_length} символа.",
                f"Этот пароль слишком короткий. Он должен содержать не менее {self.min_length} символов.",
                self.min_length), code='password_too_short', params={'min_length': self.min_length})


class MaximumLengthValidator:
    """ Проверка максимальной длины пароля """

    def __init__(self, max_length=20):
        self.max_length = max_length

    def validate(self, password, user=None):
        if len(password) > self.max_length:
            raise ValidationError(ngettext(
                f"Этот пароль слишком длинный. Он должен содержать не более {self.max_length} символа.",
                f"Этот пароль слишком длинный. Он должен содержать не более {self.max_length} символов.",
                self.max_length), code='password_too_short', params={'max_length': self.max_length})


class NumericPasswordValidator:
    """ Проверка в пароле наличия цифр и букв (верхнего и нижнего регистра) """

    def validate(self, password, user=None):
        if password.isdigit():
            raise ValidationError(_("Этот пароль полностью числовой."), code='password_entirely_numeric')
        if password.isalpha():
            raise ValidationError(_("Этот пароль полностью буквенный."), code='password_entirely_alphabetic')

        if not re.search(r'\w[a-z]', password):
            raise ValidationError(_("Пароль  должен содержать хотя бы одну маленькую букву"), code='only_big_register')
        if not re.search(r'\w[A-Z]', password):
            raise ValidationError(_("Пароль  должен содержать хотя бы одну большую букву"), code='only_small_register')


class SpecialCharactersPasswordValidator:
    """ Проверка на наличие в пароле спецсимволов """

    def validate(self, password, user=None):
        if re.search(r'[- .,:;!_*+()/#¤<>%&]', password):
            raise ValidationError(_("Пароль содержит недопустимый символ.(- .,:;!_*+()/#¤<>%&)"),
                                  code='password_special_characters', )
