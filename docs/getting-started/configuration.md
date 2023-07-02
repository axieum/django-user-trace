# Configuration

You can provide settings for `django-user-trace` by adding `DJANGO_USER_TRACE` as a
dictionary to your Django settings.

The default settings are as follows:

```py title="settings.py"
DJANGO_USER_TRACE = {
    "USER_ATTRS": {"username": "get_username"},
    "CELERY_TASK_HEADER": "User",
}
```

## `USER_ATTRS`

<small markdown>
**Default:** `#!py {"username": "get_username"}`<br>
**Type:** `#!py dict[str, str | Callable[[AbstractBaseUser | AnonymousUser, HttpRequest], Any]]`
</small>

This option controls which [`request.user`][django:request_user] attributes are
made available to the log records.

It is a mapping of log record field names to either:

1. an attribute on the Django [`request.user`][django:request_user] object;
2. a callable that accepts ([`AbstractBaseUser`][django:user] |
   [`AnonymousUser`][django:anon_user], [`HttpRequest`][django:request]) and
   returns the result;
3. an import string (prefixed with `ext://`) to a callable as seen in (2) above.

!!! tip
    To lookup nested attributes, separate them by `__` (two underscores), e.g.
    `profile__country__code`.

```py title="settings.py"
def get_custom_attribute(user, request):
    return f"Mr. {user.get_short_name()}"

DJANGO_USER_TRACE = {
    # ...
    "USER_ATTRS": {
        "email": "email",#(1)!
        "username": "get_username",#(2)!
        "custom": get_custom_attribute,#(3)!
        "custom_2": "ext://settings.get_custom_attribute",#(4)!
    },
}
```

1. Here, we are configuring the `USER_ATTRS` option of `django-user-trace` to
   map [`request.user.email`][django:user_email] to the `username` field on a
   log record.
2. Here, we are mapping the result of invoking the
   [`get_username()`][django:user_get_username] method on the
   [`request.user`][django:request_user] instance, to the `username` field on a
   log record.
3. Here, we are mapping the result of invoking the `get_custom_attribute`
   callable (defined above) to the `custom` field on a log record.
4. Here is another way of invoking the same `get_custom_attribute` callable
   (defined above) by first importing the callable from
   `settings.get_custom_attribute`.

## `CELERY_TASK_HEADER`

<small markdown>
**Default:** `#!py "User"`<br>
**Type:** `#!py str`
</small>

This option determines the name of the Celery task header used to trace user
attributes when `django_user_trace.contrib.celery` integration is installed.

[django:anon_user]: https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.models.AnonymousUser
[django:request]: https://docs.djangoproject.com/en/stable/ref/request-response/#django.http.HttpRequest
[django:request_user]: https://docs.djangoproject.com/en/stable/ref/request-response/#django.http.HttpRequest.user
[django:user]: https://docs.djangoproject.com/en/stable/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser
[django:user_email]: https://docs.djangoproject.com/en/stable/ref/contrib/auth/#django.contrib.auth.models.User.email
[django:user_get_username]: https://docs.djangoproject.com/en/stable/topics/auth/customizing/#django.contrib.auth.models.AbstractBaseUser.get_username
[python:logging]: https://docs.python.org/3/library/logging.html
