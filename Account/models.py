from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


def user_directory_path(instance, filename):
    """ Папка для хранения аватарок пользователей """
    return 'users/{0}/{1}'.format(instance.email, filename)


class TimeStampedModel(models.Model):
    """
    Модель абстрактного базового класса для добавления полей "дата создания" и "дата изменения"
    """
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')

    class Meta:
        abstract = True


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser, TimeStampedModel):
    """ Кастомная модель пользователя """
    username = None
    email = models.EmailField(verbose_name='Почта', max_length=255, unique=True)
    last_name = models.CharField(max_length=30, null=False, verbose_name='Фамилия')
    first_name = models.CharField(max_length=30, null=False, verbose_name='Имя')
    phone = models.CharField(max_length=22, blank=True, null=True, verbose_name='Телефон')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    photo = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name='Фото')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
