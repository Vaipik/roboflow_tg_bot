from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def bot_set_commands(bot: Bot):
    commands = [
        BotCommand(command="start", description="Bot main menu"),
        BotCommand(command="cancel", description="Stop any operation"),
    ]
    await bot.set_my_commands(commands, scope=BotCommandScopeAllPrivateChats())
