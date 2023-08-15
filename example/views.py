"""Django views for example project."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from django.http import JsonResponse

from example import tasks

if TYPE_CHECKING:
    from django.http import HttpRequest


logger: logging.Logger = logging.getLogger(__name__)


def index_view(_request: HttpRequest) -> JsonResponse:
    """
    Index page that logs a message.

    :param _request: http request
    :return: json response
    """

    logger.info("load `index_view` view", extra={"view": f"{index_view.__module__}.{index_view.__name__}"})
    return JsonResponse({"status": "ok"})


async def aindex_view(_request: HttpRequest) -> JsonResponse:
    """
    Async index page that logs a message.

    :param _request: http request
    :return: json response
    """

    logger.info("load `aindex_view` view", extra={"view": f"{aindex_view.__module__}.{aindex_view.__name__}"})
    return JsonResponse({"status": "ok"})


def task_add_view(_request: HttpRequest) -> JsonResponse:
    """
    A view that defers a Celery task.

    :param _request: http request
    :return: json response
    """

    logger.info("load `task_add_view` view", extra={"view": f"{task_add_view.__module__}.{task_add_view.__name__}"})
    result: int = tasks.add.delay(1, 9).get()
    return JsonResponse({"status": "ok", "detail": result})
