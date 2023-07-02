# Celery

## 1. Installed apps

Add `django_user_trace.contrib.celery` alongside [`celery`][celery] to your
[`INSTALLED_APPS`][django:installed_apps] Django setting:

```py
INSTALLED_APPS = [
  # ...
  "celery",
  "django_user_trace",  # https://github.com/axieum/django-user-trace
  "django_user_trace.contrib.celery",#(1)!
]
```

1. The Django app will register receivers against [Celery][celery:signals]'s
   signals. It will copy the captured user context into new task's headers.

[celery]: https://docs.celeryq.dev/
[celery:signals]: https://docs.celeryq.dev/en/stable/userguide/signals.html
[django:installed_apps]: https://docs.djangoproject.com/en/stable/ref/settings/#installed-apps
