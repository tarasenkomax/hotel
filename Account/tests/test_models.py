from django.contrib.auth import get_user_model
from django.test import TestCase

from Account.models import CustomUser


class CustomUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        user = get_user_model().objects.create_user(email='test@test.ru', password='Some_password123',
                                                    first_name='Иван', last_name='Иванов', phone='8-000-000-00-00')

    def test_object_name(self):
        user = CustomUser.objects.get(email='test@test.ru')
        self.assertEquals(user.__str__(), 'Иванов Иван')
