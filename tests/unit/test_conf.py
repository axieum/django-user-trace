from __future__ import annotations

from typing import TYPE_CHECKING, Any

import pytest
from django.core.exceptions import ImproperlyConfigured

from django_user_trace.conf import Settings
from django_user_trace.context import get_user_attrs

if TYPE_CHECKING:
    from pytest_django.fixtures import SettingsWrapper


def test_default_settings(settings: SettingsWrapper) -> None:
    """Tests that the default settings are loaded correctly."""

    # Remove user-defined setting from Django settings
    del settings.DJANGO_USER_TRACE

    # Instantiate a new django-user-trace settings instance
    Settings()


def test_user_defined_settings(settings: SettingsWrapper) -> None:
    """Tests that user-defined settings are loaded correctly."""

    # Set sensible user-defined settings in Django settings
    settings.DJANGO_USER_TRACE = {
        "USER_ATTRS": {"username": "get_username", "email": "email"},
    }

    # Instantiate a new django-user-trace settings instance
    new_settings: Settings = Settings()

    # Check that our user-defined settings are present
    for setting, value in settings.DJANGO_USER_TRACE.items():
        assert getattr(new_settings, setting, None) == value


def test_invalid_user_defined_setting(settings: SettingsWrapper) -> None:
    """Tests that an invalid user-defined setting raises an error on load."""

    # Set an invalid user-defined setting in Django settings
    settings.DJANGO_USER_TRACE = {
        "USER_ATTRS": {"email": "email"},
        "INVALID_OPTION": False,  # <- ERRONEOUS
    }

    # Instantiate a new django-user-trace settings instance and expect an error
    with pytest.raises(ImproperlyConfigured, match="'INVALID_OPTION' is not a valid django-user-trace setting."):
        Settings()


def test_user_attr_import_string(settings: SettingsWrapper) -> None:
    """Tests that a user attribute setting with a valid import path is successfully imported on load."""

    # Set a valid user attribute import path in Django settings
    settings.DJANGO_USER_TRACE = {"USER_ATTRS": {"username": "ext://django_user_trace.context.get_user_attrs"}}

    # Instantiate a new django-user-trace settings instance
    new_settings = Settings()

    # Check that our user attribute callable was resolved
    assert new_settings.USER_ATTRS["username"] == get_user_attrs  # type: ignore


def test_invalid_user_attr_import_string(settings: SettingsWrapper) -> None:
    """Tests that a user attribute setting with an invalid import path raises an error on load."""

    # Set an invalid user attribute import path in Django settings
    settings.DJANGO_USER_TRACE = {
        "USER_ATTRS": {
            "email": "email",
            "username": "ext://invalid.module.func",  # <- ERRONEOUS
        },
    }

    # Instantiate a new django-user-trace settings instance and expect an error
    with pytest.raises(ImproperlyConfigured, match="Cannot import django-user-trace user attribute 'username'."):
        Settings()


@pytest.mark.parametrize(
    "type_name, value",
    [
        ("<class 'bool'>", False),
        ("<class 'float'>", 3.14),
        (r"<class '.*ContextVar'>", "ext://django_user_trace.context.user_attrs"),
    ],
)
def test_invalid_user_attr_type(type_name: str, value: Any, settings: SettingsWrapper) -> None:
    """Tests that a user attribute setting with an invalid type raises an error on load."""

    # Set the invalid user attribute value in Django settings
    settings.DJANGO_USER_TRACE = {"USER_ATTRS": {"username": value}}

    # Instantiate a new django-user-trace settings instance and expect an error
    with pytest.raises(
        ImproperlyConfigured,
        match=f"Expected a string or callable for django-user-trace user attribute 'username' but got '{type_name}'.",
    ):
        Settings()
