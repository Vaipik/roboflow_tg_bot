import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.config import cfg
from bot.handlers import common_router, recognition_router, response_router
from bot.middlewares.db import DBSessionMiddleware
from bot.ui_commands import bot_set_commands
from bot.utils import initialize_roboflow

logger = logging.getLogger(__name__)


async def main():
    engine = create_async_engine(
        f"postgresql+asyncpg://{cfg.db.user}:{cfg.db.password}@{cfg.db.host}:{cfg.db.port}/{cfg.db.name}",
        echo=True
    )

    sessionmakeer = async_sessionmaker(engine, expire_on_commit=False)

    bot = Bot(token=cfg.bot_token.get_secret_value(), parse_mode="HTML")

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(common_router)
    dp.include_router(recognition_router)
    dp.include_router(response_router)

    dp.update.middleware(DBSessionMiddleware(sm=sessionmakeer))

    roboflow_api = initialize_roboflow(cfg.roboflow, cfg.bot_token.get_secret_value())
    await bot_set_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, roboflow_api=roboflow_api)


if __name__ == '__main__':
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    asyncio.run(main())
