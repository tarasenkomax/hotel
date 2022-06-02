from celery import shared_task
from datetime import datetime, timedelta

from Room.models import Reserve


@shared_task
def drop_old_reserve():
    """ Удаление броней закончившихся больше полугода назад"""
    return Reserve.objects.filter(day_out__lte=datetime.now().date() - timedelta(days=180)).delete()
