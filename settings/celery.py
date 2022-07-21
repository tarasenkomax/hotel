import os

from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings.settings')

app = Celery('settings')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'deleted_old_reserve': {
        'task': 'Room.tasks.drop_old_reserve',
        # Ежедневно в полночь
        'schedule': crontab(minute=0, hour=0),
    },
    'send_promotion': {
        'task': 'Account.tasks.send_promotion',
        # Каждый день в первый месяц каждого квартала(раз в 3 месяца)
        'schedule': crontab(0, 0, month_of_year='*/3'),
    }
}
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
