from __future__ import annotations

from contextvars import ContextVar
from typing import TYPE_CHECKING, Any

from django_user_trace.conf import settings
from django_user_trace.utils import rgetattr

if TYPE_CHECKING:
    from django.contrib.auth.base_user import AbstractBaseUser
    from django.contrib.auth.models import AnonymousUser
    from django.http import HttpRequest
    from starlette.types import Scope


# The Django user attributes available for use in log messages on the current thread
user_attrs: ContextVar[dict[str, Any] | None] = ContextVar("django_user_trace", default=None)


def get_user_attrs() -> dict[str, Any] | None:
    """
    Returns the Django user attributes currently in use for the current thread if present.

    :return: optional mapping of {log record name: user attribute}
    """

    return user_attrs.get()


def build_user_attrs(
    request: HttpRequest | Scope, user: AbstractBaseUser | AnonymousUser | None = None
) -> dict[str, Any]:
    """
    Builds the Django user attributes dictionary from a given HTTP request or ASGI scope and Django user object.

    :param request: Django HTTP request, or ASGI scope
    :param user: optional Django user
    :return: a mapping of {log record name: user attribute}
    """

    return {
        key: (
            val
            if (val := lookup(user, request) if callable(lookup) else rgetattr(user, lookup, None)) not in (None, "")
            else None
        )
        for key, lookup in settings.USER_ATTRS.items()
    }
