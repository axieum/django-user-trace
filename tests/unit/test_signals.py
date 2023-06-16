from __future__ import annotations

from typing import TYPE_CHECKING

import django_user_trace.signals
from django_user_trace.middleware import django_user_trace_middleware

if TYPE_CHECKING:
    from django.test.client import Client
    from pytest_mock import MockerFixture


def test_process_request_signal(client: Client, mocker: MockerFixture) -> None:
    """Tests that the `django_user_trace.signals.process_request` signal is dispatched."""

    signal_send_spy = mocker.spy(django_user_trace.signals.process_request, "send")
    res = client.get("/")
    signal_send_spy.assert_called_with(sender=django_user_trace_middleware, request=res.wsgi_request)


def test_cleanup_request_signal(client: Client, mocker: MockerFixture) -> None:
    """Tests that the `django_user_trace.signals.cleanup_request` signal is dispatched."""

    signal_send_spy = mocker.spy(django_user_trace.signals.cleanup_request, "send")
    res = client.get("/")
    signal_send_spy.assert_called_with(sender=django_user_trace_middleware, request=res.wsgi_request)
