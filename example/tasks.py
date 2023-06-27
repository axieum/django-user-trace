"""Celery tasks for example project."""

from __future__ import annotations

from typing import TYPE_CHECKING

from celery.utils.log import get_task_logger
from example.celery import app

if TYPE_CHECKING:
    import logging

logger: logging.Logger = get_task_logger(__name__)


@app.task(name="add")
def add(x: int, y: int) -> int:
    """
    A task that adds two integers together and returns the result.

    :param x: first term
    :param y: second term
    :return: sum of the two terms
    """

    logger.info("will add %d and %d", x, y)
    return x + y
