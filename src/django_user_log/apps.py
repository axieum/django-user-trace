from django.apps import AppConfig


class DjangoUserLogConfig(AppConfig):
    """django-user-log."""

    name = "django_user_log"

    def ready(self) -> None:
        """Sets up the django-user-log app."""

        # Register signals
        from . import signals  # noqa: F401 # isort: split

        # Load settings
        from . import conf  # noqa: F401 # isort: split
