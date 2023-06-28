from dataclasses import dataclass

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import ReplyKeyboardBuilder


@dataclass(frozen=True)
class CommonKeyBoardButtons:
    results: str = "Previous results"
    recognize: str = "Generate new"


def make_main_keyboard(
        kb_buttons: CommonKeyBoardButtons = CommonKeyBoardButtons()
) -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()
    builder.row(
        KeyboardButton(text=kb_buttons.results),
        KeyboardButton(text=kb_buttons.recognize),
    )
    builder.adjust(2)
    return builder.as_markup(resize_keyboard=True)

