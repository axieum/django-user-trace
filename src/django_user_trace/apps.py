from django.apps import AppConfig


class DjangoUserTraceConfig(AppConfig):
    """django-user-trace."""

    name = "django_user_trace"

    def ready(self) -> None:
        """Sets up the django-user-trace app."""

        # Register signals
        from . import signals  # noqa: F401 # isort: split

        # Load settings
        from . import conf  # noqa: F401 # isort: split
