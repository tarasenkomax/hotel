from django.db import models

from Account.models import CustomUser


def catalog_of_photo_rooms(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'rooms/{0}/{1}'.format(instance.room.number, filename)


class Hotel(models.Model):
    """ Модель Отеля """
    name = models.CharField(max_length=50, blank=True, unique=True, null=False, verbose_name='Название')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Отели'
        verbose_name = 'Отель'


class TypeRoom(models.Model):
    """ Модель типа комнаты """
    nomination = models.CharField(max_length=50, blank=True, unique=True, null=False, verbose_name='Наименование')

    def __str__(self):
        return self.nomination

    class Meta:
        verbose_name_plural = 'Типы комнат'
        verbose_name = 'Тип комнаты'


class Room(models.Model):
    """ Модель Комнаты """
    hotel = models.ForeignKey(Hotel, null=False, on_delete=models.PROTECT, verbose_name='Отель')
    number = models.IntegerField(null=False, unique=True, verbose_name='Номер')
    type = models.ForeignKey(TypeRoom, on_delete=models.PROTECT, null=True, verbose_name='Тип')
    price = models.IntegerField(null=True, verbose_name='Цена', help_text='указывать в рублях')
    number_of_guests = models.IntegerField(null=True, verbose_name='Количество гостей')

    # reserve

    def __str__(self):
        return str(self.number)

    class Meta:
        verbose_name_plural = 'Комнаты'
        verbose_name = 'Комната'


class Gallery(models.Model):
    """ Фотографии комнат"""
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
    photo5 = models.ImageField(upload_to=catalog_of_photo_rooms, blank=True, null=True, verbose_name='Фото 5')

    def __str__(self):
        return str(self.room)

    class Meta:
        verbose_name_plural = 'Галереи комнат'
        verbose_name = 'Галерея комнаты'


class Reserve(models.Model):
    """ Резервация комнат """
    client = models.ForeignKey(CustomUser, on_delete=models.CASCADE, null=False, related_name='client',
                               verbose_name='Клиент')
    room = models.ForeignKey(Room, on_delete=models.CASCADE, null=False, verbose_name='Комната')
    day_in = models.DateField(verbose_name='Дата заезда', null=False)
    day_out = models.DateField(verbose_name='Дата выезда', null=False)

    def __str__(self):
        return str(self.room)

    class Meta:
        verbose_name_plural = 'Резервы комнат'
        verbose_name = 'Резерв комнаты'
