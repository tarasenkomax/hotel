from django.test import TestCase

from Account.models import CustomUser


class CustomUserModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        CustomUser.objects.create(first_name='Иван', last_name='Иванов', phone='8-000-000-00-00', email='test@test.ru')

    def test_object_name(self):
        user = CustomUser.objects.get(id=1)
        self.assertEquals(user.__str__(), 'Иванов Иван')
