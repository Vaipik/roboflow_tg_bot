from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


def uploaded_photo_inline_kb() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text="Yes", callback_data="make_response"),
        InlineKeyboardButton(text="No", callback_data="cancel_response")
    )
    return builder.as_markup()
