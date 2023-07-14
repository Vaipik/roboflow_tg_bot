from aiogram import F, Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.infrastructure.db.uow import SQLAlchemyUoW
from bot.keyboards.common import CommonKeyBoardButtons, make_main_keyboard
from bot.keyboards.responses import ResponseKeyboardButtons, make_paginate_keyboard
from bot.states.responses import ResponseStates
from bot.utils.paginator import get_pages
from bot.utils import text_templates


response_router = Router()


@response_router.message(F.text == CommonKeyBoardButtons.results)
async def generate_responses(message: Message, state: FSMContext, uow: SQLAlchemyUoW):
    """Generate inline kb with previous user responses."""
    chat_id = message.from_user.id
    responses = await uow.responses.get_user_responses(chat_id, offset=0, limit=6)

    pages = get_pages(await uow.responses.count_responses(chat_id))
    await state.update_data(
        chat_id=chat_id,
        page=1,
        pages=pages,
    )
    await message.answer(
        text="Responses:",
        reply_markup=make_paginate_keyboard(responses, pages, 1),
    )
    await state.set_state(ResponseStates.paginated_response)


@response_router.callback_query(
    ResponseStates.paginated_response,
    Text(ResponseKeyboardButtons.previous_callback_data),
)
async def previous_five_responses(
    callback: CallbackQuery, state: FSMContext, uow: SQLAlchemyUoW
):
    """Generate previous user responses."""
    user_data = await state.get_data()
    page = user_data["page"] - 1
    pages = user_data["pages"]
    chat_id = user_data["chat_id"]
    offset = 6 * (page - 1)

    responses = await uow.responses.get_user_responses(chat_id, offset=offset)
    await callback.message.edit_text(
        text="Responses:",
        reply_markup=make_paginate_keyboard(responses, pages, page),
    )
    await state.update_data(page=page)


@response_router.callback_query(
    ResponseStates.paginated_response, Text(ResponseKeyboardButtons.next_callback_data)
)
async def next_five_responses(
    callback: CallbackQuery, state: FSMContext, uow: SQLAlchemyUoW
):
    """Generate next user responses."""
    user_data = await state.get_data()
    page = user_data["page"] + 1
    pages = user_data["pages"]
    chat_id = user_data["chat_id"]
    offset = 6 * (page - 1)

    responses = await uow.responses.get_user_responses(chat_id, offset=offset)

    await callback.message.edit_text(
        text="Responses:",
        reply_markup=make_paginate_keyboard(responses, pages, page),
    )
    await state.update_data(page=page)


@response_router.callback_query(ResponseStates.paginated_response, Text("pass"))
async def do_nothing(callback: CallbackQuery):
    """Just do nothing in case of callback data."""
    await callback.answer()


@response_router.callback_query(ResponseStates.paginated_response, Text(contains="-"))
async def make_response(callback: CallbackQuery, state: FSMContext, uow: SQLAlchemyUoW):
    """Generate user response."""
    response_id = callback.data
    response = await uow.responses.get_user_response_by_id(response_id)
    if response.recognized_image_id:
        await callback.message.answer_photo(
            photo=response.recognized_image_id,
            caption=text_templates.roboflow_success_response(response.get_labels()),
            reply_markup=make_main_keyboard(),
        )
    else:
        await callback.message.answer(
            text=text_templates.roboflow_empty_response(),
            reply_markup=make_main_keyboard(),
        )
    await state.clear()
    await callback.answer()
