from __future__ import absolute_import, unicode_literals

from celery import Celery
from django.conf import settings
from celery.schedules import crontab
import environ

env = environ.Env()
environ.Env.read_env('../.env')

backend=env('CELERY_RESULT_BACKEND')
broker=env('CELERY_BROKER_URL')

app = Celery('micro_investment', backend=backend, broker=broker)
app.conf.broker_url = broker

app.config_from_object(settings, namespace='CELERY')

app.autodiscover_tasks()

app.conf.beat_schedule = {
    
}