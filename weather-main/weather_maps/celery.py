from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

# setting the Django settings module.
os.environ.setdefault(key='DJANGO_SETTINGS_MODULE', value='weather_maps.settings')

app = Celery('weather_maps')
app.config_from_object('django.conf:settings', namespace='CELERY')

# Looks up for task modules in Django applications and loads them
app.autodiscover_tasks()