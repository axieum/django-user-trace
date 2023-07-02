---
title: Integrations
---

An integration is an optional extension to the `django-user-trace` functionality.

Here are a list of available integrations:

* [Celery](celery.md)

## Writing your own integration

### User Context

You can access the [`ContextVar`][python:contextvars] used to store user
attributes on the current thread from
`#!py django_user_trace.context.user_attrs`.

### Signals

#### `#!py django_user_trace.signals.process_request`

Signaled before the view is called, during the `django-user-trace` middleware.

<small markdown>
**request**: `HttpRequest` &mdash; the Django HTTP request<br>
</small>

#### `#!py django_user_trace.signals.cleanup_request`

Signaled after the view has been called, during the `django-user-trace`
middleware.

<small markdown>
**request**: `HttpRequest` &mdash; the Django HTTP request<br>
</small>

[python:contextvars]: https://docs.python.org/3/library/contextvars.html
