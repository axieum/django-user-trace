from types import SimpleNamespace

import pytest

from django_user_log.utils import rgetattr


def test_rgetattr_with_dict() -> None:
    """Tests the successful traversal of dictionaries during a recursive attribute lookup."""

    obj = {"a": {"d": "lorem ipsum"}, "b": {"e": 3.14}, "c": "dolor sit"}
    assert rgetattr(obj, "c") == "dolor sit"
    assert rgetattr(obj, "a__d") == "lorem ipsum"
    assert rgetattr(obj, "b__e") == 3.14
    with pytest.raises(KeyError, match="'z'"):
        rgetattr(obj, "z")


def test_rgetattr_with_object() -> None:
    """Tests the successful traversal of objects during a recursive attribute lookup."""

    obj = SimpleNamespace(a=1, b=2, c=3, d=SimpleNamespace(e=4, f=5), g=6)
    assert rgetattr(obj, "b") == 2
    assert rgetattr(obj, "d") == obj.d
    assert rgetattr(obj, "d__e") == 4
    assert rgetattr(obj, "d__f") == 5
    with pytest.raises(AttributeError, match="'types.SimpleNamespace' object has no attribute 'z'"):
        rgetattr(obj, "z")


def test_rgetattr_with_iterable() -> None:
    """Tests the successful traversal of lists during a recursive attribute lookup."""

    obj = ["a", "b", "c", (9, 8, 7), "d", "e"]
    assert rgetattr(obj, "1") == "b"
    assert rgetattr(obj, "3") == (9, 8, 7)
    assert rgetattr(obj, "3__1") == 8
    with pytest.raises(IndexError, match="list index out of range"):
        rgetattr(obj, "6")
    with pytest.raises(TypeError, match="list indices must be integers or slices, not str"):
        rgetattr(obj, "NaN")


def test_rgetattr_with_callable() -> None:
    """Tests that a callable is invoked when encountered during a recursive attribute lookup."""

    obj = {"a": {"c": lambda: {"d": "lorem ipsum", "e": "dolor sit"}}, "b": lambda o: o}
    assert rgetattr(obj, "a__c") == {"d": "lorem ipsum", "e": "dolor sit"}
    assert rgetattr(obj, "a__c__d") == "lorem ipsum"
    assert rgetattr(obj, "a__c__e") == "dolor sit"
    with pytest.raises(TypeError, match="missing 1 required positional argument: 'o'"):
        rgetattr(obj, "b")


def test_rgetattr_with_none_type() -> None:
    """Tests the successful traversal of nulls (i.e. `None`) during a recursive attribute lookup."""

    obj = {"a": {"c": None}, "b": None}
    assert rgetattr(obj, "a__c") is None
    assert rgetattr(obj, "b") is None
    with pytest.raises(AttributeError, match="'NoneType' object has no attribute 'x'"):
        rgetattr(obj, "b__x")


def test_rgetattr_default_value() -> None:
    """Tests that a default value is returned by a recursive attribute lookup when the attribute does not exist."""

    obj = {"a": {"e": "lorem ipsum"}, "b": {"f": 3.14}, "c": "dolor sit", "d": None}
    assert rgetattr(obj, "d") is None
    assert rgetattr(obj, "d__g", "xyz") == "xyz"
    assert rgetattr(obj, "6", "zyx") == "zyx"
    assert rgetattr(obj, "7", sentinel := object()) is sentinel


def test_rgetattr_custom_separator() -> None:
    """Tests that a recursive attribute lookup works with a custom query separator."""

    obj = {"a": {"d": "lorem ipsum"}, "b": {"e": 3.14}, "c__z": ["dolor sit"]}
    assert rgetattr(obj, "a.d", sep=".") == "lorem ipsum"
    assert rgetattr(obj, "c__z.0", sep=".") == "dolor sit"
    assert rgetattr(obj, "b//e", sep="//") == 3.14
