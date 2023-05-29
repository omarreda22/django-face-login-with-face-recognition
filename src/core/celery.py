from __future__ import absolute_import, unicode_literals
import os

from celery import Celery

# Set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')

app = Celery('core')

# Using a string here means the worker doesn't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django apps.
app.autodiscover_tasks()

# celery -A core worker -l info
# celery -A core worker -l info -P gevent


##############################

# schedules

from celery.schedules import crontab 
"""
    - https://docs.celeryq.dev/en/stable/userguide/periodic-tasks.html?highlight=periodic#crontab-schedules
    -
    - celery -A core beat -l info
"""

app.conf.beat_schedule = {
    'add-every-min':{
        'task':'add_two_numbers',
        'schedule': crontab(),
        'args': (2, 3),
    },
    'add-every-5-sic':{
        'task':'add_two_numbers',
        'schedule': 5.0,
        'args': (2, 60),
    },
    'add-every-30-sic':{
        'task':'add_two_numbers',
        'schedule': 30.0,
        'args': (2, 60),
    }
}