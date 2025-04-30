# ASGI

Wrap your ASGI application inside `django_user_trace.asgi.UserTraceMiddleware`
and [`channels.auth.AuthMiddlewareStack`][channels:authentication].

```py
import os

from asgi_correlation_id.middleware import CorrelationIdMiddleware
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
from django.urls import re_path
from django_user_trace.asgi import UserTraceMiddleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "example.settings")

django_asgi_application = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": CorrelationIdMiddleware(#(2)!
            AuthMiddlewareStack(
                UserTraceMiddleware(#(1)!
                    URLRouter(
                        [
                            re_path(r"^foo", FooHttpConsumer.as_asgi()),#(3)!
                            re_path(r"^", django_asgi_application),  # type: ignore[arg-type]#(4)!
                        ]
                    )
                )
            )
        ),
        "websocket": CorrelationIdMiddleware(
            AuthMiddlewareStack(
                UserTraceMiddleware(
                    URLRouter(
                        [
                            re_path(r"^bar", BarWebSocketConsumer.as_asgi()),
                        ]
                    )
                )
            )
        )
    },
)
```

1. :exclamation: `django-user-trace` uses middleware to capture user
   attributes from the ASGI scope's `user` key. To do this, the
   middleware must be placed **within** Django Channels' authentication
   middleware to ensure `user` exists in the scope.
2. This is optional to show [snok/asgi-correlation-id][asgi-correlation-id]'s integration.
3. This is where your ASGI-only routes are defined, for example you could
   register a [Strawberry GraphQL][strawberry-graphql] consumer here.
4. This is your standard Django application, all of its
   [middleware][django:middleware] run.

[asgi-correlation-id]: https://github.com/snok/asgi-correlation-id
[channels:authentication]: https://channels.readthedocs.io/en/stable/topics/authentication.html
[django:middleware]: https://docs.djangoproject.com/en/stable/ref/settings/#middleware
[strawberry-graphql]: https://strawberry.rocks/docs/integrations/channels
