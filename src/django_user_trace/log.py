from __future__ import annotations

import logging
from typing import Any, Iterable

from django_user_trace.conf import settings
from django_user_trace.context import user_attrs


class DjangoUserAttrs(logging.Filter):
    """A logging filter for including Django user attributes."""

    def __init__(self, attrs: Iterable[str] | None = None, *args: str, **kwargs: str) -> None:
        """
        Initialises a new logging filter for including Django user attributes.

        :param attrs: optional list of enabled user attribute keys (defaults to all)
        :param args: filter positional arguments
        :param kwargs: filter keyword arguments
        """

        super().__init__(*args, **kwargs)
        self.attrs: list[str] | None = [*attrs] if attrs else None

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Modifies the log record to include all user context data.

        :param record: mutable log record
        :return: true to always log the record
        """

        attributes: dict[str, Any] = user_attrs.get() or {}
        for attr in settings.USER_ATTRS:
            if not self.attrs or attr in self.attrs:
                setattr(record, attr, attributes.get(attr))

        return True
