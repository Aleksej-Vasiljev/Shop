from celery import Celery
from celery.schedules import crontab
import os

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings')

app = Celery('myproject')
app.config_from_object('django.conf:settings', namespace='CELERY')
app.autodiscover_tasks()

# Расписание задач
app.conf.beat_schedule = {
    'update-usd-rate-every-15-minutes': {
        'task': 'myapp.tasks.update_usd_rate',
        'schedule': crontab(minute='*/15'),
    },
}