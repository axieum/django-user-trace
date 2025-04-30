from __future__ import annotations

import asyncio
from typing import TYPE_CHECKING

import pytest
from channels.testing import HttpCommunicator
from django.contrib.auth import get_user_model
from example.asgi import application

if TYPE_CHECKING:
    from _pytest.logging import LogCaptureFixture
    from django.contrib.auth.base_user import AbstractBaseUser


async def test_anonymous_asgi_request(caplog: LogCaptureFixture) -> None:
    """Tests that logs during an unauthenticated ASGI request contain the *anonymous* user context."""

    # Fetch the index page
    await HttpCommunicator(application, method="GET", path="/asgi/").get_response()

    # Expect the log messages to have Django's *anonymous* user context
    assert [(r.message, getattr(r, "username", None)) for r in caplog.records] == [
        ("asgi middleware called", None),
        ("set `user_attrs` context var to {'username': None}", None),
        ("load `index_asgi` view", None),
    ]


@pytest.mark.django_db(transaction=True)
async def test_authenticated_asgi_request(caplog: LogCaptureFixture) -> None:
    """Tests that logs during an authenticated ASGI request contain the logged-in user context."""

    # Create a new user
    user: AbstractBaseUser = await get_user_model().objects.acreate(
        username=(username := "jonathan"), email="jonathan@localhost", first_name="Jonathan", last_name="Hiles"
    )

    # Fetch the index page
    communicator = HttpCommunicator(application, method="GET", path="/asgi/")
    communicator.scope["user"] = user
    await communicator.get_response()

    # Expect the log messages to have the expected Django user context
    assert [(r.message, getattr(r, "username", None)) for r in caplog.records] == [
        ("asgi middleware called", None),
        (f"set `user_attrs` context var to {{'username': '{username}'}}", username),
        ("load `index_asgi` view", username),
    ]


@pytest.mark.django_db(transaction=True)
async def test_concurrent_authenticated_asgi_requests(caplog: LogCaptureFixture) -> None:
    """Tests that the user context from an authenticated ASGI request does not bleed into other request logs."""

    # Create new users
    users: tuple[AbstractBaseUser, ...] = await asyncio.gather(
        # Jane Doe
        get_user_model().objects.acreate(username="jane", email="jane@localhost", first_name="Jane", last_name="Doe"),
        # John Doe
        get_user_model().objects.acreate(username="john", email="john@localhost", first_name="John", last_name="Doe"),
        # Jonathan Hiles
        get_user_model().objects.acreate(
            username="jonathan", email="jonathan@localhost", first_name="Jonathan", last_name="Hiles"
        ),
    )

    # Fetch the index page as each user concurrently
    async def _async_request(login_as: AbstractBaseUser) -> None:
        communicator = HttpCommunicator(application, method="GET", path="/asgi/")
        communicator.scope["user"] = login_as
        await communicator.get_response()

    await asyncio.gather(*(_async_request(user) for user in users))

    # Expect the log messages to have the expected Django user context
    assert sorted([(r.message, getattr(r, "username", None)) for r in caplog.records]) == sorted(
        [
            entry
            for user in users
            for entry in (
                ("asgi middleware called", None),  # user attributes from prior requests should not remain afterward
                (f"set `user_attrs` context var to {{'username': '{user.get_username()}'}}", user.get_username()),
                ("load `index_asgi` view", user.get_username()),
            )
        ]
    )
