from decimal import Decimal
from typing import Union

from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Avg, QuerySet
from django.urls import reverse

from Account.models import CustomUser, TimeStampedModel


def catalog_of_photo_rooms(instance, filename):
    """ Папка для хранения фотографий комнат """
    return 'rooms/{0}/{1}'.format(instance.room.number, filename)


class Hotel(TimeStampedModel):
    """ Модель Отеля """
    name = models.CharField(max_length=50, blank=True, unique=True, null=False, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Отели'
        verbose_name = 'Отель'


class TypeRoom(TimeStampedModel):
    """ Модель типа комнаты """
    code = models.SmallIntegerField(primary_key=True, verbose_name='Код')
    nomination = models.CharField(max_length=50, blank=True, unique=True, null=False, verbose_name='Наименование')
    description = models.CharField(max_length=300, blank=True, null=False, verbose_name='Описание')

    def __str__(self):
        return self.nomination

    class Meta:
        verbose_name_plural = 'Типы комнат'
        verbose_name = 'Тип комнаты'


class Room(TimeStampedModel):
    """ Модель Комнаты """
    hotel = models.ForeignKey(Hotel, null=False, on_delete=models.CASCADE, verbose_name='Отель')
    number = models.IntegerField(null=False, unique=True, verbose_name='Номер')
    type = models.ForeignKey(TypeRoom, on_delete=models.PROTECT, null=True, verbose_name='Тип')
    price = models.IntegerField(null=True, verbose_name='Цена', help_text='указывать в рублях')
    number_of_guests = models.IntegerField(null=True, verbose_name='Количество гостей')

    def __str__(self):
        return str(self.number)

    def get_absolute_url(self):
        return reverse('detail_room', kwargs={"number": self.number})

    def get_average_rating(self) -> Union[Decimal, None]:
        """ Получить средний рейтинг комнаты """
        reviews = Review.objects.filter(room__number=self.number).aggregate(Avg('rating'))['rating__avg']
        return Decimal(reviews).quantize(Decimal("1.0")) if reviews else 5.0

    def get_regulations_list(self) -> QuerySet:
        """ Получить список правил для комнаты """
        return Regulations.objects.filter(type_room=self.type)

    def get_review_list(self) -> QuerySet:
        """ Получить список отзывов для комнаты """
        return Review.objects.filter(room=self).order_by('-pub_date').select_related('author')

    def get_full_price(self, days: int) -> int:
        """ Получить стоимость проживания в комнате за указанное количество дней"""
        return self.price * days

    class Meta:
        verbose_name_plural = 'Комнаты'
        verbose_name = 'Комната'


class Gallery(TimeStampedModel):
    """ Модель галереи комнат"""
    room = models.OneToOneField(Room, on_delete=models.CASCADE, related_name='photos_of_room',
                                verbose_name='Комната')
    slider_photo1 = models.ImageField(upload_to=catalog_of_photo_rooms, blank=True, null=True,
                                      verbose_name='Фото 1', help_text='Фотография будет отображаться в слайдере')
    slider_photo2 = models.ImageField(upload_to=catalog_of_photo_rooms, blank=True, null=True,
                                      verbose_name='Фото 2', help_text='Фотография будет отображаться в слайдере')
    slider_photo3 = models.ImageField(upload_to=catalog_of_photo_rooms, blank=True, null=True,
                                      verbose_name='Фото 3', help_text='Фотография будет отображаться в слайдере')
    slider_photo4 = models.ImageField(upload_to=catalog_of_photo_rooms, blank=True, null=True,
                                      verbose_name='Фото 4', help_text='Фотография будет отображаться в слайдере')

    def __str__(self):
        return str(self.room)

    class Meta:
        verbose_name_plural = 'Галереи комнат'
        verbose_name = 'Галерея комнаты'


class Reserve(TimeStampedModel):
    """ Модель резерва комнаты """
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='client',
                               verbose_name='Клиент')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False, verbose_name='Комната')
    day_in = models.DateField(verbose_name='Дата заезда', null=False)
    day_out = models.DateField(verbose_name='Дата выезда', null=False)
    number_of_guests = models.IntegerField(null=True, verbose_name='Количество гостей')
    reg_date = models.DateField(auto_now_add=True, null=True, verbose_name='Дата регистрации резерва', )

    def __str__(self):
        return f"{self.client.email} : {self.day_in} - {self.day_out}"

    def clean(self):
        if self.day_in > self.day_out:
            raise ValidationError({'day_in': "Дата заезда не может быть позже даты выезда",
                                   'day_out': "Дата выезда не может быть раньше даты заезда"})

    class Meta:
        verbose_name_plural = 'Резервы комнат'
        verbose_name = 'Резерв комнаты'


class Review(TimeStampedModel):
    """ Модель отзыва """
    room = models.ForeignKey(Room, null=True, on_delete=models.CASCADE, verbose_name='Комната')
    rating = models.IntegerField(blank=True, null=True, verbose_name='Рейтинг')
    body = models.TextField(blank=True, null=True, verbose_name='Отзыв')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=True, verbose_name='Автор')
    reserve = models.OneToOneField(Reserve, on_delete=models.CASCADE, null=True, verbose_name='Резерв')
    pub_date = models.DateField(auto_now_add=True, null=True, verbose_name='Дата публикации', )

    def __str__(self):
        return f"{self.author.email} : {self.rating}"

    def clean(self):
        if 1 > self.rating or self.rating > 5:
            raise ValidationError({'rating': "Рейтинг должен быть в диапазоне от 1 до 5"})

    class Meta:
        verbose_name_plural = 'Отзывы комнат'
        verbose_name = 'Отзыв комнаты'


class Regulations(TimeStampedModel):
    """ Правила коматы """
    type_room = models.ForeignKey(TypeRoom, null=True, on_delete=models.CASCADE, verbose_name='Тип комнаты')
    regulation = models.TextField(blank=True, null=True, verbose_name='Правило')

    class Meta:
        verbose_name_plural = 'Правила комнат'
        verbose_name = 'Правило комнаты'
