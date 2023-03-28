from __future__ import annotations

from django_user_trace.context import get_user_attrs, user_attrs


def test_set_and_get_user_attrs() -> None:
    """Tests that the Django user attributes currently in use can be retrieved."""

    assert user_attrs.get() is get_user_attrs() is None
    user_attrs.set(val := {"username": "John Doe"})
    assert user_attrs.get() is get_user_attrs() is val
