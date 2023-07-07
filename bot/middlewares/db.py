from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.db.repository import (
    ResponseRepository,
    UploadedImageRepository,
)


class DBSessionMiddleware(BaseMiddleware):
    """Outer middleware to obtain session and repositories in context."""

    def __init__(self, sm: async_sessionmaker):
        """Initialize with sessionmaker."""
        super().__init__()
        self.sessionmaker = sm

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ):
        """Put repositories in context when middleware calls."""
        async with self.sessionmaker() as session:
            data["session"] = session
            data["responses_repo"] = ResponseRepository(session)
            data["uploaded_images_repo"] = UploadedImageRepository(session)
            return await handler(event, data)
