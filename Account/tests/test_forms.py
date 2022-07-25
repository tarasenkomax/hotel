from django.contrib.auth import get_user_model
from django.test import TestCase

from Account.forms import CustomUserCreationForm, AuthenticationUserForm, UserSettingsForm


class CustomUserCreationFormTest(TestCase):
    """ Тестирование формы создания пользователя """
    good_pass = '123456789Aa'
    invert_pass = 'aA987654321'
    is_digit_pass = '123456789'
    short_pass = '123Aa'
    long_pass = '0123456789123456789Aa'
    special_pass = '123Aa+()/#¤<>%&)'
    small_letter_pass = '123456789a'
    big_letter_pass = '123456789A'

    def test_valid_form(self):
        """
        Вводим правильные данные
        Проверяем валидность формы
        """
        form_data = {'email': 'test@test.ru', 'last_name': '', 'first_name': 'Иван',
                     'date_of_birth': '1995-09-12', 'password1': self.good_pass, 'password2': self.good_pass}
        form = CustomUserCreationForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_different_passwords_form(self):
        """
        Вводим разные пароли
        Проверяем валидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'email': 'test@test.ru', 'last_name': 'Иванов', 'first_name': 'Иван',
                     'date_of_birth': '1995-09-12', 'password1': self.good_pass, 'password2': self.invert_pass}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['password2'][0], 'Введенные пароли не совпадают.')

    def test_numeric_passwords_form(self):
        """
        Вводим числовой пароль
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'email': 'test@test.ru', 'last_name': 'Иванов', 'first_name': 'Иван',
                     'date_of_birth': '1995-09-12', 'password1': self.is_digit_pass, 'password2': self.is_digit_pass}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['password2'][0], 'Этот пароль полностью числовой.')

    def test_letter_passwords_form(self):
        """
        Вводим буквенный пароль
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'email': 'test@test.ru', 'last_name': 'Иванов', 'first_name': 'Иван',
                     'date_of_birth': '1995-09-12', 'password1': 'Qwertyuiop', 'password2': 'Qwertyuiop'}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['password2'][0], 'Этот пароль полностью буквенный.')

    def test_short_passwords_form(self):
        """
        Вводим короткий пароль (меньше 8 символов)
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'email': 'test@test.ru', 'last_name': 'Иванов', 'first_name': 'Иван',
                     'date_of_birth': '1995-09-12', 'password1': self.short_pass, 'password2': self.short_pass}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['password2'][0],
                          'Этот пароль слишком короткий. Он должен содержать не менее 8 символов.')

    def test_long_passwords_form(self):
        """
        Вводим длинный пароль (более 20 символов)
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'email': 'test@test.ru', 'last_name': 'Иванов', 'first_name': 'Иван',
                     'date_of_birth': '1995-09-12', 'password1': self.long_pass, 'password2': self.long_pass}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['password2'][0],
                          'Этот пароль слишком длинный. Он должен содержать не более 20 символов.')

    def test_special_passwords_form(self):
        """
        Вводим пароль со спецсимволами (- .,:;!_*+()/#¤<>%&)
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'email': 'test@test.ru', 'last_name': 'Иванов', 'first_name': 'Иван',
                     'date_of_birth': '1995-09-12', 'password1': self.special_pass,
                     'password2': self.special_pass}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['password2'][0], 'Пароль содержит недопустимый символ.(- .,:;!_*+()/#¤<>%&)')

    def test_small_letter_passwords_form(self):
        """
        Вводим пароль без больших букв
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'email': 'test@test.ru', 'last_name': 'Иванов', 'first_name': 'Иван',
                     'date_of_birth': '1995-09-12', 'password1': self.small_letter_pass,
                     'password2': self.small_letter_pass}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['password2'][0], 'Пароль  должен содержать хотя бы одну большую букву')

    def test_big_letter_passwords_form(self):
        """
        Вводим пароль без маленьких букв
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'email': 'test@test.ru', 'last_name': 'Иванов', 'first_name': 'Иван',
                     'date_of_birth': '1995-09-12', 'password1': self.big_letter_pass,
                     'password2': self.big_letter_pass}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['password2'][0], 'Пароль  должен содержать хотя бы одну маленькую букву')

    def test_invalid_email_form(self):
        """
        Вводим некорректный адрес электронной почты
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'email': 'invalid_email.ru', 'last_name': 'Иванов', 'first_name': 'Иван',
                     'date_of_birth': '1995-09-12', 'password1': self.good_pass, 'password2': self.good_pass}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['email'][0], 'Введите правильный адрес электронной почты.')

    def test_invalid_date_of_birth_form(self):
        """
        Вводим некорректную дату
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'email': 'test@test.ru', 'last_name': 'Иванов', 'first_name': 'Иван',
                     'date_of_birth': '192', 'password1': self.good_pass, 'password2': self.good_pass}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['date_of_birth'][0], 'Введите правильную дату.')

    def test_symbols_in_first_name_form(self):
        """
        Вводим имя со спецсимволами (- .,:;!_*+()/#¤<>%&)
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'email': 'test@test.ru', 'last_name': 'Иванов', 'first_name': 'Иван_*+()',
                     'date_of_birth': '1995-09-12', 'password1': self.good_pass, 'password2': self.good_pass}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['first_name'][0], 'Имя не должно содержать символы')

    def test_digit_in_first_name_form(self):
        """
        Вводим имя с цифрами
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'email': 'test@test.ru', 'last_name': 'Иванов', 'first_name': 'Иван1',
                     'date_of_birth': '1995-09-12', 'password1': self.good_pass, 'password2': self.good_pass}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['first_name'][0], 'Имя не должно содержать цифры')

    def test_space_in_first_name_form(self):
        """
        Вводим имя с пробелами
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'email': 'test@test.ru', 'last_name': 'Иванов', 'first_name': 'Ив ан',
                     'date_of_birth': '1995-09-12', 'password1': self.good_pass, 'password2': self.good_pass}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['first_name'][0], 'Имя не должно содержать пробелы')

    def test_symbols_in_last_name_form(self):
        """
        Вводим фамилию со спецсимволами (- .,:;!_*+()/#¤<>%&)
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'email': 'test@test.ru', 'last_name': 'Иванов_*+()', 'first_name': 'Иван',
                     'date_of_birth': '1995-09-12', 'password1': self.good_pass, 'password2': self.good_pass}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['last_name'][0], 'Фамилия не должна содержать символы')

    def test_digit_in_last_name_form(self):
        """
        Вводим фамилию с цифрами
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'email': 'test@test.ru', 'last_name': 'Иванов1', 'first_name': 'Иван',
                     'date_of_birth': '1995-09-12', 'password1': self.good_pass, 'password2': self.good_pass}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['last_name'][0], 'Фамилия не должна содержать цифры')

    def test_space_in_last_name_form(self):
        """
        Вводим фамилию с пробелами
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'email': 'test@test.ru', 'last_name': 'Ива нов', 'first_name': 'Иван',
                     'date_of_birth': '1995-09-12', 'password1': self.good_pass, 'password2': self.good_pass}
        form = CustomUserCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['last_name'][0], 'Фамилия не должна содержать пробелы')


class UserSettingsFormTest(TestCase):
    """ Тестирование формы изменения личных данных пользователя """

    def test_valid_form(self):
        """
        Вводим правильные данные
        Проверяем валидность формы
        """
        form_data = {'last_name': 'Иванов', 'first_name': 'Иван', 'date_of_birth': '1995-09-12',
                     'phone': '8-900-000-00-00'}
        form = UserSettingsForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_invalid_phone_form(self):
        """
        Вводим некорректный телефон (с буквами)
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'last_name': 'Иванов', 'first_name': 'Иван', 'date_of_birth': '192', 'phone': '8-900-0Abc'}
        form = UserSettingsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['phone'][0], 'Телефон не должен содержать букв')

    def test_invalid_date_of_birth_form(self):
        """
        Вводим некорректную дату
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'last_name': 'Иванов', 'first_name': 'Иван', 'date_of_birth': '192', 'phone': '8-900-000-00-00'}
        form = UserSettingsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['date_of_birth'][0], 'Введите правильную дату.')

    def test_symbols_in_first_name_form(self):
        """
        Вводим имя со спецсимволами (- .,:;!_*+()/#¤<>%&)
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'last_name': 'Иванов', 'first_name': 'Иван_*+()', 'date_of_birth': '1995-09-12',
                     'phone': '8-900-000-00-00'}
        form = UserSettingsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['first_name'][0], 'Имя не должно содержать символы')

    def test_digit_in_first_name_form(self):
        """
        Вводим имя с цифрами
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'last_name': 'Иванов', 'first_name': 'Иван1', 'date_of_birth': '1995-09-12',
                     'phone': '8-900-000-00-00'}
        form = UserSettingsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['first_name'][0], 'Имя не должно содержать цифры')

    def test_space_in_first_name_form(self):
        """
        Вводим имя с пробелами
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'email': 'test@test.ru', 'last_name': 'Иванов', 'first_name': 'Ив ан',
                     'date_of_birth': '1995-09-12', 'phone': '8-900-000-00-00'}
        form = UserSettingsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['first_name'][0], 'Имя не должно содержать пробелы')

    def test_symbols_in_last_name_form(self):
        """
        Вводим фамилию со спецсимволами (- .,:;!_*+()/#¤<>%&)
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'last_name': 'Иванов_*+()', 'first_name': 'Иван', 'date_of_birth': '1995-09-12',
                     'phone': '8-900-000-00-00'}
        form = UserSettingsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['last_name'][0], 'Фамилия не должна содержать символы')

    def test_digit_in_last_name_form(self):
        """
        Вводим фамилию с цифрами
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'last_name': 'Иванов1', 'first_name': 'Иван', 'date_of_birth': '1995-09-12',
                     'phone': '8-900-000-00-00'}
        form = UserSettingsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['last_name'][0], 'Фамилия не должна содержать цифры')

    def test_space_in_last_name_form(self):
        """
        Вводим фамилию с пробелами
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'last_name': 'Ива нов', 'first_name': 'Иван', 'date_of_birth': '1995-09-12',
                     'phone': '8-900-000-00-00'}
        form = UserSettingsForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['last_name'][0], 'Фамилия не должна содержать пробелы')


class AuthenticationUserFormTest(TestCase):
    """ Тестирование формы авторизации пользователя """

    def test_user_exist_form(self):
        """
        Вводим данные для входа
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        user = get_user_model().objects.create_user(email='test@test.ru', password='Some_password123')
        form_data = {'username': 'test@test.ru', 'password': 'Some_password123', }
        form = AuthenticationUserForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_user_not_exist_form(self):
        """
        Вводим данные для входа в аккаунт несуществующего пользователя
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        form_data = {'username': 'test@test.ru', 'password': 'Some_password123', }
        form = AuthenticationUserForm(data=form_data)
        self.assertEquals(form.errors['__all__'][0], 'Не нашлось совпадений почты и пароля')
        self.assertFalse(form.is_valid())
