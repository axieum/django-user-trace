<div align="center">

# `django-user-trace`

A Python [logging][python:logging] filter for [Django][django] user attributes

[![Build](https://img.shields.io/github/actions/workflow/status/axieum/django-user-trace/release.yml?branch=main&style=flat-square)][ci:release]
[![Coverage](https://img.shields.io/codecov/c/github/axieum/django-user-trace?style=flat-square)][codecov]
[![Python](https://img.shields.io/pypi/pyversions/django-user-trace?style=flat-square)][python]
[![PyPI](https://img.shields.io/pypi/v/django-user-trace?style=flat-square&include_prereleases&sort=semver)][pypi]

</div>

`django-user-trace` provides a Python [logging][python:logging] filter that
injects attributes from the currently logged in [Django][django] user.

It uses a [`ContextVar`][python:contextvars] to store user attributes for use on
the current thread. These are then injected into all log records via a logging
filter.

_[Visit the documentation][docs]._

```mermaid
sequenceDiagram
    actor User
    User ->>+ django: make request
    django ->>+ django.contrib.auth: AuthenticationMiddleware
    django.contrib.auth ->>+ django: set `request.user`
    django ->>+ django_user_trace: django_user_trace_middleware
    note over django, django_user_trace: Capture relevant user attributes into a `ContextVar`
    django_user_trace ->>+ django: continue
    django --> logging: log message
    logging ->>+ django_user_trace: get user attrs
    django_user_trace -->> logging: `ContextVar` for user attrs
    django ->>+ django_user_trace: signal `request_finished`
    note over django, django_user_trace: Clear user attributes from the `ContextVar`
    django_user_trace ->>+ django: continue
    django -->> User: send response
```

#### Resources

* [Django &mdash; How to configure and use logging][django:logging]

#### Related Projects

* [madzak/python-json-logger][python-json-logger]
* [snok/django-guid][django-guid]

## Installation

Install via `pip`:

```shell
pip install django-user-trace
```

Or, via [`poetry`][poetry]:

```shell
poetry add django-user-trace
```

## Contributing

Thank you for considering contributing to `django-user-trace`! Please see the
[Contribution Guidelines][contributing].

## Security Vulnerabilities

Please review the [Security Policy][security] on how to report security
vulnerabilities.

## Licence

`django-user-trace` is open-sourced software licenced under the
[MIT licence][licence].

[ci:release]: https://github.com/axieum/django-user-trace/actions/workflows/release.yml
[ci:test]: https://github.com/axieum/django-user-trace/actions/workflows/test.yml
[codecov]: https://app.codecov.io/gh/axieum/django-user-trace
[contributing]: CONTRIBUTING.md
[django]: https://djangoproject.com/
[django:logging]: https://docs.djangoproject.com/en/stable/howto/logging/
[django-guid]: https://github.com/snok/django-guid
[docs]: https://axieum.github.io/django-user-trace
[licence]: https://opensource.org/licenses/MIT
[poetry]: https://python-poetry.org/
[pypi]: https://pypi.org/project/django-user-trace
[python]: https://python.org/
[python:contextvars]: https://docs.python.org/3/library/contextvars.html
[python:logging]: https://docs.python.org/3/library/logging.html
[python-json-logger]: https://github.com/madzak/python-json-logger
[security]: SECURITY.md
