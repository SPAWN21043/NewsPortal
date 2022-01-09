import os
from celery import Celery
from celery.schedules import crontab


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'NewsPortal.settings')


app = Celery('NewsPortal')
app.config_from_object('django.conf:settings', namespace='CELERY')

app.conf.beat_schedule = {
    'send_mail_monday_8am': {
        'task': 'news.tasks.mail_monday',
        'schedule': crontab(hour=8, minute=0, day_of_week='monday'),
        # 'args': (agrs),
    },
}

app.autodiscover_tasks()



