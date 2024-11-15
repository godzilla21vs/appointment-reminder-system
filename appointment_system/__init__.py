from __future__ import absolute_import, unicode_literals

# Importer Celery
from .celery import app as celery_app

# Exposer Celery en tant que module au niveau du package
__all__ = ('celery_app',)
