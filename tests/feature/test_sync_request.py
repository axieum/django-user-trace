from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.contrib.auth import get_user_model

if TYPE_CHECKING:
    from _pytest.logging import LogCaptureFixture
    from django.contrib.auth.models import User
    from django.test.client import Client


def test_anonymous_sync_request(client: Client, caplog: LogCaptureFixture) -> None:
    """Tests that logs during an unauthenticated sync request contain the *anonymous* user context."""

    # Fetch the index page
    client.get("/")

    # Expect the log messages to have Django's *anonymous* user context
    assert [(r.message, getattr(r, "username", None)) for r in caplog.records] == [
        ("sync middleware called", None),
        ("set `user_attrs` context var to {'username': None}", None),
        ("load `index_view` view", None),
        ("received signal `request_finished`, clearing `user_attrs` context var", None),
    ]


@pytest.mark.django_db(transaction=True)
def test_authenticated_sync_request(client: Client, caplog: LogCaptureFixture) -> None:
    """Tests that logs during an authenticated sync request contain the logged-in user context."""

    # Create a new user
    user: User = get_user_model().objects.create(
        username="jonathan", email="jonathan@localhost", first_name="Jonathan", last_name="Hiles"
    )

    # Fetch the index page
    client.force_login(user)
    client.get("/")

    # Expect the log messages to have the expected Django user context
    assert [(r.message, getattr(r, "username", None)) for r in caplog.records] == [
        ("sync middleware called", None),
        ("set `user_attrs` context var to {'username': 'jonathan'}", user.get_username()),
        ("load `index_view` view", user.get_username()),
        ("received signal `request_finished`, clearing `user_attrs` context var", user.get_username()),
    ]


@pytest.mark.django_db(transaction=True)
def test_multiple_authenticated_sync_requests(client: Client, caplog: LogCaptureFixture) -> None:
    """Tests that the user context from an authenticated sync request does not bleed into other request logs."""

    # Create new users
    users: tuple[User, ...] = (
        # Jane Doe
        get_user_model().objects.create(username="jane", email="jane@localhost", first_name="Jane", last_name="Doe"),
        # John Doe
        get_user_model().objects.create(username="john", email="john@localhost", first_name="John", last_name="Doe"),
    )

    # Fetch the index page as each user
    for user in users:
        client.force_login(user)
        client.get("/")

    # Expect the log messages to have the expected Django user context
    assert [(r.message, getattr(r, "username", None)) for r in caplog.records] == [
        entry
        for user in users
        for entry in (
            ("sync middleware called", None),  # user attributes from prior requests should not remain afterwards
            (f"set `user_attrs` context var to {{'username': '{user.get_username()}'}}", user.get_username()),
            ("load `index_view` view", user.get_username()),
            ("received signal `request_finished`, clearing `user_attrs` context var", user.get_username()),
        )
    ]
