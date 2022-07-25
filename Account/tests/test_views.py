from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

from Account.models import CustomUser


class AccountViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(email='test@test.ru', password='Some_password123',
                                                    first_name='Иван', last_name='Иванов', phone='8-000-000-00-00')

    def test_redirect_if_not_logged_in(self):
        """ Проверяет, что не авторизованного пользователя редиректит на страницу авторизации"""
        resp = self.client.get(reverse('account'))
        self.assertRedirects(resp, f'/login?next=/account/')

    def test_logged_in_uses_correct_email(self):
        """
        Проверяет почту авторизованного пользователя в контексте ответа
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        resp = self.client.get(reverse('account'))
        self.assertEqual(str(resp.context['user'].email), 'test@test.ru')
        self.assertEqual(resp.status_code, 200)

    def test_logged_in_uses_correct_generate_url(self):
        """
        Проверяет код ответа по сгенерированному урлу
        Проверяет что используется правильный шаблон
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        resp = self.client.get(reverse('account'))
        self.assertEqual(str(resp.context['user'].email), 'test@test.ru')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "profile/account.html")

    def test_view_url_exists_at_desired_location(self):
        """
        Проверяет код ответа по указанному урлу
        Проверяет что используется правильный шаблон
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        resp = self.client.get('/account/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "profile/account.html")

    def test_context(self):
        """
        Проверяет наличие ключа 'user' и его значение в контексте ответа
        """
        user = CustomUser.objects.get(email='test@test.ru')
        self.client.login(email='test@test.ru', password='Some_password123')
        resp = self.client.get('/account/')
        self.assertTrue('user' in resp.context)
        self.assertEqual(resp.context['user'], user)


class AccountSettingsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(email='test@test.ru', password='Some_password123',
                                                    first_name='Иван', last_name='Иванов', phone='8-000-000-00-00')

    def test_redirect_if_not_logged_in(self):
        """ Проверяет, что не авторизованного пользователя редиректит на страницу авторизации"""
        resp = self.client.get(reverse('account_settings'))
        self.assertRedirects(resp, f'/login?next=/account_settings/')

    def test_logged_in_uses_correct_email(self):
        """
        Проверяет почту авторизованного пользователя в контексте ответа
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        resp = self.client.get(reverse('account_settings'))
        self.assertEqual(str(resp.context['user'].email), 'test@test.ru')
        self.assertEqual(resp.status_code, 200)

    def test_logged_in_uses_correct_generate_url(self):
        """
        Проверяет код ответа по сгенерированному урлу
        Проверяет что используется правильный шаблон
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        resp = self.client.get(reverse('account_settings'))
        self.assertEqual(str(resp.context['user'].email), 'test@test.ru')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "profile/account_settings.html")

    def test_view_url_exists_at_desired_location(self):
        """
        Проверяет код ответа по указанному урлу
        Проверяет что используется правильный шаблон
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        resp = self.client.get('/account_settings/')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "profile/account_settings.html")

    def test_update_data(self):
        """
        Проверка изменения имени после post запроса
        Проверка кода ответа после post запроса (302)
        Проверка урла для редиректа
        """
        user = CustomUser.objects.get(email='test@test.ru')
        self.client.login(email='test@test.ru', password='Some_password123')
        self.assertEqual(user.first_name, 'Иван')
        resp = self.client.post('/account_settings/',
                                data={'first_name': 'Игорь', 'last_name': 'Иванов', 'phone': '8-000-000-00-00'})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/account/'))
        user = CustomUser.objects.get(email='test@test.ru')
        self.assertEqual(user.first_name, 'Игорь')
