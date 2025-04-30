"""ASGI configuration for example project."""

import os

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path

from django_user_trace.asgi import UserTraceMiddleware
from example.consumers import IndexHttpConsumer

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": AuthMiddlewareStack(
            UserTraceMiddleware(
                URLRouter(
                    [
                        re_path(r"^asgi", IndexHttpConsumer.as_asgi()),
                        re_path(r"^", django_asgi_app),  # type: ignore[arg-type]
                    ]
                ),
            )
        ),
    },
)
