from __future__ import annotations

from typing import TYPE_CHECKING

from django_user_trace.context import user_attrs
from django_user_trace.contrib.celery.signals import (
    on_before_task_publish,
    on_task_postrun,
    on_task_prerun,
)

if TYPE_CHECKING:
    from unittest.mock import Mock

    from pytest_mock import MockerFixture


def test_on_before_task_publish_signal() -> None:
    """Tests that user context is added to new Celery task headers."""

    user_attrs.set({"username": "jane", "email": "jane.doe@localhost"})
    on_before_task_publish(headers := {"Correlation-ID": "abc"})
    assert headers == {
        "Correlation-ID": "abc",
        "User": {
            "username": "jane",
            "email": "jane.doe@localhost",
        },
    }


def test_on_before_task_publish_signal_without_user_context() -> None:
    """Tests that missing user context is *not* added to new Celery task headers."""

    user_attrs.set(None)
    on_before_task_publish(headers := {"Correlation-ID": "abc"})
    assert headers == {"Correlation-ID": "abc"}


def test_on_task_prerun_signal(mocker: MockerFixture) -> None:
    """Tests that user context is set when present in Celery task headers."""

    task: Mock = mocker.Mock()
    task.request = {"Correlation-ID": "asdf", "User": {"username": "john.doe"}}

    user_attrs.set(None)
    on_task_prerun(task)
    assert user_attrs.get() == {"username": "john.doe"}


def test_on_task_prerun_signal_without_user_context(mocker: MockerFixture) -> None:
    """Tests that user context is *not* set when missing from Celery task headers."""

    task: Mock = mocker.Mock()
    task.request = {"Correlation-ID": "asdf"}

    user_attrs.set(None)
    on_task_prerun(task)
    assert user_attrs.get() is None


def test_on_task_postrun_signal(mocker: MockerFixture) -> None:
    """Tests that user context is cleared."""

    task: Mock = mocker.Mock()
    task.request = {"Correlation-ID": "asdf", "User": {"username": "jonathan", "email": "jonathan@localhost"}}

    user_attrs.set(task.request)
    on_task_postrun(task)
    assert user_attrs.get() is None
