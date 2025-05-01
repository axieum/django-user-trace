# ASGI

To use the `django_user_trace.asgi.UserTraceMiddleware` middleware, wrap it
around the appropriate level of consumer in your `asgi.py` alongside the
[`AuthMiddlewareStack`][channels:authentication]:

```py
from asgi_correlation_id.middleware import CorrelationIdMiddleware
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from django.urls import re_path
from django_user_trace.asgi import UserTraceMiddleware

application = ProtocolTypeRouter(
    {
        "http": CorrelationIdMiddleware(#(2)!
            AuthMiddlewareStack(
                UserTraceMiddleware(#(1)!
                    URLRouter(
                        [
                            re_path(r"^foo", FooHttpConsumer.as_asgi()),#(3)!
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
   middleware must be placed **within**
   [`AuthMiddlewareStack`][channels:authentication] to ensure `user` exists in
   the scope.
2. This is optional to show [snok/asgi-correlation-id][asgi-correlation-id]'s
   integration.
3. This is an example of an ASGI-only route — for example, you could register
   a [Strawberry GraphQL][strawberry-graphql] consumer here.

[asgi-correlation-id]: https://github.com/snok/asgi-correlation-id
[channels:authentication]: https://channels.readthedocs.io/en/stable/topics/authentication.html
[django:middleware]: https://docs.djangoproject.com/en/stable/ref/settings/#middleware
[strawberry-graphql]: https://strawberry.rocks/docs/integrations/channels_
