from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

if TYPE_CHECKING:
    from pytest_django.fixtures import SettingsWrapper


@pytest.fixture(autouse=True)
def install_django_user_trace_celery_app(settings: SettingsWrapper) -> None:
    """Installs the `django_user_trace.contrib.celery` app to Django settings."""

    settings.INSTALLED_APPS += ["django_user_trace.contrib.celery"]
