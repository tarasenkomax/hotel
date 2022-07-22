from django.test import TestCase
from Room.forms import ReviewForm


class ReviewFormTest(TestCase):

    def test_valid_form(self):
        """
        Вводим правильные данные
        Проверяем валидность формы
        """
        form_data = {'body': '1234567890', 'rating': 5}
        form = ReviewForm(data=form_data)
        self.assertTrue(form.is_valid())

    def test_not_valid_form(self):
        """
        Вводим большую строку в body (более 500 символов)
        Проверяем невалидность формы
        Проверяем сообщение об ошибке
        """
        string_more_than_500_characters = """
        1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
        1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
        1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
        1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
        1234567890123456789012345678901234567890123456789012345678901234567890123456789012345678901234567890
        """
        form_data = {'body': string_more_than_500_characters, 'rating': 5, }
        form = ReviewForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertEquals(form.errors['body'][0], 'Отзыв не должен превышать 500 символов')
