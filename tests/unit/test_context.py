from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.contrib.auth import get_user_model

from django_user_trace.conf import Settings
from django_user_trace.context import build_user_attrs, get_user_attrs, user_attrs

if TYPE_CHECKING:
    from _pytest.monkeypatch import MonkeyPatch
    from django.contrib.auth.base_user import AbstractBaseUser
    from pytest_django.fixtures import SettingsWrapper
    from starlette.types import Scope


def test_set_and_get_user_attrs() -> None:
    """Tests that the Django user attributes currently in use can be retrieved."""

    assert user_attrs.get() is get_user_attrs() is None
    user_attrs.set(val := {"username": "John Doe"})
    assert user_attrs.get() is get_user_attrs() is val


@pytest.mark.django_db(transaction=True)
def test_build_user_attrs(settings: SettingsWrapper, monkeypatch: MonkeyPatch) -> None:
    """Tests that all configured user attributes are constructed into a user attributes mappings."""

    # Set multiple user attributes to log in Django settings
    settings.DJANGO_USER_TRACE = {
        "USER_ATTRS": {"username": "get_username", "email": "email"},
    }
    monkeypatch.setattr("django_user_trace.log.settings", new_settings := Settings())
    monkeypatch.setattr("django_user_trace.context.settings", new_settings)

    # Create a new user
    user: AbstractBaseUser = get_user_model().objects.create(
        username=(username := "jonathan"), email=(email := "jonathan@localhost"), first_name="Jon", last_name="Hiles"
    )

    # Build the user attributes mapping
    scope: Scope = {"type": "http", "user": user}

    # Expect the captured user attributes match
    assert build_user_attrs(scope, user) == {"username": username, "email": email}
