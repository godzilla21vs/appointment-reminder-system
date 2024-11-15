from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# Définir les paramètres de Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'appoitment_system.settings')

# Initialiser Celery
app = Celery('appoitment_system')

# Charger la configuration depuis les paramètres Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Recherche automatique des tâches dans les applications installées
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
