from dataclasses import dataclass

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder


@dataclass(frozen=True)
class RecognitionKeyboardButtons:
    yes_button: str = "make_response"
    no_button: str = "cancel_response"
    make_response: str = "Yes"
    upload_another: str = "No"


def uploaded_photo_inline_kb(
    kb_buttons: RecognitionKeyboardButtons = RecognitionKeyboardButtons(),
) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(
            text=kb_buttons.make_response, callback_data=kb_buttons.yes_button
        ),
        InlineKeyboardButton(
            text=kb_buttons.upload_another, callback_data=kb_buttons.no_button
        ),
    )
    return builder.as_markup()
