import os

from tenant_schemas_celery.app import CeleryApp

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "eduon_v1.settings")

app = CeleryApp("eduon_v1")

app.config_from_object("django.conf:settings", namespace="CELERY")
app.autodiscover_tasks()
