from __future__ import annotations

import logging

from channels.generic.http import AsyncHttpConsumer

logger: logging.Logger = logging.getLogger(__name__)


class IndexHttpConsumer(AsyncHttpConsumer):  # type: ignore[misc]
    """ASGI index page that logs a message."""

    async def handle(self, body: bytes) -> None:
        logger.info(
            "load `index_asgi` view", extra={"view": f"{IndexHttpConsumer.__module__}.{IndexHttpConsumer.__name__}"}
        )
        await self.send_response(200, b'{"status": "ok"}', headers=[(b"content-type", b"application/json")])
