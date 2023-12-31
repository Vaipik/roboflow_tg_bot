import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from bot.config import load_confg
from bot.handlers import common_router, recognition_router, response_router
from bot.middlewares.db import DBSessionMiddleware
from bot.ui_commands import bot_set_commands
from bot.utils import roboflow_service, on_startup


async def main():
    """Entry point for application."""
    cfg = load_confg()
    db = cfg.db
    engine = create_async_engine(
        f"postgresql+asyncpg://{db.user}:{db.password}@{db.host}:{db.port}/{db.name}",
    )

    sessionmaker = async_sessionmaker(engine, expire_on_commit=False)
    model = await on_startup.get_model(cfg.nn, sessionmaker)
    bot_token = cfg.bot_token.get_secret_value()
    bot = Bot(token=bot_token, parse_mode="HTML")

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(common_router)
    dp.include_router(recognition_router)
    dp.include_router(response_router)

    dp.update.middleware(DBSessionMiddleware(sm=sessionmaker))

    roboflow_api = roboflow_service.initialize_roboflow(
        roboflow_api_settings=cfg.roboflow, neural_network=cfg.nn, bot_token=bot_token
    )
    await bot_set_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, roboflow_api=roboflow_api, model=model)


if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(name)s - %(message)s",
    )
    asyncio.run(main())
