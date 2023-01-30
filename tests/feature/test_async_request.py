from __future__ import annotations

import asyncio
from copy import deepcopy
from typing import TYPE_CHECKING

import pytest
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model

if TYPE_CHECKING:
    from _pytest.logging import LogCaptureFixture
    from django.contrib.auth.models import AbstractUser
    from django.http import HttpResponseBase
    from django.test.client import AsyncClient


async def test_anonymous_async_request(async_client: AsyncClient, caplog: LogCaptureFixture) -> None:
    """Tests that logs during an unauthenticated async request contain the *anonymous* user context."""

    # Fetch the index page
    await async_client.get("/")

    # Expect the log messages to have Django's *anonymous* user context
    assert [(r.message, getattr(r, "username", None)) for r in caplog.records] == [
        ("async middleware called", None),
        ("set `user_attrs` context var to {'username': None}", None),
        ("load `index_view` view", None),
        ("received signal `request_finished`, clearing `user_attrs` context var", None),
    ]


@pytest.mark.django_db(transaction=True)
async def test_authenticated_async_request(async_client: AsyncClient, caplog: LogCaptureFixture) -> None:
    """Tests that logs during an authenticated async request contain the logged-in user context."""

    # Create a new user
    user: AbstractUser = await sync_to_async(get_user_model().objects.create)(
        username=(username := "jonathan"), email="jonathan@localhost", first_name="Jonathan", last_name="Hiles"
    )

    # Fetch the index page
    await sync_to_async(async_client.force_login)(user)
    await async_client.get("/")

    # Expect the log messages to have the expected Django user context
    assert [(r.message, getattr(r, "username", None)) for r in caplog.records] == [
        ("async middleware called", None),
        (f"set `user_attrs` context var to {{'username': '{username}'}}", username),
        ("load `index_view` view", username),
        ("received signal `request_finished`, clearing `user_attrs` context var", username),
    ]


@pytest.mark.django_db(transaction=True)
async def test_concurrent_authenticated_async_requests(async_client: AsyncClient, caplog: LogCaptureFixture) -> None:
    """Tests that the user context from an authenticated async request does not bleed into other request logs."""

    # Create new users
    users: tuple[AbstractUser, ...] = await asyncio.gather(
        # Jane Doe
        sync_to_async(get_user_model().objects.create)(
            username="jane", email="jane@localhost", first_name="Jane", last_name="Doe"
        ),
        # John Doe
        sync_to_async(get_user_model().objects.create)(
            username="john", email="john@localhost", first_name="John", last_name="Doe"
        ),
        # Jonathan Hiles
        sync_to_async(get_user_model().objects.create)(
            username="jonathan", email="jonathan@localhost", first_name="Jonathan", last_name="Hiles"
        ),
    )

    # Fetch the index page as each user concurrently
    async def _async_request(login_as: AbstractUser) -> HttpResponseBase:
        _async_client: AsyncClient = deepcopy(async_client)
        await sync_to_async(_async_client.force_login)(login_as)
        return await _async_client.get("/")

    await asyncio.gather(*(_async_request(user) for user in users))

    # Expect the log messages to have the expected Django user context
    assert sorted([(r.message, getattr(r, "username", None)) for r in caplog.records]) == sorted(
        [
            entry
            for user in users
            for entry in (
                ("async middleware called", None),  # user attributes from prior requests should not remain afterwards
                (f"set `user_attrs` context var to {{'username': '{user.get_username()}'}}", user.get_username()),
                ("load `index_view` view", user.get_username()),
                ("received signal `request_finished`, clearing `user_attrs` context var", user.get_username()),
            )
        ]
    )
