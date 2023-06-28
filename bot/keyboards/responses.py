from dataclasses import dataclass

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


@dataclass(frozen=True)
class ResponseKeyboardButtons:
    next_callback_data: str = "next_six"  # button name - next, callback data - next_six
    previous_callback_data: str = "previous_six"  # button name - next, callback data - next_six
    next_button_text: str = "➡️"
    previous_button_text: str = "⬅️"


def make_paginate_keyboard(
        responses: list,
        total_responses: int,
        page: int,
        kb_buttons: ResponseKeyboardButtons = ResponseKeyboardButtons()
) -> InlineKeyboardMarkup:
    """
    Generating responses 3 in a row with buttons for next and previous six below response
    :param responses: list of responses that should be shown
    :param total_responses:
    :param page:
    :param kb_buttons:
    :return: keyboard
    """
    pages = total_responses // 6

    builder = InlineKeyboardBuilder()
    for i in range(0, len(responses), 3):
        builder.row(*[
            InlineKeyboardButton(text=response, callback_data="pass") for response in responses[i:i + 3]
        ])
    builder.row(
        InlineKeyboardButton(text=kb_buttons.previous_button_text, callback_data=kb_buttons.previous_callback_data),
        InlineKeyboardButton(text=f"{page}/{pages}", callback_data="pass"),
        InlineKeyboardButton(text=kb_buttons.next_button_text, callback_data=kb_buttons.next_callback_data)
    )

    return builder.as_markup()
