import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase

from django.urls import reverse

from Account.models import CustomUser
from Room.models import Room, Hotel, TypeRoom, Reserve, Review, Regulations


class AllRoomsViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        hotel = Hotel.objects.create(name='Test hotel name')
        type_room = TypeRoom.objects.create(code=1, nomination='Эконом', description='Дешевый номер')
        for number in range(10):
            Room.objects.create(hotel=hotel, number=number, type=type_room, price=1000)

    def test_view_url_exists_at_desired_location(self):
        """ Проверяет код ответа по заданному урлу """
        resp = self.client.get('/all_rooms')
        self.assertEqual(resp.status_code, 200)

    def test_view_url_accessible_by_name(self):
        """ Проверяет код ответа по сгенерированному урлу """
        resp = self.client.get(reverse('all_rooms'))
        self.assertEqual(resp.status_code, 200)

    def test_view_uses_correct_template(self):
        """ Проверяет что используется правильный шаблон """
        resp = self.client.get(reverse('all_rooms'))
        self.assertTemplateUsed(resp, "rooms/all_rooms.html")

    def test_pagination_is_six(self):
        """
        Проверяет наличие ключа 'is_paginated' в контексте овтета
        Проверяет истиность значения 'is_paginated' в контексте ответа
        Проверяет длину списка объектов на первой странице пагинации
        """
        resp = self.client.get(reverse('all_rooms'))
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['rooms']) == 6)

    def test_lists_all_rooms(self):
        """
        Проверяет код ответа по заданому урлу (вторая страница пагинации)
        Проверяет наличие ключа 'is_paginated' в контексте овтета
        Проверяет истиность значения 'is_paginated' в контексте ответа
        Проверяет длину списка объектов на второй странице пагинации
        """
        resp = self.client.get(reverse('all_rooms') + '?page=2')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['rooms']) == 4)


class AllReservesViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        type_room = TypeRoom.objects.create(code=1, nomination='Эконом', description='Дешевый номер')
        hotel = Hotel.objects.create(name='Test hotel name')
        room = Room.objects.create(hotel=hotel, number=101, type=type_room, price=1000, number_of_guests=5)
        user = get_user_model().objects.create_user(email='test@test.ru', password='Some_password123',
                                                    first_name='Иван', last_name='Иванов', phone='8-000-000-00-00')

    def test_redirect_if_not_logged_in(self):
        """ Проверяет, что не авторизованного пользователя редиректит на страницу авторизации"""
        resp = self.client.get(reverse('all_reserves'))
        self.assertRedirects(resp, '/login?next=/all_reserves')

    def test_logged_in_uses_correct_template(self):
        """
        Проверяет почту авторизованного пользователя в контексте ответа
        Проверяет код ответа по заданому урлу
        Проверяет что используется правильный шаблон
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        resp = self.client.get(reverse('all_reserves'))
        self.assertEqual(str(resp.context['user'].email), 'test@test.ru')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "rooms/all_reserves.html")

    def test_list_reserves_to_user(self):
        """
        Проверяет почту авторизованного пользователя в контексте ответа
        Проверяет код ответа по заданому урлу
        Проверяет наличие ключа 'reserve_list' в контексте ответа
        Проверяет, что изначально у пользователя нет резервов
        Проверяет, что после создания резервов они отображаются у пользователя
        Проверяет, что список резервов отсортирован по id
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        resp = self.client.get(reverse('all_reserves'))
        self.assertEqual(str(resp.context['user'].email), 'test@test.ru')
        self.assertEqual(resp.status_code, 200)
        self.assertTrue('reserve_list' in resp.context)
        self.assertEqual(len(resp.context['reserve_list']), 0)
        user = CustomUser.objects.get(email='test@test.ru')
        room = Room.objects.get(number=101)
        reserve1 = Reserve.objects.create(client=user, room=room, day_in='2022-09-17', day_out='2022-09-19',
                                          number_of_guests=2, id=1)
        reserve2 = Reserve.objects.create(client=user, room=room, day_in='2022-09-25', day_out='2022-09-26',
                                          number_of_guests=3, id=2)
        reserve3 = Reserve.objects.create(client=user, room=room, day_in='2022-09-27', day_out='2022-09-28',
                                          number_of_guests=3, id=3)
        resp = self.client.get(reverse('all_reserves'))
        self.assertEqual(len(resp.context['reserve_list']), 3)
        self.assertEqual(resp.status_code, 200)
        self.assertEqual(resp.context['reserve_list'][0], reserve3)


class DetailRoomViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        type_room = TypeRoom.objects.create(code=1, nomination='Эконом', description='Дешевый номер')
        hotel = Hotel.objects.create(name='Test hotel name')
        room = Room.objects.create(hotel=hotel, number=101, type=type_room, price=1000, number_of_guests=5)
        user = get_user_model().objects.create_user(email='test@test.ru', password='Some_password123',
                                                    first_name='Иван', last_name='Иванов', phone='8-000-000-00-00')
        reserve1 = Reserve.objects.create(client=user, room=room, day_in='2022-09-17', day_out='2022-09-19',
                                          number_of_guests=2)
        reserve2 = Reserve.objects.create(client=user, room=room, day_in='2022-09-25', day_out='2022-09-26',
                                          number_of_guests=3)
        review1 = Review.objects.create(room=room, rating=3, body='1234', author=user, reserve=reserve1)
        review2 = Review.objects.create(room=room, rating=2, body='1234', author=user, reserve=reserve2)

        regulation1 = Regulations.objects.create(type_room=room.type, regulation='Не курить')
        regulation2 = Regulations.objects.create(type_room=room.type, regulation='Без домашних животных')

    def test_view_url_exists_at_desired_location(self):
        """
        Проверяет код ответа по заданому урлу
        Проверяет что используется правильный шаблон
        """
        room = Room.objects.get(number=101)
        resp = self.client.get(f'/room/{room.number}')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'rooms/detail_room.html')

    def test_view_url_accessible_by_name(self):
        """
        Проверяет код ответа по сгенерированному урлу
        Проверяет что используется правильный шаблон
        """
        room = Room.objects.get(number=101)
        resp = self.client.get(reverse('detail_room', kwargs={'number': room.number}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'rooms/detail_room.html')

    def test_context_data(self):
        """
        Проверяет в контексте наличие ключей 'regulations_list', 'review_list','num_of_review'
        Проверяет количество правил команты'
        Проверяет количество отзывов команты'
        """
        room = Room.objects.get(number=101)
        resp = self.client.get(reverse('detail_room', kwargs={'number': room.number}))
        self.assertTrue('regulations_list' in resp.context)
        self.assertTrue('review_list' in resp.context)
        self.assertTrue('num_of_review' in resp.context)
        self.assertEqual(len(resp.context['regulations_list']), 2)
        self.assertEqual(len(resp.context['review_list']), 2)
        self.assertEqual(resp.context['num_of_review'], 2)


class AddReviewViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        type_room = TypeRoom.objects.create(code=2, nomination='Стандарт', description='Стандартный номер')
        hotel = Hotel.objects.create(name='Test hotel name')
        user1 = get_user_model().objects.create_user(email='test@test.ru', password='Some_password123',
                                                     first_name='Иван', last_name='Иванов', phone='8-000-000-00-00')
        user2 = get_user_model().objects.create_user(email='test2@test.ru', password='Some_password123',
                                                     first_name='Петр', last_name='Петров', phone='8-000-000-00-11')
        room = Room.objects.create(hotel=hotel, number=102, type=type_room, price=700, number_of_guests=6)
        reserve = Reserve.objects.create(client=user2, room=room, day_in='2022-09-27', day_out='2022-09-28',
                                         number_of_guests=3)

    def test_view_url_exists_at_desired_location(self):
        """
        Проверяет код ответа по указанному урлу
        Проверяет что используется правильный шаблон
        """
        self.client.login(email='test2@test.ru', password='Some_password123')
        user = CustomUser.objects.get(email='test2@test.ru')
        reserve = Reserve.objects.get(client=user)
        resp = self.client.get(f'/add_review/{reserve.pk}')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'rooms/add_review.html')

    def test_view_url_accessible_by_name(self):
        """
        Проверяет код ответа по сгенерированному урлу
        Проверяет что используется правильный шаблон
        """
        self.client.login(email='test2@test.ru', password='Some_password123')
        user = CustomUser.objects.get(email='test2@test.ru')
        reserve = Reserve.objects.get(client=user)
        resp = self.client.get(reverse('add_review', kwargs={'pk': reserve.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, 'rooms/add_review.html')

    def test_context_data(self):
        """ Проверяет в контексте наличие ключей 'day_in', 'day_out','room_reserve' и их значения """
        self.client.login(email='test2@test.ru', password='Some_password123')
        user = CustomUser.objects.get(email='test2@test.ru')
        reserve = Reserve.objects.get(client=user)
        resp = self.client.get(f'/add_review/{reserve.pk}')
        self.assertTrue('day_in' in resp.context)
        self.assertTrue('day_out' in resp.context)
        self.assertTrue('room_reserve' in resp.context)
        self.assertEqual(resp.context['day_in'], datetime.date(2022, 9, 27))
        self.assertEqual(resp.context['day_out'], datetime.date(2022, 9, 28))
        self.assertEqual(resp.context['room_reserve'].number, 102)

    def test_permission_denied(self):
        """
        Проверка кода ответа в случае запроса к старнице пользователя, которому не принадлежит резерв (404)
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        user = CustomUser.objects.get(email='test2@test.ru')
        reserve = Reserve.objects.get(client=user)
        resp = self.client.get(reverse('add_review', kwargs={'pk': reserve.pk}))
        self.assertEqual(resp.status_code, 404)

    def test_permission_allowed(self):
        """
        Проверка кода ответа в случае запроса к старнице пользователя, которому  принадлежит резерв (200)
        """
        self.client.login(email='test2@test.ru', password='Some_password123')
        user = CustomUser.objects.get(email='test2@test.ru')
        reserve = Reserve.objects.get(client=user)
        resp = self.client.get(reverse('add_review', kwargs={'pk': reserve.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_post_request(self):
        """
        Проверка что после валидного post запроса добавляется объект Отзыва
        Проверка кода ответа при успешном post запросе (302)
        Проверка урла для редиректа
        """
        self.client.login(email='test2@test.ru', password='Some_password123')
        user = CustomUser.objects.get(email='test2@test.ru')
        reserve = Reserve.objects.get(client=user)
        resp = self.client.post(reverse('add_review', kwargs={'pk': reserve.pk}), data={'body': 'тест111', 'rating': 4})
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(Review.objects.get(body='тест111'))
        self.assertTrue(resp.url.startswith('/all_reserves'))


class ReserveRoomViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        type_room = TypeRoom.objects.create(code=1, nomination='Эконом', description='Дешевый номер')
        hotel = Hotel.objects.create(name='Test hotel name')
        user1 = get_user_model().objects.create_user(email='test@test.ru', password='Some_password123',
                                                     first_name='Иван', last_name='Иванов', phone='8-000-000-00-00')
        user2 = get_user_model().objects.create_user(email='test2@test.ru', password='Some_password123',
                                                     first_name='Петр', last_name='Петров', phone='8-000-000-00-11')
        room = Room.objects.create(hotel=hotel, number=101, type=type_room, price=1000, number_of_guests=5)
        reserve1 = Reserve.objects.create(client=user1, room=room, day_in='2022-09-17', day_out='2022-09-19',
                                          number_of_guests=2)
        reserve2 = Reserve.objects.create(client=user1, room=room, day_in='2022-09-25', day_out='2022-09-26',
                                          number_of_guests=3)
        review1 = Review.objects.create(room=room, rating=3, body='1234', author=user1, reserve=reserve1)
        review2 = Review.objects.create(room=room, rating=2, body='1234', author=user1, reserve=reserve2)
        regulation1 = Regulations.objects.create(type_room=room.type, regulation='Не курить')
        regulation2 = Regulations.objects.create(type_room=room.type, regulation='Без домашних животных')

    def test_redirect_if_not_logged_in(self):
        """ Проверяет, что не авторизованного пользователя редиректит на страницу авторизации"""
        room = Room.objects.get(number=101)
        resp = self.client.get(reverse('reserve_room', kwargs={'number': room.number}))
        self.assertRedirects(resp, f'/login?next=/reserve_room/{room.number}')

    def test_logged_in_uses_correct_email(self):
        """
        Проверяет почту авторизованного пользователя в контексте ответа
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        room = Room.objects.get(number=101)
        resp = self.client.get(reverse('reserve_room', kwargs={'number': room.number}),
                               data={'day_in': '2022-09-17', 'day_out': '2022-09-19', 'number_of_guests': '3'})
        self.assertEqual(str(resp.context['user'].email), 'test@test.ru')
        self.assertEqual(resp.status_code, 200)

    def test_logged_in_uses_correct_generate_url(self):
        """
        Проверяет код ответа по сгенерированному урлу
        Проверяет что используется правильный шаблон
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        room = Room.objects.get(number=101)
        resp = self.client.get(reverse('reserve_room', kwargs={'number': room.number}),
                               data={'day_in': '2022-09-17', 'day_out': '2022-09-19', 'number_of_guests': '3'})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "rooms/reserve_room.html")

    def test_context_data(self):
        """ Проверяет в контексте наличие ключей 'regulations_list', 'review_list', 'num_of_review', 'day_in',
         'day_out', 'number_of_guests', 'days', 'full_price' и их значения
         """
        self.client.login(email='test@test.ru', password='Some_password123')
        room = Room.objects.get(number=101)
        resp = self.client.get(reverse('reserve_room', kwargs={'number': room.number}),
                               data={'day_in': '2022-09-17', 'day_out': '2022-09-19', 'number_of_guests': '3'})
        self.assertTrue('regulations_list' in resp.context)
        self.assertTrue('review_list' in resp.context)
        self.assertTrue('num_of_review' in resp.context)
        self.assertTrue('day_in' in resp.context)
        self.assertTrue('day_out' in resp.context)
        self.assertTrue('number_of_guests' in resp.context)
        self.assertTrue('days' in resp.context)
        self.assertTrue('full_price' in resp.context)
        self.assertEqual(len(resp.context['regulations_list']), 2)
        self.assertEqual(len(resp.context['review_list']), 2)
        self.assertEqual(resp.context['num_of_review'], 2)
        self.assertEqual(resp.context['day_in'], '2022-09-17')
        self.assertEqual(resp.context['day_out'], '2022-09-19')
        self.assertEqual(resp.context['number_of_guests'], '3')
        self.assertEqual(resp.context['days'], 2)
        self.assertEqual(resp.context['full_price'], 2000)


class CancelViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        type_room1 = TypeRoom.objects.create(code=1, nomination='Эконом', description='Дешевый номер')
        type_room2 = TypeRoom.objects.create(code=2, nomination='Стандарт', description='Стандартный номер')
        hotel = Hotel.objects.create(name='Test hotel name')
        user1 = get_user_model().objects.create_user(email='test@test.ru', password='Some_password123',
                                                     first_name='Иван', last_name='Иванов', phone='8-000-000-00-00')
        user2 = get_user_model().objects.create_user(email='test2@test.ru', password='Some_password123',
                                                     first_name='Петр', last_name='Петров', phone='8-000-000-00-11')
        room = Room.objects.create(hotel=hotel, number=101, type=type_room1, price=1000, number_of_guests=5)
        room2 = Room.objects.create(hotel=hotel, number=102, type=type_room2, price=700, number_of_guests=6)
        reserve1 = Reserve.objects.create(client=user1, room=room, day_in='2022-09-17', day_out='2022-09-19',
                                          number_of_guests=2)
        reserve2 = Reserve.objects.create(client=user2, room=room2, day_in='2022-09-27', day_out='2022-09-28',
                                          number_of_guests=3)

    def test_redirect_if_not_logged_in(self):
        """ Проверяет, что не авторизованного пользователя редиректит на страницу авторизации"""
        room = Room.objects.get(number=101)
        user = CustomUser.objects.get(email='test@test.ru')
        reserve = Reserve.objects.get(client=user, room=room, day_in='2022-09-17', day_out='2022-09-19',
                                      number_of_guests=2)
        resp = self.client.get(reverse('cancel', kwargs={'pk': reserve.pk}))
        self.assertRedirects(resp, f'/login?next=/cancel/{reserve.pk}')

    def test_logged_in_uses_correct_email(self):
        """
        Проверяет почту авторизованного пользователя в контексте ответа
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        room = Room.objects.get(number=101)
        user = CustomUser.objects.get(email='test@test.ru')
        reserve = Reserve.objects.get(client=user, room=room, day_in='2022-09-17', day_out='2022-09-19',
                                      number_of_guests=2)
        resp = self.client.get(reverse('cancel', kwargs={'pk': reserve.pk}))
        self.assertEqual(str(resp.context['user'].email), 'test@test.ru')
        self.assertEqual(resp.status_code, 200)

    def test_logged_in_uses_correct_generate_url(self):
        """
        Проверяет код ответа по сгенерированному урлу
        Проверяет что используется правильный шаблон
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        room = Room.objects.get(number=101)
        user = CustomUser.objects.get(email='test@test.ru')
        reserve = Reserve.objects.get(client=user, room=room, day_in='2022-09-17', day_out='2022-09-19',
                                      number_of_guests=2)
        resp = self.client.get(reverse('cancel', kwargs={'pk': reserve.pk}))
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "rooms/cancel.html")

    def test_view_url_exists_at_desired_location(self):
        """
        Проверяет код ответа по указанному урлу
        Проверяет что используется правильный шаблон
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        room = Room.objects.get(number=101)
        user = CustomUser.objects.get(email='test@test.ru')
        reserve = Reserve.objects.get(client=user, room=room, day_in='2022-09-17', day_out='2022-09-19',
                                      number_of_guests=2)
        resp = self.client.get(f'/cancel/{reserve.pk}')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "rooms/cancel.html")

    def test_context_data(self):
        """ Проверяет в контексте наличие ключей 'days', 'delay','message' и их значения """
        self.client.login(email='test2@test.ru', password='Some_password123')
        user = CustomUser.objects.get(email='test2@test.ru')
        reserve = Reserve.objects.get(client=user)
        resp = self.client.get(reverse('cancel', kwargs={'pk': reserve.pk}))
        self.assertTrue('days' in resp.context)
        self.assertTrue('delay' in resp.context)
        self.assertTrue('message' in resp.context)
        self.assertEqual(resp.context['days'], 1)
        self.assertFalse(resp.context['delay'])
        self.assertEqual(resp.context['message'],
                         'Вам вернется стоимость за 1 дней с 2022-09-27 по 2022-09-28 в размере 700 рублей.')

    def test_permission_denied(self):
        """
        Проверка кода ответа в случае запроса к старнице пользователя, которому не принадлежит резерв (404)
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        user = CustomUser.objects.get(email='test2@test.ru')
        reserve = Reserve.objects.get(client=user)
        resp = self.client.get(reverse('cancel', kwargs={'pk': reserve.pk}))
        self.assertEqual(resp.status_code, 404)

    def test_permission_allowed(self):
        """
        Проверка кода ответа в случае запроса к старнице пользователя, которому  принадлежит резерв (200)
        """
        self.client.login(email='test2@test.ru', password='Some_password123')
        user = CustomUser.objects.get(email='test2@test.ru')
        reserve = Reserve.objects.get(client=user)
        resp = self.client.get(reverse('cancel', kwargs={'pk': reserve.pk}))
        self.assertEqual(resp.status_code, 200)

    def test_post_request(self):
        """
        Проверка что после валидного post запроса добавляется объект Отзыва
        Проверка кода ответа при успешном post запросе (302)
        Проверка урла для редиректа
        Проверка что объект резерва удалился
        """
        self.client.login(email='test2@test.ru', password='Some_password123')
        user = CustomUser.objects.get(email='test2@test.ru')
        reserve = Reserve.objects.get(client=user)
        resp = self.client.post(reverse('cancel', kwargs={'pk': reserve.pk}))
        self.assertEqual(resp.status_code, 302)
        self.assertTrue(resp.url.startswith('/all_reserves'))
        resp = self.client.post(reverse('cancel', kwargs={'pk': reserve.pk}))
        self.assertEqual(resp.status_code, 404)


class ListFreeRoomsViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        type_room = TypeRoom.objects.create(code=2, nomination='Стандарт', description='Стандартный номер')
        hotel = Hotel.objects.create(name='Test hotel name')
        user1 = get_user_model().objects.create_user(email='test@test.ru', password='Some_password123',
                                                     first_name='Иван', last_name='Иванов', phone='8-000-000-00-00')
        user2 = get_user_model().objects.create_user(email='test2@test.ru', password='Some_password123',
                                                     first_name='Петр', last_name='Петров', phone='8-000-000-00-11')
        room = Room.objects.create(hotel=hotel, number=101, type=type_room, price=1000, number_of_guests=5)
        for i in range(8):
            Room.objects.create(hotel=hotel, number=i, type=type_room, price=5000, number_of_guests=5)
        reserve = Reserve.objects.create(client=user1, room=room, day_in='2022-09-17', day_out='2022-09-19',
                                         number_of_guests=2)

    def test_redirect_if_not_logged_in(self):
        """ Проверяет, что не авторизованного пользователя редиректит на страницу авторизации"""
        resp = self.client.get(reverse('list_free_rooms'))
        self.assertRedirects(resp, f'/login?next=/list_free_rooms')

    def test_logged_in_uses_correct_email(self):
        """
        Проверяет почту авторизованного пользователя в контексте ответа
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        resp = self.client.get(reverse('list_free_rooms'),
                               data={'number_of_guests': '3', 'day_in': '2022-10-25', 'day_out': '2022-10-30'})
        self.assertEqual(str(resp.context['user'].email), 'test@test.ru')
        self.assertEqual(resp.status_code, 200)

    def test_logged_in_uses_correct_generate_url(self):
        """
        Проверяет код ответа по сгенерированному урлу
        Проверяет что используется правильный шаблон
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        resp = self.client.get(reverse('list_free_rooms'),
                               data={'number_of_guests': '3', 'day_in': '2022-10-25', 'day_out': '2022-10-30'})
        self.assertEqual(str(resp.context['user'].email), 'test@test.ru')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "rooms/list_free_rooms.html")

    def test_view_url_exists_at_desired_location(self):
        """
        Проверяет код ответа по указанному урлу
        Проверяет что используется правильный шаблон
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        resp = self.client.get(f'/list_free_rooms',
                               data={'number_of_guests': '3', 'day_in': '2022-10-25', 'day_out': '2022-10-30'})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "rooms/list_free_rooms.html")

    def test_context_data(self):
        """ Проверяет в контексте наличие ключей 'day_in', 'day_out','number_of_guests' и их значения """
        self.client.login(email='test@test.ru', password='Some_password123')
        resp = self.client.get(reverse('list_free_rooms'),
                               data={'number_of_guests': '3', 'day_in': '2022-10-25', 'day_out': '2022-10-30'})
        self.assertTrue('day_in' in resp.context)
        self.assertTrue('day_out' in resp.context)
        self.assertTrue('number_of_guests' in resp.context)
        self.assertEqual(resp.context['day_in'], '2022-10-25')
        self.assertEqual(resp.context['day_out'], '2022-10-30')
        self.assertEqual(resp.context['number_of_guests'], '3')

    def test_pagination_is_six(self):
        """
        Проверяет наличие ключа 'is_paginated' в контексте ответа
        Проверяет истиность значения 'is_paginated' в контексте ответа
        Проверяет длину списка объектов на первой странице пагинации
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        resp = self.client.get(reverse('list_free_rooms'),
                               data={'number_of_guests': '3', 'day_in': '2022-10-25', 'day_out': '2022-10-30'})
        self.assertTrue('is_paginated' in resp.context)
        self.assertTrue(resp.context['is_paginated'])
        self.assertTrue(len(resp.context['rooms']) == 6)


class PayViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        type_room = TypeRoom.objects.create(code=1, nomination='Эконом', description='Дешевый номер')
        hotel = Hotel.objects.create(name='Test hotel name')
        user1 = get_user_model().objects.create_user(email='test@test.ru', password='Some_password123',
                                                     first_name='Иван', last_name='Иванов', phone='8-000-000-00-00')
        user2 = get_user_model().objects.create_user(email='test2@test.ru', password='Some_password123',
                                                     first_name='Петр', last_name='Петров', phone='8-000-000-00-11')
        room = Room.objects.create(hotel=hotel, number=101, type=type_room, price=1000, number_of_guests=5)
        for i in range(8):
            Room.objects.create(hotel=hotel, number=i, type=type_room, price=5000, number_of_guests=5)
        reserve = Reserve.objects.create(client=user1, room=room, day_in='2022-09-17', day_out='2022-09-19',
                                          number_of_guests=2)



    def test_redirect_if_not_logged_in(self):
        """ Проверяет, что не авторизованного пользователя редиректит на страницу авторизации"""
        room = Room.objects.get(number=101)
        resp = self.client.get(reverse('pay', kwargs={'number': room.number}))
        self.assertRedirects(resp, f'/login?next=/pay/{room.number}')

    def test_logged_in_uses_correct_email(self):
        """
        Проверяет почту авторизованного пользователя в контексте ответа
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        room = Room.objects.get(number=101)
        resp = self.client.get(reverse('pay', kwargs={'number': room.number}),
                               data={'number_of_guests': '3', 'day_in': '2022-10-25', 'day_out': '2022-10-30'})
        self.assertEqual(str(resp.context['user'].email), 'test@test.ru')
        self.assertEqual(resp.status_code, 200)

    def test_logged_in_uses_correct_generate_url(self):
        """
        Проверяет код ответа по сгенерированному урлу
        Проверяет что используется правильный шаблон
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        room = Room.objects.get(number=101)
        resp = self.client.get(reverse('pay', kwargs={'number': room.number}),
                               data={'number_of_guests': '3', 'day_in': '2022-10-25', 'day_out': '2022-10-30'})
        self.assertEqual(str(resp.context['user'].email), 'test@test.ru')
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "rooms/pay.html")

    def test_view_url_exists_at_desired_location(self):
        """
        Проверяет код ответа по указанному урлу
        Проверяет что используется правильный шаблон
        """
        self.client.login(email='test@test.ru', password='Some_password123')
        room = Room.objects.get(number=101)
        resp = self.client.get(f'/pay/{room.number}',
                               data={'number_of_guests': '3', 'day_in': '2022-10-25', 'day_out': '2022-10-30'})
        self.assertEqual(resp.status_code, 200)
        self.assertTemplateUsed(resp, "rooms/pay.html")

    def test_context_data(self):
        """ Проверяет в контексте наличие ключа 'message' и его значения """
        self.client.login(email='test@test.ru', password='Some_password123')
        room = Room.objects.get(number=101)
        resp = self.client.get(f'/pay/{room.number}',
                               data={'number_of_guests': '3', 'day_in': '2022-10-25', 'day_out': '2022-10-30'})
        self.assertTrue('message' in resp.context)
        message = """ 
                    Номер успешно забронирован. Детали бронирования были отправлены вам на электронную почту. 
                    Так же информацию о брони вы можете посмотреть в разделе "Мои резервы". 
                    """
        self.assertEqual(resp.context['message'], message)
