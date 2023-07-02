from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Final

from django.conf import settings as django_settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string

if TYPE_CHECKING:
    from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
    from django.http import HttpRequest


# The key used to lookup user-defined settings from Django settings
SETTINGS_KEY: str = "DJANGO_USER_TRACE"


class Settings:
    """django-user-trace settings."""

    def __init__(self, key: str = SETTINGS_KEY) -> None:
        """
        Initialises the settings for use throughout django-user-trace.

        :param key: key used to lookup user-defined settings from Django settings
        """

        # A mapping of log record field names to either:
        #   1. an attribute on the Django `request.user` object;
        #     a. To lookup nested attributes, separate them by `__` (two underscores), e.g. `profile__country__code`
        #   2. a callable that accepts (`AbstractBaseUser` | `AnonymousUser`, `HttpRequest`) and returns the result;
        #   3. an import string (prefixed with `ext://`) to a callable as seen in (2) above.
        self.USER_ATTRS: dict[str, str | Callable[[AbstractBaseUser | AnonymousUser, HttpRequest], Any]] = {
            "username": "get_username",
        }

        # The name of the Celery task header used to trace user attributes
        self.CELERY_TASK_HEADER: str = "User"

        # Load user defined settings
        if user_settings := getattr(django_settings, key, None):
            for setting, value in user_settings.items():
                if not hasattr(self, setting):
                    raise ImproperlyConfigured(f"'{setting}' is not a valid django-user-trace setting.")
                setattr(self, setting, value)

        # Validate settings
        self._validate_user_attrs()

    def _validate_user_attrs(self) -> None:
        """Validates the `USER_ATTRS` setting."""

        for name, attr in self.USER_ATTRS.items():
            # Resolve lazy imports, i.e. strings that start with 'ext://'
            if isinstance(attr, str) and attr.startswith("ext://"):
                try:
                    self.USER_ATTRS[name] = attr = import_string(attr[6:])
                except Exception as e:
                    raise ImproperlyConfigured(f"Cannot import django-user-trace user attribute '{name}'.") from e

            # Check that the attribute type is either a string or callable
            if not (isinstance(attr, str) or callable(attr)):
                raise ImproperlyConfigured(
                    f"Expected a string or callable for django-user-trace user attribute '{name}' "
                    f"but got '{type(attr)}'."
                )


settings: Final[Settings] = Settings()
