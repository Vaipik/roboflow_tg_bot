from aiogram import F, Router
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from bot.keyboards.common import CommonKeyBoardButtons
from bot.keyboards.responses import ResponseKeyboardButtons, make_paginate_keyboard
from bot.states.responses import ResponseStates


response_router = Router()


@response_router.message(
    F.text == CommonKeyBoardButtons.results
)
async def generate_responses(message: Message, state: FSMContext):
    user_id = message.from_user.id
    await state.update_data(user_id=user_id, page=1)
    # responses = await db.get_responses(user_id, offset=0, limit=6)
    responses = [f"response_{i}" for i in range(1, 19)]
    await message.answer(
        text="Responses:",
        reply_markup=make_paginate_keyboard(responses, len(responses) * 2, 1)
    )
    await state.set_state(ResponseStates.paginated_response)


@response_router.callback_query(
    ResponseStates.paginated_response,
    Text(ResponseKeyboardButtons.previous_callback_data)
)
async def previous_five_responses(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    page = user_data["page"] - 1
    responses = [f"response_{i}" for i in range(1 + 19 * (page - 1), 19 * (1 + (page - 1)))]
    await callback.message.edit_text(
        text="Responses:",
        reply_markup=make_paginate_keyboard(responses, len(responses) * 4, page)
    )
    await state.update_data(page=page)


@response_router.callback_query(
    ResponseStates.paginated_response,
    Text(ResponseKeyboardButtons.next_callback_data)
)
async def previous_five_responses(callback: CallbackQuery, state: FSMContext):
    user_data = await state.get_data()
    page = user_data["page"] + 1
    responses = [f"response_{i}" for i in range(1 + 19 * (page - 1), 19 * (1 + (page - 1)))]
    await callback.message.edit_text(
        text="Responses:",
        reply_markup=make_paginate_keyboard(responses, len(responses) * 4, page)
    )
    await state.update_data(page=page)
