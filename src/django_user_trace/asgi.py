from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import TYPE_CHECKING, cast

from django.core.exceptions import ImproperlyConfigured

from django_user_trace.context import build_user_attrs, user_attrs

if TYPE_CHECKING:
    from django.contrib.auth.base_user import AbstractBaseUser
    from django.contrib.auth.models import AnonymousUser
    from starlette.types import ASGIApp, Receive, Scope, Send


logger: logging.Logger = logging.getLogger(__name__)


@dataclass
class UserTraceMiddleware:
    """Observes the user context of a scope for use in Python's logging framework."""

    app: ASGIApp

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        """Capture the user context of a scope for use in Python's logging framework."""

        if scope["type"] not in ("http", "websocket"):  # pragma: nocover
            return await self.app(scope, receive, send)

        logger.debug("asgi middleware called")

        # Check that authentication has been performed by earlier middleware
        if "user" not in scope:
            raise ImproperlyConfigured(
                "The django-user-trace ASGI middleware requires authentication middleware to be installed. "
                "Edit your ASGI application to wrap it in 'AuthStackMiddleware(UserTraceMiddleware(...))'."
            )
        user: AbstractBaseUser | AnonymousUser = cast("AbstractBaseUser | AnonymousUser", scope["user"])

        # Capture any necessary user attributes for use in log messages
        user_attrs.set(attrs := build_user_attrs(scope, user))
        logger.debug("set `user_attrs` context var to %s", attrs)

        return await self.app(scope, receive, send)
