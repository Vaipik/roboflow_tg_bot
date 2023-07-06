from typing import Callable, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from sqlalchemy.ext.asyncio import async_sessionmaker

from bot.db.repository.responses import ResponseRepository


class DBSessionMiddleware(BaseMiddleware):
    def __init__(self, sm: async_sessionmaker):
        super().__init__()
        self.sessionmaker = sm

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ):
        async with self.sessionmaker() as session:
            data["session"] = session
            data["responses_repo"] = ResponseRepository(session)
            return await handler(event, data)
