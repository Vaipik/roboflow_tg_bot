from dataclasses import dataclass

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot import dto


@dataclass(frozen=True)
class ResponseKeyboardButtons:
    """Dataclass for responses kb."""

    next_callback_data: str = "next_six"  # button name - next, callback data - next_six
    previous_callback_data: str = (
        "previous_six"  # button name - next, callback data - next_six
    )
    next_button_text: str = "➡️"
    previous_button_text: str = "⬅️"


def make_paginate_keyboard(
    responses: list[dto.Response],
    pages: int,
    page: int,
    kb_buttons: ResponseKeyboardButtons = ResponseKeyboardButtons(),
) -> InlineKeyboardMarkup:
    """
    Generate responses 3 in a row with buttons for next and previous six responses.

    :param responses: list of responses that should be shown
    :param pages:
    :param page:
    :param kb_buttons:
    :return: keyboard.
    """
    builder = InlineKeyboardBuilder()
    for i in range(0, len(responses), 2):
        builder.row(
            *[
                InlineKeyboardButton(
                    text=response.generated_at, callback_data=str(response.id)
                )
                for response in responses[i : i + 2]
            ]
        )
    builder.row(
        InlineKeyboardButton(
            text=kb_buttons.previous_button_text,
            callback_data=kb_buttons.previous_callback_data if page > 1 else "pass",
        ),
        InlineKeyboardButton(text=f"{page}/{pages}", callback_data="pass"),
        InlineKeyboardButton(
            text=kb_buttons.next_button_text,
            callback_data=kb_buttons.next_callback_data if page < pages else "pass",
        ),
    )

    return builder.as_markup()
