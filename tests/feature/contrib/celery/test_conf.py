from __future__ import annotations

from typing import TYPE_CHECKING

import pytest
from django.contrib.auth import get_user_model

from django_user_trace.conf import Settings

if TYPE_CHECKING:
    from _pytest.monkeypatch import MonkeyPatch
    from celery.worker import WorkController
    from django.contrib.auth.models import AbstractUser
    from django.test import Client
    from pytest import LogCaptureFixture
    from pytest_django.fixtures import SettingsWrapper


@pytest.mark.django_db(transaction=True)
def test_custom_celery_task_header(
    client: Client,
    settings: SettingsWrapper,
    caplog: LogCaptureFixture,
    monkeypatch: MonkeyPatch,
    celery_worker: WorkController,
) -> None:
    """Tests that Celery tasks have the correct header added for tracing user context."""

    # Set the Celery task header setting in Django settings
    settings.DJANGO_USER_TRACE = {"CELERY_TASK_HEADER": "X-User-Context"}
    monkeypatch.setattr("django_user_trace.contrib.celery.signals.settings", Settings())

    # Create a new user
    user: AbstractUser = get_user_model().objects.create(
        username="jonathan", email="jonathan@localhost", first_name="Jonathan", last_name="Hiles"
    )

    # Fetch the delay page
    client.force_login(user)
    client.get("/delay/")

    # Expect the log messages to have the expected Django user context and Celery task header
    assert [(r.message, getattr(r, "username", None)) for r in caplog.records] == [
        ("sync middleware called", None),
        ("set `user_attrs` context var to {'username': 'jonathan'}", user.get_username()),
        ("load `delay_view` view", user.get_username()),
        # BEGIN `django_user_trace.contrib.celery` integration
        ("received signal `before_task_publish`, adding `X-User-Context` task header", user.get_username()),
        ("received signal `task_prerun`, setting `user_attrs` context var", user.get_username()),
        ("will add 1 and 9", user.get_username()),
        ("received signal `task_postrun`, clearing `user_attrs` context var", user.get_username()),
        # END `django_user_trace.contrib.celery` integration
        ("received signal `request_finished`, clearing `user_attrs` context var", user.get_username()),
    ]
