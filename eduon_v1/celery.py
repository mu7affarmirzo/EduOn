from __future__ import absolute_import, unicode_literals

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eduon_v1.settings")

app = Celery("eduon_v1")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
