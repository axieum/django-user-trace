from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Awaitable, Callable, Union

from asgiref.sync import sync_to_async
from django.core.exceptions import ImproperlyConfigured
from django.utils.decorators import sync_and_async_middleware

from django_user_trace.conf import settings
from django_user_trace.context import user_attrs
from django_user_trace.utils import rgetattr

if TYPE_CHECKING:
    from django.http import HttpRequest, HttpResponse

    GetResponseCallable = Callable[[HttpRequest], Union[HttpResponse, Awaitable[HttpResponse]]]


logger: logging.Logger = logging.getLogger(__name__)


def process_request(request: HttpRequest) -> None:
    """
    Process an incoming HTTP request.

    :param request: http request
    """

    # Check that authentication has been performed by an earlier middleware
    if not hasattr(request, "user"):
        raise ImproperlyConfigured(
            "The django-user-trace middleware requires authentication middleware to be installed. "
            "Edit your MIDDLEWARE setting to insert 'django.contrib.auth.middleware.AuthenticationMiddleware' "
            "before 'django_user_trace.middleware.django_user_trace_middleware'."
        )

    # Capture any necessary user attributes for use in log messages
    user_attrs.set(
        {
            key: (
                val
                if (val := lookup(request.user, request) if callable(lookup) else rgetattr(request.user, lookup, None))
                not in (None, "")
                else None
            )
            for key, lookup in settings.USER_ATTRS.items()
        }
    )
    logger.debug("set `user_attrs` context var to %s", user_attrs.get())


@sync_and_async_middleware
def django_user_trace_middleware(get_response: GetResponseCallable) -> GetResponseCallable:
    """
    Observes the Django user context of a request for use in Python's logging framework.

    :param get_response: next callable for the http response
    :return: middleware callable
    """

    # async middleware
    if asyncio.iscoroutinefunction(get_response):

        async def middleware(request: HttpRequest) -> HttpResponse:
            logger.debug("async middleware called")
            if hasattr(request, "user"):
                await sync_to_async(request.user._setup)()  # type: ignore
            process_request(request)
            return await get_response(request)  # type: ignore

    # sync middleware
    else:

        def middleware(request: HttpRequest) -> HttpResponse:  # type: ignore[misc]
            logger.debug("sync middleware called")
            process_request(request)
            return get_response(request)  # type: ignore

    return middleware
