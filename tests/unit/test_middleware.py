from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.core.exceptions import ImproperlyConfigured

if TYPE_CHECKING:
    from django.test.client import Client
    from pytest_django.fixtures import SettingsWrapper


def test_incorrect_middleware_order(client: Client, settings: SettingsWrapper) -> None:
    """
    Tests that registering the `django_user_trace_middleware` middleware before Django's `AuthenticationMiddleware`
    raises an error.
    """

    settings.MIDDLEWARE = [
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django_user_trace.middleware.django_user_trace_middleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
    ]

    with pytest.raises(
        ImproperlyConfigured,
        match=(
            "The django-user-trace middleware requires authentication middleware to be installed. "
            "Edit your MIDDLEWARE setting to insert 'django.contrib.auth.middleware.AuthenticationMiddleware' "
            "before 'django_user_trace.middleware.django_user_trace_middleware'."
        ),
    ):
        client.get("/")
