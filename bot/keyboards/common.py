from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def make_main_keyboard() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text="Previous results"),
        KeyboardButton(text="Generate new"),
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

