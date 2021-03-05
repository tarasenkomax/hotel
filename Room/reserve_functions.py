import datetime as DT
from Room.models import Reserve


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
