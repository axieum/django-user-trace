from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from channels.testing import HttpCommunicator
from django.core.exceptions import ImproperlyConfigured
from example.asgi import django_asgi_app

from django_user_trace.asgi import UserTraceMiddleware
from django_user_trace.context import get_user_attrs

if TYPE_CHECKING:
    from starlette.types import Receive, Scope, Send


async def test_incorrect_asgi_middleware_order() -> None:
    """
    Tests that registering the ``UserTraceMiddleware`` middleware before Django's ``AuthenticationMiddleware``
    raises an error.
    """

    with pytest.raises(
        ImproperlyConfigured,
        match=(
            "The django-user-trace ASGI middleware requires authentication middleware to be installed. "
            r"Edit your ASGI application to wrap it in 'AuthStackMiddleware\(UserTraceMiddleware\(...\)\)'."
        ),
    ):
        await HttpCommunicator(UserTraceMiddleware(django_asgi_app), method="GET", path="/").get_response()  # type: ignore[arg-type]


async def test_asgi_middleware_with_unknown_scope() -> None:
    """Tests that a non-HTTP or WebSocket scope is ignored by the ``UserTraceMiddleware`` middleware."""

    async def app(_scope: Scope, _receive: Receive, _send: Send) -> None:
        pass

    await UserTraceMiddleware(app)({"type": "other"}, None, None)  # type: ignore[arg-type]

    assert get_user_attrs() is None
