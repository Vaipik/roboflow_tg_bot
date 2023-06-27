import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.handlers import common_router, recognition_router
from bot.utils import initialize_roboflow
from config import cfg


async def main():
    logging.basicConfig(
        level=logging.INFO,
        # format="%(asctime)s [%(levelname)s%] - %(message)s"
    )
    bot = Bot(token=cfg.bot_token.get_secret_value(), parse_mode="HTML")

    dp = Dispatcher(storage=MemoryStorage())
    dp.include_router(common_router)
    dp.include_router(recognition_router)

    roboflow_api = initialize_roboflow(cfg.roboflow)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, roboflow_api=roboflow_api)


if __name__ == '__main__':
    asyncio.run(main())
