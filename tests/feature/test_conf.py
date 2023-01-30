from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest
from django.contrib.auth import get_user_model

from django_user_log.conf import Settings

if TYPE_CHECKING:
    from _pytest.logging import LogCaptureFixture
    from _pytest.monkeypatch import MonkeyPatch
    from django.contrib.auth.models import AbstractUser
    from django.http import HttpRequest
    from django.test.client import Client
    from pytest_django.fixtures import SettingsWrapper


@pytest.mark.django_db(transaction=True)
def test_log_multiple_attrs_of_user(
    client: Client, settings: SettingsWrapper, caplog: LogCaptureFixture, monkeypatch: MonkeyPatch
) -> None:
    """Tests that all configured user attributes are logged successfully for an authenticated user."""

    # Set multiple user attributes to log in Django settings
    settings.DJANGO_USER_LOG = {
        "USER_ATTRS": {"username": "get_username", "email": "email"},
    }
    monkeypatch.setattr("django_user_log.log.settings", new_settings := Settings())
    monkeypatch.setattr("django_user_log.middleware.settings", new_settings)

    # Create a new user
    user: AbstractUser = get_user_model().objects.create(
        username=(username := "matthew"), email=(email := "matthew@localhost"), first_name="Matthew", last_name="Hiles"
    )

    # Fetch the index page
    client.force_login(user)
    client.get("/")

    # Expect the log messages to have Django's *anonymous* user context
    assert [(r.message, getattr(r, "username", None), getattr(r, "email", None)) for r in caplog.records] == [
        ("sync middleware called", None, None),
        ("set `user_attrs` context var to {'username': 'matthew', 'email': 'matthew@localhost'}", username, email),
        ("load `index_view` view", username, email),
        ("received signal `request_finished`, clearing `user_attrs` context var", username, email),
    ]


def test_log_multiple_attrs_of_anonymous_user(
    client: Client, settings: SettingsWrapper, caplog: LogCaptureFixture, monkeypatch: MonkeyPatch
) -> None:
    """Tests that all configured user attributes are logged successfully for an anonymous user."""

    # Set multiple user attributes to log in Django settings
    settings.DJANGO_USER_LOG = {
        "USER_ATTRS": {"username": "get_username", "email": "email"},
    }
    monkeypatch.setattr("django_user_log.log.settings", new_settings := Settings())
    monkeypatch.setattr("django_user_log.middleware.settings", new_settings)

    # Fetch the index page
    client.get("/")

    # Expect the log messages to have Django's *anonymous* user context
    assert [(r.message, getattr(r, "username", None), getattr(r, "email", None)) for r in caplog.records] == [
        ("sync middleware called", None, None),
        ("set `user_attrs` context var to {'username': None, 'email': None}", None, None),
        ("load `index_view` view", None, None),
        ("received signal `request_finished`, clearing `user_attrs` context var", None, None),
    ]


@pytest.mark.django_db(transaction=True)
def test_log_result_of_custom_callable_for_user(
    client: Client, settings: SettingsWrapper, caplog: LogCaptureFixture, monkeypatch: MonkeyPatch
) -> None:
    """Tests that the result of a custom callable configured as a user attribute is logged successfully."""

    def get_custom_attribute(auth_user: AbstractUser, _request: HttpRequest) -> Any:
        return f"Mr. {auth_user.get_short_name()}"

    # Set a custom callable as a user attribute to log in Django settings
    settings.DJANGO_USER_LOG = {
        "USER_ATTRS": {"username": "get_username", "custom": get_custom_attribute},
    }
    monkeypatch.setattr("django_user_log.log.settings", new_settings := Settings())
    monkeypatch.setattr("django_user_log.middleware.settings", new_settings)

    # Create a new user with a unique mark
    user: AbstractUser = get_user_model().objects.create(
        username="jonathan", email="jonathan@localhost", first_name="Jonathan", last_name="Hiles"
    )

    # Fetch the index page
    client.force_login(user)
    client.get("/")

    # Expect the log messages to have Django's *anonymous* user context
    custom_value: str = "Mr. Jonathan"
    assert [(r.message, getattr(r, "custom", None)) for r in caplog.records] == [
        ("sync middleware called", None),
        ("set `user_attrs` context var to {'username': 'jonathan', 'custom': 'Mr. Jonathan'}", custom_value),
        ("load `index_view` view", custom_value),
        ("received signal `request_finished`, clearing `user_attrs` context var", custom_value),
    ]
