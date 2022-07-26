import datetime
import re
from typing import Union

from django.contrib.auth.models import User
from django.core.mail import send_mail

from Room.models import Reserve, Room
from settings import config


def convert_str_to_date(date_str: Union[datetime.date, str]) -> datetime.date:
    """ Конвертировать строку 'ГГГГ-ММ-ДД' или 'ДД.ММ.ГГГГ' в datetime.date """
    if re.search(r"(\d{4}-\d{1,2}-\d{1,2})", date_str):
        return datetime.datetime.strptime(date_str, '%Y-%m-%d').date() if isinstance(date_str, str) else date_str
    elif re.search(r"(\d{1,2}.\d{1,2}.\d{4})", date_str):
        return datetime.datetime.strptime(date_str, '%d.%m.%Y').date() if isinstance(date_str, str) else date_str


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


def send_reserve_email(name, room, day_in: datetime.date, day_out: datetime.date, number_of_guests, recipient):
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


def send_cancel_email(recipient):
    """ Отправка письма об отмене брони """
    email_theme = 'Дипломная работа. Отмена бронирования.'
    email_text = """
    Здравствуйте. Ваша заявка на отмену брони одобрена.
    --
    С уважением, Администрация отеля.
    """
    send_mail(email_theme, email_text, config.EMAIL_HOST_USER, [str(recipient)], fail_silently=False)


def calculate_refund_amount(reserve: Reserve) -> dict:
    """ Расчитать сумму возврата при отмене бронировния """
    if datetime.datetime.now().date() < reserve.day_in:
        days = get_number_of_days(reserve.day_in, reserve.day_out)
        delay = False
    elif datetime.datetime.now().date() == reserve.day_in:
        days = get_number_of_days(reserve.day_in, reserve.day_out) - 1
        delay = False
    else:
        if datetime.datetime.now().date() > reserve.day_out:
            days = 0
            delay = True
        else:
            days = get_number_of_days(datetime.datetime.now().date(), reserve.day_out)
            delay = False
    cost = reserve.room.price * days
    return {'days': days, 'delay': delay, 'cost': cost}
