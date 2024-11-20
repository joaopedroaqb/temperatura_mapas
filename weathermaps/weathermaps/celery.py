from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Define as configurações padrão do Django para o Celery
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'weathermaps.settings')

app = Celery('weathermaps')

# Lê as configurações do Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descobre automaticamente tarefas (tasks.py) nos apps instalados
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')


# celery -A weathermaps flower --port=5555                 COMANDO PARA EXECUTAR PRIMEIRO O CELERY
# entrar pela porta http://127.0.0.1:5555 e não a http://0.0.0.0:5555