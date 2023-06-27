from django.apps import AppConfig


class DjangoUserTraceCeleryConfig(AppConfig):
    """django-user-trace Celery integration."""

    name = "django_user_trace.contrib.celery"
    label = "django_user_trace_celery"

    def ready(self) -> None:
        """Sets up the django-user-trace Celery integration app."""

        # Register signals
        from . import signals  # noqa: F401 # isort: split
