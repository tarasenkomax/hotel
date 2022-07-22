from django.test import TestCase

from Account.models import CustomUser
from Room.models import Hotel, TypeRoom, Room, Reserve, Review, Regulations, Gallery


class HotelModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        Hotel.objects.create(name='Test hotel name')

    def test_object_name(self):
        hotel = Hotel.objects.get(name='Test hotel name')
        self.assertEquals(hotel.__str__(), 'Test hotel name')


class TypeRoomModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        TypeRoom.objects.create(code=1, nomination='Эконом', description='Дешевый номер')

    def test_object_name(self):
        type_room = TypeRoom.objects.get(code=1)
        self.assertEquals(type_room.__str__(), 'Эконом')


class RoomModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        type_room = TypeRoom.objects.create(code=1, nomination='Эконом', description='Дешевый номер')
        type_room2 = TypeRoom.objects.create(code=2, nomination='Стандарт', description='Стандартный номер')
        hotel = Hotel.objects.create(name='Test hotel name')
        user = CustomUser.objects.create(first_name='Иван', last_name='Иванов', phone='8-000-000-00-00',
                                         email='test@test.ru')
        room = Room.objects.create(hotel=hotel, number=101, type=type_room, price=1000, number_of_guests=5)
        room2 = Room.objects.create(hotel=hotel, number=102, type=type_room2, price=700, number_of_guests=6)
        room3 = Room.objects.create(hotel=hotel, number=103, type=type_room2, price=300, number_of_guests=6)
        reserve1 = Reserve.objects.create(client=user, room=room, day_in='2022-09-17', day_out='2022-09-19',
                                          number_of_guests=2)
        reserve2 = Reserve.objects.create(client=user, room=room, day_in='2022-09-25', day_out='2022-09-26',
                                          number_of_guests=3)
        reserve3 = Reserve.objects.create(client=user, room=room2, day_in='2022-09-27', day_out='2022-09-28',
                                          number_of_guests=3)
        Review.objects.create(room=room, rating=3, body='1234', author=user, reserve=reserve1)
        Review.objects.create(room=room, rating=2, body='1234', author=user, reserve=reserve2)
        Review.objects.create(room=room2, rating=2, body='1234', author=user, reserve=reserve3)
        Regulations.objects.create(type_room=room.type, regulation='Не курить')
        Regulations.objects.create(type_room=room.type, regulation='Без домашних животных')
        Regulations.objects.create(type_room=room2.type, regulation='Не писать тесты')

    def test_object_name(self):
        room = Room.objects.get(number=101)
        self.assertEquals(room.__str__(), '101')

    def test_get_absolute_url(self):
        room = Room.objects.get(number=101)
        self.assertEquals(room.get_absolute_url(), '/room/101')

    def test_get_average_rating_empty(self):
        room = Room.objects.get(number=103)
        self.assertEquals(room.get_average_rating(), 5.0)

    def test_get_average_rating_not_empty(self):
        room = Room.objects.get(number=101)
        self.assertEquals(room.get_average_rating(), 2.5)

    def test_get_regulations_list(self):
        room = Room.objects.get(number=101)
        room2 = Room.objects.get(number=102)
        self.assertEquals(len(room.get_regulations_list()), 2)
        self.assertEquals(len(room2.get_regulations_list()), 1)

    def test_get_review_list(self):
        room = Room.objects.get(number=101)
        room2 = Room.objects.get(number=102)
        self.assertEquals(len(room.get_review_list()), 2)
        self.assertEquals(len(room2.get_review_list()), 1)

    def test_get_full_price(self):
        room = Room.objects.get(number=101)
        room2 = Room.objects.get(number=102)
        room3 = Room.objects.get(number=103)
        self.assertEquals(room.get_full_price(7), 7000)
        self.assertEquals(room2.get_full_price(5), 3500)
        self.assertEquals(room3.get_full_price(3), 900)


class GalleryModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        type_room = TypeRoom.objects.create(code=1, nomination='Эконом', description='Дешевый номер')
        hotel = Hotel.objects.create(name='Test hotel name')
        room = Room.objects.create(hotel=hotel, number=101, type=type_room, price=1000, number_of_guests=5)
        Gallery.objects.create(room=room)

    def test_object_name(self):
        room = Room.objects.get(number=101)
        gallery = Gallery.objects.get(room=room)
        self.assertEquals(gallery.__str__(), '101')


class ReserveModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        type_room = TypeRoom.objects.create(code=1, nomination='Эконом', description='Дешевый номер')
        hotel = Hotel.objects.create(name='Test hotel name')
        room = Room.objects.create(hotel=hotel, number=101, type=type_room, price=1000, number_of_guests=5)
        user = CustomUser.objects.create(first_name='Иван', last_name='Иванов', phone='8-000-000-00-00',
                                         email='test@test.ru')
        reserve = Reserve.objects.create(client=user, room=room, day_in='2022-09-17', day_out='2022-09-19',
                                         number_of_guests=2)

    def test_object_name(self):
        reserve = Reserve.objects.get(id=1)
        self.assertEquals(reserve.__str__(), 'test@test.ru : 2022-09-17 - 2022-09-19')


class ReviewModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        type_room = TypeRoom.objects.create(code=1, nomination='Эконом', description='Дешевый номер')
        hotel = Hotel.objects.create(name='Test hotel name')
        room = Room.objects.create(hotel=hotel, number=101, type=type_room, price=1000, number_of_guests=5)
        user = CustomUser.objects.create(first_name='Иван', last_name='Иванов', phone='8-000-000-00-00',
                                         email='test@test.ru')
        reserve = Reserve.objects.create(client=user, room=room, day_in='2022-09-17', day_out='2022-09-19',
                                         number_of_guests=2)
        review = Review.objects.create(room=room, rating=3, body='1234', author=user, reserve=reserve)

    def test_object_name(self):
        review = Review.objects.get(id=1)
        self.assertEquals(review.__str__(), 'test@test.ru : 3')
