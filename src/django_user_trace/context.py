from __future__ import annotations

from contextvars import ContextVar
from typing import Any

# The Django user attributes available for use in log messages on the current thread
user_attrs: ContextVar[dict[str, Any] | None] = ContextVar("django_user_trace", default=None)


def get_user_attrs() -> dict[str, Any] | None:
    """
    Returns the Django user attributes currently in use for the current thread if present.

    :return: optional mapping of {log record name: user attribute}
    """

    return user_attrs.get()
