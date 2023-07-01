from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from celery.signals import before_task_publish, task_postrun, task_prerun
from django.dispatch import receiver

from django_user_trace.context import user_attrs

if TYPE_CHECKING:
    from celery import Task

logger: logging.Logger = logging.getLogger(__name__)


@receiver(before_task_publish)
def on_before_task_publish(headers: dict[str, Any], **_kwargs: dict[str, Any]) -> None:
    """
    Adds user context to new Celery task headers.

    :param headers: Celery task headers
    """

    if attrs := user_attrs.get():
        logger.debug("received signal `before_task_publish`, adding `user` task header")
        headers["user"] = attrs


@receiver(task_prerun)
def on_task_prerun(task: Task, **_kwargs: dict[str, Any]) -> None:
    """
    Acquires user context from Celery task headers.

    :param task: Celery task
    """

    if (attrs := task.request.get("user")) and isinstance(attrs, dict):
        user_attrs.set(attrs)
        logger.debug("received signal `task_prerun`, setting `user_attrs` context var")


@receiver(task_postrun)
def on_task_postrun(task: Task, **_kwargs: dict[str, Any]) -> None:
    """
    Clears the user context after a Celery task has run.

    :param task: Celery task
    """

    if user_attrs.get() is not None:
        logger.debug("received signal `task_postrun`, clearing `user_attrs` context var")
        user_attrs.set(None)
