import datetime as DT
from django.core.mail import send_mail
from Room.models import Reserve


def check_availability(room, day_in, day_out):
    """ Проверка, не пересекаются ли даты резрва отдельной комнаты с указанными данными """
    reserve_list = Reserve.objects.filter(room=room)
    counter_false = 0
    if len(reserve_list) == 0:
        return True
    if (type(day_in) or type(day_out)) == str:
        day_in = DT.datetime.strptime(day_in, '%Y-%m-%d').date()
        day_out = DT.datetime.strptime(day_out, '%Y-%m-%d').date()
    for reserve in reserve_list:
        if not (reserve.day_in >= day_out or reserve.day_out <= day_in):
            counter_false += 1
    if counter_false > 0:
        return False
    else:
        return True


def number_of_days(day_in, day_out):
    """ Подсчет количества дней"""
    if type(day_in) == str:
        day_in = DT.datetime.strptime(day_in, '%Y-%m-%d').date()
    if type(day_out) == str:
        day_out = DT.datetime.strptime(day_out, '%Y-%m-%d').date()
    days = day_out - day_in
    return days.days


def dates_of_user(instance, day_in, day_out):
    """ Проверка на наличие у пользователя существующих резервов на эти даты"""
    user = instance
    counter = 0
    reserve_list = Reserve.objects.filter(client=user)
    if type(day_in) == str:
        day_in = DT.datetime.strptime(day_in, '%Y-%m-%d').date()
    if type(day_out) == str:
        day_out = DT.datetime.strptime(day_out, '%Y-%m-%d').date()
    if len(reserve_list) == 0:
        return True
    else:
        for reserve in reserve_list:
            if reserve.day_in >= day_out or reserve.day_out <= day_in:
                counter += 0
            else:
                counter += 1
    if counter <= 0:
        return True
    else:
        return False


def send_email(name, room, day_in, day_out, number_of_guests, recipient):
    """ Отправка письма о подтверждении брони """
    email_theme = 'Дипломная работа'
    email_text = 'Здравствуйте, {}, ваша заявка на бронирование одобрена.\n ------ Детали бронирования ' \
                 '------\n Комната: {}\n Прибытие: {}.\n Выезд: {}.\n Количество гостей: {}\n Желаем вам ' \
                 'хорошего отдыха.\n\n\n\n --\n С уважением, Администрация отеля.'.format(name, room,
                                                                                          day_in, day_out,
                                                                                          number_of_guests)
    send_mail(email_theme, email_text, 'djangotest97@gmail.com', [str(recipient)],
              fail_silently=False)


def send_email_cancel(recipient):
    """ Отправка письма об отмене брони """
    email_theme = 'Дипломная работа. Отмена бронирования.'
    email_text = 'Здравствуйте. Ваша заявка на отмену брони одобрена.\n\n\n\n --\n С уважением, ' \
                 'Администрация отеля.'
    send_mail(email_theme, email_text, 'djangotest97@gmail.com', [str(recipient)],
              fail_silently=False)
