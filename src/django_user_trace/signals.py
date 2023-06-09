from __future__ import annotations

import logging
from typing import Any, Final

from django.core.signals import request_finished
from django.dispatch import Signal, receiver

from django_user_trace.context import user_attrs

logger: logging.Logger = logging.getLogger(__name__)


# Signaled before the view is called, during the `django-user-trace` middleware
#   :param request: HttpRequest
process_request: Final[Signal] = Signal()


# Signaled after the view has been called, during the `django-user-trace` middleware
#   :param request: HttpRequest
cleanup_request: Final[Signal] = Signal()


@receiver(request_finished)
def clear_user_attrs_after_request(sender: Any, **kwargs: dict[str, Any]) -> None:
    """
    Clears the `user_attrs` context variable after each HTTP request.

    :param sender: signal sender
    :param kwargs: signal keyword arguments
    """

    logger.debug("received signal `request_finished`, clearing `user_attrs` context var")
    user_attrs.set(None)
