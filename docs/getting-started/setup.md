# Setup

## 1. Installed apps

Add `django_user_trace` to your [`INSTALLED_APPS`][django:installed_apps] Django setting:

```py
INSTALLED_APPS = [
  # ...
  "django_user_trace",  # https://github.com/axieum/django-user-trace
]
```

## 2. Middleware

Add `django_user_trace.middleware.django_user_trace_middleware` to your
[`MIDDLEWARE`][django:middleware] Django setting:

```py
MIDDLEWARE = [
    # ...
    "django.contrib.auth.middleware.AuthenticationMiddleware",#(1)!
    "django_user_trace.middleware.django_user_trace_middleware",
    # ...
]
```

1. :exclamation: `django-user-trace` uses middleware to capture user
   attributes from each request's [`request.user`][django:request_user]
   attribute. To do this, the middleware must be placed **after** Django's
   [`AuthenticationMiddleware`][django:auth_middleware]!

## 3. Logging

Add `django_user_trace.log.DjangoUserAttrs` as a filter to your
[`LOGGING`][django:logging] Django setting, apply the filter to handler/s, and
add the new `username` field to any formatters:

```py
LOGGING = {
    # ...
    "filters": {
        # ...
        "user_attrs": {"()": "django_user_trace.log.DjangoUserAttrs"},#(1)!
    },
    "formatters": {
        # ...
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(username)s %(message)s",#(2)!
        },
    },
    "handlers": {
        # ...
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "verbose",
            "filters": ["user_attrs"],#(3)!
        },
    },
}
```

1. This Python [logging][python:logging] filter injects any configured user
   attributes to every log record.
2. Add any configured user attributes here, `username` is available by default.
3. We apply the new `user_attrs` filter that we defined above here.

### 3.1 Internal logs <small>optional</small> { #31-internal-logs data-toc-label="3.1 Internal logs" }

To view internal logs made by `django-user-trace` for debugging purposes, add the
`django_user_trace` logger to your [`LOGGING`][django:logging] Django setting:

```py
LOGGING = {
    # ...
    "loggers": {
        "django_user_trace": {
            "handlers": ["console"],
            "level": "WARNING",#(1)!
            "propagate": False,
        },
    },
}
```

1. :warning: It's recommended to not log any lower than `WARNING` in production,
   as doing so will lead to extra log messages **per request** &mdash; these add
   up over time.

[django:auth_middleware]: https://docs.djangoproject.com/en/stable/ref/middleware/#django.contrib.auth.middleware.AuthenticationMiddleware
[django:installed_apps]: https://docs.djangoproject.com/en/stable/ref/settings/#installed-apps
[django:logging]: https://docs.djangoproject.com/en/stable/ref/settings/#logging
[django:middleware]: https://docs.djangoproject.com/en/stable/ref/settings/#middleware
[django:request_user]: https://docs.djangoproject.com/en/stable/ref/request-response/#django.http.HttpRequest.user
[python:logging]: https://docs.python.org/3/library/logging.html
