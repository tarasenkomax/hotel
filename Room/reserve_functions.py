import datetime as DT
from django.core.mail import send_mail
from Room.models import Reserve, Review


def check_availability(room, day_in, day_out):
    """ Проверка, не пересекаются ли даты резрва отдельной комнаты с указанными данными """
    reserve_list = Reserve.objects.filter(room=room)
    if len(reserve_list) == 0:
        return True
    if (type(day_in) or type(day_out)) == str:
        day_in = DT.datetime.strptime(day_in, '%Y-%m-%d').date()
        day_out = DT.datetime.strptime(day_out, '%Y-%m-%d').date()
    for reserve in reserve_list:
        if reserve.day_in > day_out or reserve.day_out <= day_in:
            return True
        else:
            return False


def number_of_days(day_in, day_out):
    """ Подсчет количества дней"""
    day_in_ = DT.datetime.strptime(day_in, '%Y-%m-%d').date()
    day_out_ = DT.datetime.strptime(day_out, '%Y-%m-%d').date()
    days = day_out_ - day_in_
    return days.days


def dates_of_user(instance, day_in, day_out):
    """ Проверка на наличие у пользователя существующих резервов на эти даты"""
    user = instance
    day_in = DT.datetime.strptime(day_in, '%Y-%m-%d').date()
    day_out = DT.datetime.strptime(day_out, '%Y-%m-%d').date()
    reserve_list = Reserve.objects.filter(client=user)
    counter = 0
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


def average_rating(room):
    """ Средний рейтинг """
    review_list = Review.objects.filter(room=room)
    if review_list:
        rating_list = []
        for review in review_list:
            rating_list.append(review.rating)
        average = sum(rating_list) / len(rating_list)
        return average
    else:
        return None


def send_email(name, patronymic, room, day_in, day_out, number_of_guests, recipient):
    """ Отправка письма о подтверждении брони """
    email_theme = 'Диполмная работа'
    email_text = 'Здравствуйте, {} {} , ваша заявка на бронирование одобрена.\n ------ Детали бронирования ' \
                 '------\n Комната: {}\n Прибытие: {}.\n Выезд: {}.\n Количество гостей: {}\n Желаем вам ' \
                 'хорошего отдыха.\n\n\n\n --\n С уважением, Администрация отеля.'.format(name, patronymic, room,
                                                                                          day_in, day_out,
                                                                                          number_of_guests)
    send_mail(email_theme, email_text, 'djangotest97@gmail.com', ['{}'.format(recipient)],
              fail_silently=False)

