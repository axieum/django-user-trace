"""Celery configuration for example project."""

import os

from celery import Celery

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.settings")

app = Celery("example")
app.config_from_object("django.conf:settings", namespace="CELERY")

from . import tasks  # noqa: E402, F401 # isort: split
