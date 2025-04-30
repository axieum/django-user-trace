from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING

from django.core.exceptions import ImproperlyConfigured
from django.utils.decorators import sync_and_async_middleware

from django_user_trace.context import build_user_attrs, user_attrs
from django_user_trace.signals import cleanup_request, process_request

if TYPE_CHECKING:
    from collections.abc import Awaitable, Callable

    from django.contrib.auth.models import AbstractBaseUser, AnonymousUser
    from django.http import HttpRequest, HttpResponse

    GetResponseCallable = Callable[[HttpRequest], HttpResponse | Awaitable[HttpResponse]]


logger: logging.Logger = logging.getLogger(__name__)


def process_incoming_request(request: HttpRequest, user: AbstractBaseUser | AnonymousUser | None = None) -> None:
    """
    Processes an incoming HTTP request.

    :param request: http request
    :param user: Django user
    """

    # Check that authentication has been performed by earlier middleware
    if not user:
        raise ImproperlyConfigured(
            "The django-user-trace middleware requires authentication middleware to be installed. "
            "Edit your MIDDLEWARE setting to insert 'django.contrib.auth.middleware.AuthenticationMiddleware' "
            "before 'django_user_trace.middleware.django_user_trace_middleware'."
        )

    # Capture any necessary user attributes for use in log messages
    user_attrs.set(attrs := build_user_attrs(request, user))
    logger.debug("set `user_attrs` context var to %s", attrs)

    # Send a signal
    process_request.send(django_user_trace_middleware, request=request)


def process_outgoing_request(request: HttpRequest) -> None:
    """
    Processes an outgoing HTTP request.

    :param request: http request
    """

    # Send a signal
    cleanup_request.send(django_user_trace_middleware, request=request)


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
            process_incoming_request(request, await request.auser() if hasattr(request, "auser") else None)
            res: HttpResponse = await get_response(request)
            process_outgoing_request(request)
            return res

    # sync middleware
    else:

        def middleware(request: HttpRequest) -> HttpResponse:  # type: ignore[misc]
            logger.debug("sync middleware called")
            process_incoming_request(request, getattr(request, "user", None))
            res: HttpResponse = get_response(request)  # type: ignore
            process_outgoing_request(request)
            return res

    return middleware
