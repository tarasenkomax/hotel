import datetime
from typing import Union

from django.contrib.auth.models import User
from django.core.mail import send_mail

from Room.models import Reserve, Room
from settings import config


def convert_str_to_date(date_str: Union[datetime.date, str]) -> datetime.date:
    """ Конвертировать строку 'ГГГГ-ММ-ДД' в datetime.date """
    return datetime.datetime.strptime(date_str, '%Y-%m-%d').date() if isinstance(date_str, str) else date_str


def check_availability(room: Room, day_in: datetime.date, day_out: datetime.date) -> bool:
    """ Проверка, не пересекаются ли даты резрва отдельной комнаты с указанными данными """
    reserve_list = Reserve.objects.filter(room=room)
    counter_false = 0
    if len(reserve_list) == 0:
        return True
    for reserve in reserve_list:
        if not (reserve.day_in >= day_out or reserve.day_out <= day_in):
            counter_false += 1
    return False if counter_false > 0 else True


def get_number_of_days(day_in: datetime.date, day_out: datetime.date) -> int:
    """ Подсчет количества дней"""
    return (day_out - day_in).days


def check_dates_of_user(user: User, day_in: datetime.date, day_out: datetime.date) -> bool:
    """ Проверка на наличие у пользователя существующих резервов на эти даты"""
    counter = 0
    reserve_list = Reserve.objects.filter(client=user)
    if len(reserve_list) == 0:
        return True
    else:
        for reserve in reserve_list:
            counter += 0 if reserve.day_in >= day_out or reserve.day_out <= day_in else 1
        return True if counter <= 0 else False


def send_email(name, room, day_in: datetime.date, day_out: datetime.date, number_of_guests, recipient):
    """ Отправка письма о подтверждении брони """
    email_theme = 'Дипломная работа'
    email_text = f"""
    Здравствуйте, {name}, ваша заявка на бронирование одобрена.
     ------ Детали бронирования ------
    Комната: {room}
    Прибытие: {day_in}
    Выезд: {day_out}
    Количество гостей: {number_of_guests}
    Желаем вам хорошего отдыха
    --
    С уважением, Администрация отеля.
    """
    send_mail(email_theme, email_text, config.EMAIL_HOST_USER, [str(recipient)], fail_silently=False)


def send_email_cancel(recipient):
    """ Отправка письма об отмене брони """
    email_theme = 'Дипломная работа. Отмена бронирования.'
    email_text = """
    Здравствуйте. Ваша заявка на отмену брони одобрена.
    --
    С уважением, Администрация отеля.
    """
    send_mail(email_theme, email_text, config.EMAIL_HOST_USER, [str(recipient)], fail_silently=False)
