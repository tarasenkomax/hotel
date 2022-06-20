from django.contrib.auth.base_user import BaseUserManager
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _


def user_directory_path(instance, filename):
    """ Папка для хранения аватарок пользователей """
    return 'users/{0}/{1}'.format(instance.email, filename)


class CustomUserManager(BaseUserManager):
    """ Пользовательский менеджер модели пользователя, где электронная почта является уникальным идентификатором для
    аутентификации вместо имени пользователей """

    def create_user(self, email, password, **extra_fields):
        """ Создает и сохраняет пользователя с указанным адресом электронной почты и паролем """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """ Создает и сохраняет суперпользователя с указанным адресом электронной почты и паролем """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    """ Кастомная модель пользователя """
    username = None
    email = models.EmailField(verbose_name='Почта', max_length=255, unique=True, )
    name = models.CharField(max_length=50, blank=True, null=True, verbose_name='Имя')
    surname = models.CharField(max_length=50, blank=True, null=True, verbose_name='Фамилия')
    phone = models.CharField(max_length=22, blank=True, null=True, verbose_name='Телефон')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    photo = models.ImageField(upload_to=user_directory_path, blank=True, null=True, verbose_name='Фото')

    def __str__(self):
        return '{0} {1}'.format(self.name, self.surname)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    class Meta:
        verbose_name_plural = 'Пользователи'
        verbose_name = 'Пользователь'
