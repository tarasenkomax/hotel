from django.core.mail import send_mail

from celery import shared_task

from Account.models import CustomUser
from settings import config


@shared_task
def send_promotion():
    """ Рассылка рекламных писем всем зарегистрированным пользователям """
    users = CustomUser.objects.all()
    email_theme = 'Рекламное письмо'
    email_text = 'Посетите наш сайт'
    for user in users:
        send_mail(email_theme, email_text, config.EMAIL_HOST_USER, [str(user.email)], fail_silently=False)
