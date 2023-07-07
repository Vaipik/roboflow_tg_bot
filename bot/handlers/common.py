from aiogram import Router
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, ReplyKeyboardRemove

from bot.keyboards.common import make_main_keyboard

common_router = Router()


@common_router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """Entry command for tg bot."""
    await state.clear()
    await message.answer(
        text="What do you want to do ?\n", reply_markup=make_main_keyboard()
    )


@common_router.message(Command("cancel"))
@common_router.message(Text(text="cancel", ignore_case=True))
async def cmd_cancel(message: Message, state: FSMContext):
    """Stop all operations wherever they are."""
    await state.clear()
    await message.answer(text="Action cancelled", reply_markup=ReplyKeyboardRemove())
