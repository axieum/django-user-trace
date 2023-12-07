from functools import reduce
from typing import Any, Final

from django.db.models.constants import LOOKUP_SEP

SENTINEL: Final[object] = object()


def rgetattr(obj: Any, query: str, default: Any = SENTINEL, *, sep: str = LOOKUP_SEP) -> Any:
    """
    Recursively traverses a given object for an attribute, executing any callables in the path.

    :param obj: object to query
    :param query: attribute query path, e.g. 'user__username'
    :param sep: query attribute separator (default: '__')
    :param default: optional default value if the attribute does not exist
    :return: the attribute value if found
    :raise AttributeError: if the attribute could not be found, and no default was provided
    :raise TypeError: if an invalid iterable index is provided; or a callable with args is encountered
    """

    try:
        # Recursively lookup each part of the query string on the object
        val: Any = reduce(_resolve_attr, query.split(sep), obj)
    except (AttributeError, IndexError, KeyError):
        # Return the default if provided, otherwise re-raise the error
        if default is SENTINEL:
            raise
        return default
    else:
        # Return the found value or the provided default if no match
        return val if val is not SENTINEL else default


def _resolve_attr(obj: Any, attr: str) -> Any:
    """
    Returns a given attribute from a given object, invoking the result if callable.

    :param obj: object to query
    :param attr: attribute to retrieve
    :return: the attribute value
    :raise Exception: if unable to resolve the attribute
    """

    result: Any
    if obj is None:
        raise AttributeError(f"{type(obj).__name__!r} object has no attribute {attr!r}")
    elif hasattr(obj, "__getitem__"):
        result = obj[int(attr) if attr.isnumeric() else attr]
    else:
        result = getattr(obj, attr)
    return result() if callable(result) else result
