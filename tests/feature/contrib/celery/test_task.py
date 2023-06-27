from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.contrib.auth import get_user_model

if TYPE_CHECKING:
    from celery.worker import WorkController
    from django.contrib.auth.models import AbstractUser
    from django.test import Client
    from pytest import LogCaptureFixture


def test_anonymous_sync_request(client: Client, caplog: LogCaptureFixture, celery_worker: WorkController) -> None:
    """Tests that Celery logs during an unauthenticated sync request contain the *anonymous* user context."""

    # Fetch the delay page
    client.get("/delay/")

    # Expect the log messages to have Django's *anonymous* user context
    assert [(r.message, getattr(r, "username", None)) for r in caplog.records] == [
        ("sync middleware called", None),
        ("set `user_attrs` context var to {'username': None}", None),
        ("load `delay_view` view", None),
        # BEGIN `django_user_trace.contrib.celery` integration
        ("received signal `before_task_publish`, adding `user` task header", None),
        ("received signal `task_prerun`, setting `user_attrs` context var", None),
        ("will add 1 and 9", None),
        ("received signal `task_postrun`, clearing `user_attrs` context var", None),
        # END `django_user_trace.contrib.celery` integration
        ("received signal `request_finished`, clearing `user_attrs` context var", None),
    ]


@pytest.mark.django_db(transaction=True)
def test_authenticated_sync_request(client: Client, caplog: LogCaptureFixture, celery_worker: WorkController) -> None:
    """Tests that Celery logs during an authenticated sync request contain the logged-in user context."""

    # Create a new user
    user: AbstractUser = get_user_model().objects.create(
        username="jonathan", email="jonathan@localhost", first_name="Jonathan", last_name="Hiles"
    )

    # Fetch the delay page
    client.force_login(user)
    client.get("/delay/")

    # Expect the log messages to have the expected Django user context
    assert [(r.message, getattr(r, "username", None)) for r in caplog.records] == [
        ("sync middleware called", None),
        ("set `user_attrs` context var to {'username': 'jonathan'}", user.get_username()),
        ("load `delay_view` view", user.get_username()),
        # BEGIN `django_user_trace.contrib.celery` integration
        ("received signal `before_task_publish`, adding `user` task header", user.get_username()),
        ("received signal `task_prerun`, setting `user_attrs` context var", user.get_username()),
        ("will add 1 and 9", user.get_username()),
        ("received signal `task_postrun`, clearing `user_attrs` context var", user.get_username()),
        # END `django_user_trace.contrib.celery` integration
        ("received signal `request_finished`, clearing `user_attrs` context var", user.get_username()),
    ]
